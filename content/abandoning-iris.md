Title: Abandoning Iris
Slug: abandoning-iris
Date: 2015-07-14 17:45
Modified: 2015-07-14 17:45
Authors: Daniel Rothenberg
 
Seven years ago, when I first started working with climate model output and analysis within Python, the software stack we had available was pretty shoddy. Although [direct interfaces to netCDF](https://github.com/Unidata/netcdf4-python) (the *de facto* standard data format in climate science) existed, they could be kind of clunky. They didn't have smart ways to manipulate coordinate systems attached to the data, they didn't play nice with updating metadata, and they usually had dependencies which were difficult to deal with (considering the bifurcation between netCDF3/netCDF4/HDF5). 

Some okay toolkits existed, though. A [package maintained by NCAR](https://www.pyngl.ucar.edu/Nio.shtml) exposed a good interface for manipulating netCDF data, and allowed you to play directly with NCL - a graphics scripting language used in the atmospheric sciences). But working with these tools - and cartographic supplements like [Basemap](http://matplotlib.org/basemap/) was very hacky and headache-inducing.

### Enter Cartopy/Iris

When I started my PhD, I knew it was time for a change. I wanted to build better, flexible packages for repeating my various analyses with minimal repetition of code and with the hopes that other people could use my code whenever they wanted. The stack wasn't up to the task.

Luckily, two major toolkits came to maturity around this time: [cartopy](http://scitools.org.uk/cartopy/docs/latest/index.html) and [iris](http://scitools.org.uk/iris/docs/latest/index.html). Cartopy is a Basemap-replacement, with some more sophisticated routines and a simpler interface for dealing with re-gridding, map projections, and combining geographical data from all sorts of different sources. For instance, one of the gallery examples from cartopy is a visualization of Hurricane Katrina's track and impacts in the US:

![Katrina cartopy example](http://scitools.org.uk/cartopy/docs/latest/_images/hurricane_katrina_01_00.png)

The script which generates this figure is incredibly simple; suddenly, you could build GIS-type graphics with minimal effort! Within cartopy, you can also easily combine geographical data from many different sources. This quick plot I made for a thesis committee meeting combines two completely different MODIS satellite data sources and output from the online HYSPLIT calculator:

![fire map april 2011]({filename}/images/2015/07/MODIS_CentAm_Fires_AOD_Hysplit_4_24.png)

As another example, here's a visualization combining some GOES-R IR satellite imagery with timeseries data from a flight during the [MACPEX field campaign](http://www-air.larc.nasa.gov/missions/macpex/macpex.html):

![MACPEX GOES-R IR]({filename}/images/2015/07/IR-4_flightpath_20110425_183229.png)

Iris is a toolkit which integrates directly with cartopy by wrapping geophysical data sets. Rather than load a dataset directly using a low-level interface, iris exposes a different API which allows you to manipulated data more semantically. You can slice through dimensions, perform aggregations or apply functions over them, and generally pipeline your analyses in such a way that you preserve the metadata attached to your dataset. It can also handle multi-file datasets by seamlessly concatenating over record dimensions. But best of all, it wraps the matplotlib+cartopy visualization ecosystem so that you can very quickly and easily generate maps of your data.

### Python 3

I was content with these tools until I decided to suck it up and migrate to Python 3. That posed a problem - cartopy works *ok* with Python 3 (as in, I haven't run into any issues yet). But iris emphatically doesn't. It's also not clear when iris will become Python 3-compliant. 

Luckily, there are *fantastic* alternatives to iris available. One of my favorites is [xray](http://xray.readthedocs.org/en/stable/), which exposes an API offering much of the same sort semantic handling of your netCDF data, but in a less-clunky, simpler manner. It also directly extends a good deal of the logic behind pandas, which itself is a fantastic way to manipulate timeseries/indexed datasets. Xray also works with Python 3 out of the box, and can very easily work with cartopy plotting routines ([it even has a plotting library in the works](http://xray.readthedocs.org/en/feature-plotting/)).

### Conclusions

I still like iris. Up until this week, I was developing my analysis toolkit such that you could work with either xray/iris in any context, and seamlessly convert between the two. But the lack of Python 3 support - at the critical time *when I actually have some extra time to get used to the changes* - is enough to demote it from the top of my scientific Python stack. This doesn't even get to all the awesome goodies that xray implements, like [dask integration for out-of-core computing](http://dask.pydata.org/en/latest/).

So for now, there's a new workhorse in my toolkit!
