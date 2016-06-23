Title: landing
Template: pages/landing
Save_as: index.html
Status: hidden

<!--
Using the vertical-align class I've made here works fine, but then when bootsrap collapses things in mobile view, it screws up - they should just stack, not stay aligned side-by-side!
-->
<div class="row vertical-align">
  <div class="col-lg-4 hidden-xs">
    <p>
      <img class="headshot img-circle" src="{filename}/images/headshot.png"  />
    </p>
  </div>
  <div class="col-lg-8">
    <div class="row">
      <div class="col-lg-12">
        <p>I’m a doctoral candidate in the Program in Atmospheres, Oceans, and Climate at the <a href="http://www.mit.edu">Massachusetts Institute of Technology</a>. My research focuses on the interactions between aerosols, clouds, and climate, but I have many interests including in science policy, scientific software, open/reproducible science, and classical violin.</p>
      </div>
    </div>
    <div class="row">                
        <div class="col-md-12">
          <ul class="list-inline social-media">
            <li><a href="http://www.twitter.com/danrothenberg"<i class="fa fa-twitter-square" aria-hidden="true"></i></a></li>
            <li><a href="http://www.github.com/darothen"><i class="fa fa-github-square" aria-hidden="true"></i></a></li>
            <li><a href="http://www.linkedin.com/in/rothenbergdaniel"><i class="fa fa-linkedin-square" aria-hidden="true"></i></a></li>
            <li><a href="mailto://darothen@mit.edu"><i class="fa fa-envelope" aria-hidden="true"></i></a></li>
          <ul>
        </div>
    </div>
  </div>
</div>
