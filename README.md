# Personal Homepage

This repository contains the content and code for producing my personal homepage, with the aid of [pelican](http://blog.getpelican.com/).

## Deployment

Not many Python packages are needed for deployment here, but the few that are are listed and maintained in a conda environment. To install that environment, simply execute

``` shell
$ conda env create -f environment.yml
```

the resulting environment, `blog`, can be activated with

``` shell
$ source activate blog
```
