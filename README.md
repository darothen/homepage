# Personal Homepage

This repository contains the content and code for producing my personal homepage, with the aid of [pelican](http://blog.getpelican.com/).

## Deployment

Not many Python packages are needed for deployment here, but the few that are are listed and maintained in a conda environment. To install that environment, simply execute

``` shell
$ conda env create -f environment.yml
```

the resulting environment, `blog`, can be activated with

``` shell
$ conda activate blog
```

Alternatively, you can just use the included `requirements.txt` to prepare the necessary packages

## Development

For development, simply start a dev server using the supplied Makefile via `make devserver` and navigate to [localhost:8000/output/](). You should hit the landing page.


## Deployment

Use the included [makefile]:

``` shell
$ make html
$ make publish
$ make ssh_upload
```


## Gotchas

- May need to manually install most-recent Jinja
- Have a glitch in Markdown pkg and have pinned version number