Title: New Website Design
Slug: new-website-design
Tags: Python, blog
Date: 2016-07-13 10:57
Modified: 2016-07-13 10:57
Authors: Daniel Rothenberg

Although it's not 100% finished, I'm launching the new version of my homepage. This version departs significantly from my older versions in that I've chosen to move everything to static site generator. I think this gels a nicer with my current writing/tools workflow, which leans *heavily* on plain-text files and eschews fancier note-taking programs like Evernote or OneNote.

## Static Site Generators

A static site generator differs from the usual content management system approach in that there is no database running behind the scenes; the entire site is static content, which can be built once and uploaded directly to a server. You can then choose to author your content however you like, with a mixture of plaintext markup languages, templates, and straight HTML or CSS files. Truthfully, this is a much better solution for a part-time blogger, because it provides a simple way to spin-off any of your notes or short writings into a quick blog post on the fly.

The best part of adopting a static site generator is that there are **loads** of tools available for this purpose. Without re-hashing the pros/cons of many, I want to quickly document my own criteria for choosing such a tool:

1. **Python-based**. This was non-negotiable; I wanted something that I could quickly hack and configure on my own, and Python is the best language for that.
2. **Supports theming**. Initially, I didn't want to theme an entire site by myself - I wanted to hack something into submission and *then* build something from the ground up.
3. **Active development**. It's important to me that people are actively working on a project, because this ensures there will be ample sample code when you choose to delve in and hack the project to bend it to your will.
4. **Simple building/tooling**. For great hacking! And incremental builds, which (hopefully) will be necessary as I spend more time churning out content for my blog.

I spent quite a while checking out the existing tools available within the Python ecosystem. At the end of the day, the project that seemed to fit my needs the best was [Pelican](http://blog.getpelican.com/). And so, with a quick `git init` and `pelican-quickstart`, this new homepage was born! I split the code for maintaining the website into two parts: a [main codebase](https://github.com/darothen/homepage) for archiving and deploying content, and a [theme submodule](https://github.com/darothen/pelican-darothen/tree/e64b0683d0ffd47e51efaef5a7f78567fcc56efc) which can be maintained separately.

## Porting from Ghost

The last iteration of my homepage used [ghost](https://ghost.org/), a nice, node-js based blogging application. My main reason for moving away from this was to move to a writing workflow that integrated more closely with more content setup for taking notes, and to have better control over the main "page" content (non-blog posts) hosted on the site.

However, I still wanted to preserve the posts I had published on the old site. This ended up being very easy to do. First, I simply dumped all the content from my website using ghost's online interface to a JSON file on disk. I had to manually copy over all the old images, but they were organized very simply on my webhost so I could just `rsync` them locally (I preserved the folder hierarchy, where images were organized into folders by the year they were uploaded). The only remaining task was to convert the JSON database into individual Markdown files for Pelican to render. Luckily, the page content on ghost is *already* in Markdown, so I really only needed to extract each element in the JSON database and its associated metadata. The script I used to do this is [archived in my homepage's new repository](https://github.com/darothen/homepage/blob/master/old_blog/convert_ghost_posts.py), although it only had to be run once.

## New Content and Theming

With all my old content ported, now came the task of building new pages for my site. I really wanted a professional homepage to display some of my work projects and research interests - more-so than just writing short blog posts on them (although I'll plan on doing that in the near future). One option that came to mind was to have a distinct Pelican "category" for the "main" pages on my website; each entry would be its own blog post. An alternative - which is what I used - was to author static content to serve.

This ended up being a better solution, because I ultimately decided to use complex layouts on the main content pages. Although Pelican excels at quickly rendering straightforward Markdown, you can really serve any plaintext that you want, as long as you provide a suitable adapter. *Additionally*, you can provide straight-up HTML web pages. The material that I wanted to show on my static pages didn't really lend itself to a simple template or layout, so I simply took advantage of Pelican's HTML adapter and just authored some HTML pages. This let me set all the custom theming and styling I wanted without having to negotiate a template.

With regards to theming, I really wanted a simple, straightforward website. Several community offerings to the Pelican project were attractive, but in service towards my goal of ultimately building a theme from the ground up, I adopted the [pelican-bootstrap3](https://github.com/getpelican/pelican-themes/tree/master/pelican-bootstrap3) project. By itself, this is a *great* theme; it uses the [Bootstrap HTML/CSS/JS framework](http://getbootstrap.com/) to control page layout and elements and provides a responsive page layout that looks beautiful on screens of all sizes. In its vanilla form, the theme has tons of customizable options exposed, such as side-bars, navbars, and footers. I [hacked it into the form you see here](https://github.com/darothen/pelican-darothen/tree/e64b0683d0ffd47e51efaef5a7f78567fcc56efc), complete with my own templating, page design, and custom styling. When the new iteration of Bootstrap is released sometime later this year, I plan on totally building my own theme using it from the ground up. It'll still be simple, but because I plan on being the main user, I won't bother with adding lots of Python hooks - everything will be tweakable through HTML/CSS directly.

## Continuing development

I plan on continuing to flesh out the content and theme of the webpage. In particular:

- New CV page, based on a re-factoring of my [vita](https://github.com/darothen/vita) projects
- New blog theme
- Overhaul of bootstrap theme, pending release of Bootstrap 4
- Automatic hosting of my research notes, which are published separately
- Automatic deployment via Travis CI

These will all be spectacular distractions while I finish up my dissertation!
