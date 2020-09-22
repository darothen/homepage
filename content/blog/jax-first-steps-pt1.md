Title: First Steps with Jax, Part 1
Slug: jax-first-steps-pt1
Tags: jax, autodiff, programming
Date: 2020-09-21 23:00
Authors: Daniel Rothenberg

Earlier this summer, I took some time to invest in getting more comfortable with the latest-and-greatest deep learning frameworks that had been released over the past two or so years.
While my [Keras](https://keras.io/)-fu was serving me well with a lot of the toy deep learning projects I'd mess around with, I knew that there were freshser takes on the same basic tools, and it can never hurt to try something new -- after all, a wise Computer Science teacher once told me that it's better to learn more languages and approaches than fewer. 

So towards that end, I took some "Hello, world!" deep learning projects (the classics, such as MNIST digit classification, and two from my own, including a simple precipitation nowcasting demo) and embarked on a journey to write the same problem over and over again, trying out any framework I could find.
And boy, did I find a lot!
From Flux to PyToch to fast.ai, I was really enjoying the change from my day job, just writing some code and learning some new (but familiar) things.

And then I stumbled across [jax](https://github.com/google/jax).

Or rather, I re-discovered jax in some notes for an old project. 
Jax is a powerful programming tool which does two very impressive things.
First, jax allows you to take idiomatic, array-oriented NumPy code and just-in-time compile it with [XLA](https://www.tensorflow.org/xla), so that your code can target GPUs or other accelerators.
That's pretty cool in its own right, but jax has one other awesome trick up its sleeve -- it's effectively an auto-differentation tool for NumPy-based code. 

The purpose of this series of blog posts isn't to delve into too much technical detail on auto-differentation or even to be a "how-to" guide for getting started with jax.
Rather, when I re-discovered jax over the summer, I hit a great streak where I was able to churn out a number of proof-of-concept codes for my own gratification, mostly centered around applications of [neural ODEs](https://arxiv.org/abs/1806.07366) and data assimilation. 
I'm not an expert on the idiosyncrasies with, say, deriving the reverse-mode derivative of an ODE IVP as found in that paper by Chen et al, but my several pages of chicken scratch notes, annotations of the implementation of the technique in jax, and more importantly, my applications, might be useful to others looking to learn more about the topic.
So, this series of blog posts are cleaned-up versions of my demos building towards a simple 4DVar of the Lorenz96 system with jax, taking some detours along the way to play with jax's ecosystem of deep learning tools. 

All of the demos are written in and archived on [Google Colaboratory](https://colab.research.google.com/), but rendered here for convenience (with links to the actual code).

We'll kick things off with a gentle introduction to jax.

{% notebook jax-first-steps-pt1.ipynb cells[1:] %}

