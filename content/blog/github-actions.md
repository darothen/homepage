Title: Automating My Homepage Builds with GitHub Actions
Slug: automating-build-github-actions
Tags: github, automation, ci/cd
Date: 2020-07-25 23:00
Authors: Daniel Rothenberg

[GitHub Actions](https://docs.github.com/en/actions) is a simple tool available with any repository you create on GitHub to create automated workflows to support your software development. 
As a scientist or a junior developer, this might seem like an esoteric feature -- I have enough terminal-fu to do what I need and I can write scripts, so why would I ever need something like this? 
The use cases, it turns out, are nearly endless:

1. Implementing CI/CD pipelines (automated testing, builds against different systems, linting, generating updated documentation, etc.)
2. Coordinating with collaborators (automatically e-mailing or texting when new code is ready for review)
3. Automatic publishing (we'll see that here in a moment)

... and much more!

## Compiling My Homepage

As I've mentioned in a [previous blog post]({filename}/blog/new-website.md), my homepage (for now) is a static site compiled with [Pelican](https://docs.getpelican.com/en/stable/).
Building and deploying the site is very simple; I have a a standard `Makefile` with rules for launching a local development server, building the static content when there are changes, and deploying to my web host.
The entire process can be invoked on my local machine with three commands in my terminal:

``` shell
$ make html     # Generate HTML content from my Markdown/RST/Notebook files
$ make publish  # Generate publishable form using Pelican
$ make rsync_upload  # Use rsync to transfer to my host
```

That's pretty easy, right?
This approach comes with some caveats, unfortunately. 
For starters, I have to have Pelican and some related packages installed if I want to execute this type of build.
I also need to worry about having appropriate SSH keys set up in order to deploy to my web host.
While these problems are relatively simple to mitigate, they're annoying; wouldn't it be nice if anytime I had any idea for a blog post or wanted to make a quick tweak to the website, I could just go into GitHub and make a quick change?

## Enter GitHub Actions

This sort of workflow is *perfect* for automating using GitHub Actions (GHA for short from here on).
GHA provides a very simple mechanism for creating workflows; you provide a YAML file with a few special keys describing how a given workflow is triggered, and then provide a set of "jobs" to trigger composed of individual steps.
One of the attractive things about GHA is that is community-integrated -- GitHub and many independent developers offer simple, canned steps that you may want to use in a job, such as cloning your repository (which is nice and lets you avoid dealing with GitHub authentication in some random Docker image running on some random VM!), uploading/retrieving build artifacts to/from short-term storage, setting up common development environments such as Node.js or Python, and [much more](https://github.com/marketplace?type=actions) (over 4500 more, to be precise!).

If you're used to [CircleCI](https://circleci.com/), [TravisCI](https://travis-ci.com/), [Jenkins](https://www.jenkins.io/), or anything similar, GitHub Actions will be extremely familiar. 
Of these tools, I've the most experience with CircleCI. 
Both tools allow you to define "secrets" natively within their respective UIs/tools, which is super handy for dealing with passwords, SSH keys, and similar.
Furthermore, both tools allow you to lean heavily on Docker images to run your workflows.
At the end of the day I think for most standard CI/CD pipelines or workflows you can probably get away with either tool and be happy.

## Our Build/Deploy Workflow

To highlight just how easy this tool is to use, here's the complete workflow I built for building and deploying the entire website:

``` yaml
name: Compile latest content and deploy

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:

  compile_and_deploy:
    name: Compile latest content
    runs-on: ubuntu-latest
    steps:
      - name: Checkout latest materials
        uses: actions/checkout@v2
        with:
          submodules: 'true'
      
      - name: Set up Python
        uses: actions/setup-python@v1
        with:
          python-version: 3.8

      - name: Install required packages
        run: |
          python --version
          pip install wheel
          pip install -r requirements.txt

      - name: Compile latest content
        run: |
          make html
          make publish
      
      - name: Install SSH key
        uses: shimataro/ssh-key-action@v2
        with:
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          known_hosts: ${{ secrets.KNOWN_HOSTS }}
          name: id_rsa 

      - name: Deploy to Webfaction
        run: |
          make rsync_upload 
```

The vast majority of this workflow is self-explanatory, and is comprised of just a handful of steps:

1. Check-out our latest changes to the repository
2. Install Python
3. Install the packages we need to build the website 
4. Compile the website
5. Set up SSH keys so we can upload to the web host
6. Upload to the web host

and *that's it*! 
The entire process runs in less than a minute when it is executed by GitHub Actions.

The only idiosyncrasy I ran into during the entire process was in dealing with authentication with my web host. 
I've always used privately-managed SSH keys for this.
Managing these sorts of "secrets" is a cumbersome but critical part of any automated workflow you may wish to build/productionize, especially if it's even a single bit more complicated than a toy. 
There are different strategies for dealing with this: adding an encrypt/decrypt capability to your deployment; preparing some sort of whitelist or DMZ so that you can sidestep authentication (highly inadvisable!); and probably many more. 

My approach here was to leverage the built-in secrets functionality that GitHub/Actions provides, and then use the an Action I found on the Marketplace called [`ssh-key-action`](https://github.com/marketplace/actions/install-ssh-key). 
This Action installs a user-provided SSH key and configures a `known-hosts` file to make negotiating with a remote server over SSH quite easy.

### Preparing an SSH Key for Deployment

I created a single-purpose SSH key for use with this application. 
The complete set of steps for doing this looked something like this:

1. **Generate a new ssh key**: Execute the command `ssh-keygen -m PEM -t rsa`; this will create both your private key and a corresponding public key file (e.g. *~/.ssh/id_rsa{.pub}*).
2. **Register the public key on the web host**: This can be most easily done with the utility tool, `ssh-copy-id -i /path/to/my/key.pub user@webhost`; you'll need to enter your password. To confirm this work, SSH into the webhost directly and make sure that the public key appears in *~/.ssh/authorized_keys*
3. **Add your private key as a secret in your GitHub repo**; You can grab the private key by executing `pbcopy < /path/to/my/key`, and then copy/paste it into a new entry on **Settings/Secrets** in your repo's page on GitHub. Note the name of the entry (I used `SSH_PRIVATE_KEY`).
4. **Add the remote host as a secret in your GitHub repo**; Similarly, you need to record the fingerprint of the host you'll be connecting to. By virtue of this short workflow, you'll have a record of it in *~/.ssh/known_hosts* (likely the very last entry). Copy this and create another new secret on GitHub (mine is `KNOWN_HOSTS`) with the fingerprint.
5. **Confirm the secret names in your workflow**; We pass the secret key and known hosts stub to the `ssh-key-action` step of our workflow, as shown in the full example above.

---

When all is said and done, this provides a super simple way to automate builds and deploys of my homepage. 
Now, my current workflow is to draft new content in a feature branch, and once it's merged in via PR, it'll be live at danielrothenberg.com in less than a minute without any intervention on my behalf.
And if I'm out in the mountains and get a text message that there is a typo on my website, I can quickly pull up my repo on my phone's web browser, make a quick hack, and commit without ever needing to touch a computer!