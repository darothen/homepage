Title: Plotting HYCOM/RTOFS SST data in Python
Slug: plotting-hycomrtofs-sst-data-in-python
Tags: python, cartopy, iris, xray, visualization, netcdf, data
Date: 2015-07-02 13:01
Modified: 2015-07-02 13:01
Authors: Daniel Rothenberg


Based on [this notebook](https://gist.github.com/darothen/84ae9a29154389fe45a5), which highlights some basics on reading in RTOFS/netCDF output into Python, manipulating that data, and plotting it. For additional examples, [Filipe Fernandes has a great example of similar operations on his blog](https://ocefpaf.github.io/python4oceanographers/blog/2014/12/29/iris_ocean_models/).


```python
    import netCDF4 as nc
    import numpy as np

    %matplotlib inline
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set(style="ticks")
```

Download some RTOFS global output. It's a rather large file, so be sure to comment out this command once it's already downloaded!


``` language-bash
#!curl -O ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/rtofs.20150701/rtofs_glo_2ds_f001_1hrly_prog.nc
```

For starters, let's read in the data using the Unidate `netCDF4` module. This module gives very low-level access to the netCDF file - basically just its raw contents and metadata. We load the file directly into memory using the `Dataset` type, and print it to give an overview of its contents.

``` language-python
    fn = "rtofs_glo_2ds_f001_1hrly_prog.nc"
    data = nc.Dataset(fn)
    print data
```

    <type 'netCDF4.Dataset'>
    root group (NETCDF3_CLASSIC data model, file format UNDEFINED):
        Conventions: CF-1.0
        title: HYCOM ATLb2.00
        institution: National Centers for Environmental Prediction
        source: HYCOM archive file
        experiment: 90.9
        history: archv2ncdf2d
        dimensions(sizes): MT(1), Y(3298), X(4500), Layer(1)
        variables(dimensions): float64 [4mMT[0m(MT), float64 [4mDate[0m(MT), int32 [4mLayer[0m(Layer), int32 [4mY[0m(Y), int32 [4mX[0m(X), float32 [4mLatitude[0m(Y,X), float32 [4mLongitude[0m(Y,X), float32 [4mu_velocity[0m(MT,Layer,Y,X), float32 [4mv_velocity[0m(MT,Layer,Y,X), float32 [4msst[0m(MT,Y,X), float32 [4msss[0m(MT,Y,X), float32 [4mlayer_density[0m(MT,Layer,Y,X)
        groups:



Each `Dataset` object contains a dict-like interface for accessing variables, which can be selected by their *var_name* from the original netCDF file. Let's select the SST data and inspect it in more detail.


``` language-python
    sst = data.variables['sst']
    print sst
```

    <type 'netCDF4.Variable'>
    float32 sst(MT, Y, X)
        coordinates: Longitude Latitude Date
        standard_name: sea_surface_temperature
        units: degC
        _FillValue: 1.26765e+30
        valid_range: [ -3.58215308  34.7584877 ]
        long_name:  sea surf. temp.   [90.9H]
    unlimited dimensions: MT
    current shape = (1, 3298, 4500)
    filling off



This gives us a quick overview of the sst data. It's a 3-dimensional dataset (time, latitude, and longitude). Furthermore, from the inspection of the full dataset, we can see that the latitude and longitude coordinates are actually aliases for a complex, 2D latitude-longitude system underpinning the model coordinate systems.

---

Note that we can use standard netCDF terminal commands to also inspect the contents of the dataset:


``` language-bash
    !ncdump -h {fn}
```

    netcdf rtofs_glo_2ds_f001_1hrly_prog {
    dimensions:
    	MT = UNLIMITED ; // (1 currently)
    	Y = 3298 ;
    	X = 4500 ;
    	Layer = 1 ;
    variables:
    	double MT(MT) ;
    		MT:long_name = "time" ;
    		MT:units = "days since 1900-12-31 00:00:00" ;
    		MT:calendar = "standard" ;
    		MT:axis = "T" ;
    	double Date(MT) ;
    		Date:long_name = "date" ;
    		Date:units = "day as %Y%m%d.%f" ;
    		Date:C_format = "%13.4f" ;
    		Date:FORTRAN_format = "(f13.4)" ;
    	int Layer(Layer) ;
    		Layer:units = "layer" ;
    		Layer:positive = "down" ;
    		Layer:axis = "Z" ;
    	int Y(Y) ;
    		Y:point_spacing = "even" ;
    		Y:axis = "Y" ;
    	int X(X) ;
    		X:point_spacing = "even" ;
    		X:axis = "X" ;
    	float Latitude(Y, X) ;
    		Latitude:standard_name = "latitude" ;
    		Latitude:units = "degrees_north" ;
    	float Longitude(Y, X) ;
    		Longitude:standard_name = "longitude" ;
    		Longitude:units = "degrees_east" ;
    		Longitude:modulo = "360 degrees" ;
    	float u_velocity(MT, Layer, Y, X) ;
    		u_velocity:coordinates = "Longitude Latitude Date" ;
    		u_velocity:standard_name = "eastward_sea_water_velocity" ;
    		u_velocity:units = "m/s" ;
    		u_velocity:_FillValue = 1.267651e+30f ;
    		u_velocity:valid_range = -2.127099f, 2.834078f ;
    		u_velocity:long_name = " u-veloc. [90.9H]" ;
    	float v_velocity(MT, Layer, Y, X) ;
    		v_velocity:coordinates = "Longitude Latitude Date" ;
    		v_velocity:standard_name = "northward_sea_water_velocity" ;
    		v_velocity:units = "m/s" ;
    		v_velocity:_FillValue = 1.267651e+30f ;
    		v_velocity:valid_range = -2.466692f, 2.390137f ;
    		v_velocity:long_name = " v-veloc. [90.9H]" ;
    	float sst(MT, Y, X) ;
    		sst:coordinates = "Longitude Latitude Date" ;
    		sst:standard_name = "sea_surface_temperature" ;
    		sst:units = "degC" ;
    		sst:_FillValue = 1.267651e+30f ;
    		sst:valid_range = -3.582153f, 34.75849f ;
    		sst:long_name = " sea surf. temp.   [90.9H]" ;
    	float sss(MT, Y, X) ;
    		sss:coordinates = "Longitude Latitude Date" ;
    		sss:standard_name = "sea_surface_salinity" ;
    		sss:units = "psu" ;
    		sss:_FillValue = 1.267651e+30f ;
    		sss:valid_range = 0.2699257f, 40.10468f ;
    		sss:long_name = "sea surf. salnity  [90.9H]" ;
    	float layer_density(MT, Layer, Y, X) ;
    		layer_density:coordinates = "Longitude Latitude Date" ;
    		layer_density:standard_name = "sea_water_potential_density" ;
    		layer_density:units = "sigma" ;
    		layer_density:_FillValue = 1.267651e+30f ;
    		layer_density:valid_range = 0.f, 0.f ;
    		layer_density:long_name = " density [90.9H]" ;

    // global attributes:
    		:Conventions = "CF-1.0" ;
    		:title = "HYCOM ATLb2.00" ;
    		:institution = "National Centers for Environmental Prediction" ;
    		:source = "HYCOM archive file" ;
    		:experiment = "90.9" ;
    		:history = "archv2ncdf2d" ;
    }


---

Another useful package for reading in netCDF or other structured datasets is [`xray`](http://xray.readthedocs.org/en/stable/). `xray` automatically labels coordinate axes and gives a `pandas`-like interface to manipulating data. For instance, here is an example of selecting the sst data from the netCDF file using `xray`, and plotting the distribution of temperature values:


``` language-python
    import xray
    ds = xray.open_dataset(fn, decode_times=True)
    sst = ds.sst.values.ravel()
    sst_masked = sst[~np.isnan(sst)]

    ## Masking a numpy array with multiple logical criteria:
    # sst_between_-10_5 = sst[(sst > -10) & (sst < 5)]

    sns.distplot(sst_masked)
    print ds.sst[0]
    plt.imshow(ds.sst[0,::-100,::100])
```

    <xray.DataArray 'sst' (Y: 3298, X: 4500)>
    array([[ nan,  nan,  nan, ...,  nan,  nan,  nan],
           [ nan,  nan,  nan, ...,  nan,  nan,  nan],
           [ nan,  nan,  nan, ...,  nan,  nan,  nan],
           ...,
           [ nan,  nan,  nan, ...,  nan,  nan,  nan],
           [ nan,  nan,  nan, ...,  nan,  nan,  nan],
           [ nan,  nan,  nan, ...,  nan,  nan,  nan]])
    Coordinates:
        MT         datetime64[ns] 2015-07-01T01:00:00.028800
      * Y          (Y) int32 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 ...
      * X          (X) int32 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 ...
        Latitude   (Y, X) float32 -78.64 -78.64 -78.64 -78.64 -78.64 -78.64 ...
        Longitude  (Y, X) float32 74.16 74.24 74.3199 74.4 74.48 74.5601 74.64 ...
        Date       float64 2.015e+07
    Attributes:
        standard_name: sea_surface_temperature
        units: degC
        valid_range: [ -3.58215308  34.7584877 ]
        long_name:  sea surf. temp.   [90.9H]



![png]({static}/images/2015/07/SST_data_11_2.png)


We can also very quickly render the raw data in a cartesian coordinate system using `imshow` from matplotlib. Note that we invert the second axis (latitude) since `imshow` defines its coordinate system from top-to-bottom.


``` language-python
    plt.imshow(ds.sst[0,::-1,...])
```

![png]({static}/images/2015/07/SST_data_13_1.png)

---

A more sophisticated mapping system is provided by the `iris`/`cartopy` ecosystem. `iris` allows us to easily open structured climate data sets (of which this model output is an example), and automatically handles processing of metadata, such as timestamps and coordinate systems. It also has easy-to-use machinery for reprojecting, slicing through, or other basic manipulations of the data.


``` language-python
    import cartopy.crs as ccrs

    import iris
    import iris.plot as iplt
    import iris.quickplot as qplt
```

It's easy enough to load a dataset using `iris`; just open the raw netCDF file, and we'll have a list of *Cube*s for each variable in it, each containing information on the structure of the coordinate system.


``` language-python
    cubes = iris.load(fn)
    print cubes
```

    0: eastward_sea_water_velocity / (m/s) (time: 1; Layer: 1; latitude: 3298; longitude: 4500)
    1: northward_sea_water_velocity / (m/s) (time: 1; Layer: 1; latitude: 3298; longitude: 4500)
    2: sea_surface_salinity / (unknown)    (time: 1; latitude: 3298; longitude: 4500)
    3: sea_surface_temperature / (degC)    (time: 1; latitude: 3298; longitude: 4500)
    4: sea_water_potential_density / (unknown) (time: 1; Layer: 1; latitude: 3298; longitude: 4500)


We can extract a single variable (*Cube*) from the cube list using indexing notation, or the `extract` function. Printing the cube tells us all the metadata we need to know about it.


``` language-python
    #sst_c = cubes[3]
    sst_c = cubes.extract("sea_surface_temperature", strict=True)
    print sst_c
```

    sea_surface_temperature / (degC)    (time: 1; latitude: 3298; longitude: 4500)
         Dimension coordinates:
              time                           x            -                -
              latitude                       -            x                -
                 point_spacing='even'
              longitude                      -            -                x
                 point_spacing='even'
         Auxiliary coordinates:
              date                           x            -                -
              latitude                       -            x                x
              longitude                      -            x                x
                 modulo='360 degrees'
         Attributes:
              Conventions: CF-1.0
              experiment: 90.9
              history: archv2ncdf2d
              institution: National Centers for Environmental Prediction
              source: HYCOM archive file
              title: HYCOM ATLb2.00


Generally speaking, the plotting machinery of `matplotlib` or `cartopy` can't handle 2D coordinate systems very well. So we'll try to re-project the data into a standard system. There are caveats here:

1. The `project` function used below is not fancy; it applies a nearest-neighbor algorithm, so it does not conserve anything about the data. Ideally, you'd want to use something like a bilinear interpolation method to migrate data to the new coordinate system.

2. This particular dataset is weird; the "raw" x-y coordinate system do not have names in the original netCDF file, but `iris` tags them as redundant latitude-longitude coordinates. It still retains the true 2D grid as Auxiliary coords, so we can just delete the mis-named coordinates without harming ourselves too much.

3. The projection method is kind of slow, so we slice through a subset of the data as an example.

4. We use a Plate Carree projection, but any one could do.


``` language-python
    import iris.analysis.cartography as iac
    sst_d = sst_c[0, ::10, ::10]

    sst_d.remove_coord(sst_d.coord(var_name='Y'))
    sst_d.remove_coord(sst_d.coord(var_name='X'))

    new_sst, extent = iac.project(sst_d, ccrs.PlateCarree())

    print new_sst
```

    sea_surface_temperature / (degC)    (projection_y_coordinate: 330; projection_x_coordinate: 450)
         Dimension coordinates:
              projection_y_coordinate                           x                             -
              projection_x_coordinate                           -                             x
         Auxiliary coordinates:
              latitude                                          x                             x
              longitude                                         x                             x
         Scalar coordinates:
              date: 20150701.0417
              time: 2015-07-01 01:00:00
         Attributes:
              Conventions: CF-1.0
              experiment: 90.9
              history: archv2ncdf2d
              institution: National Centers for Environmental Prediction
              source: HYCOM archive file
              title: HYCOM ATLb2.00


We can now easily plot the dataset using `iris`' interface to `matplotlib`, as a proof of concept:


``` language-python
    qplt.pcolormesh(new_sst)
```

![png]({static}/images/2015/07/SST_data_23_1.png)

---

As a slightly fancier example, let's just plot SSTs in the vicinity of the Gulf Stream.

First, we should extract a 'rectangular' box of SST data around the US Atlantic coast form the original dataset. `iris` has problems with 2D coordinate systems (most tools will!), so [Filipe Fernandes has built a package of workarounds that we could use to help](https://ocefpaf.github.io/python4oceanographers/blog/2015/06/29/tardis/). For simplicity, we'll just write a function for extracting the correct points from the 2D data (stolen form Filipe!)


``` language-python
    sst_d = sst_c[:]

    sst_d.remove_coord(sst_d.coord(var_name='Y'))
    sst_d.remove_coord(sst_d.coord(var_name='X'))

    # add 360 to lon coord since it's not symmetric about the prime meridian
    #bbox = [-78.+360., 34., -75.+360., 42.]
    bbox = [-82.0+360., 32., -66.0+360., 45.]

    minmax = lambda x: (np.min(x), np.max(x))

    def bbox_extract_2Dcoords(cube, bbox):
        """
        Extract a sub-set of a cube inside a lon, lat bounding box
        bbox=[lon_min lon_max lat_min lat_max].
        NOTE: This is a work around too subset an iris cube that has
        2D lon, lat coords.

        """
        lons = cube.coord('longitude').points
        lats = cube.coord('latitude').points

        lons_inregion = np.logical_and(lons > bbox[0], lons < bbox[2])
        lats_inregion = np.logical_and(lats > bbox[1], lats < bbox[3])
        inregion = np.logical_and(lons_inregion, lats_inregion)

        region_inds = np.where(inregion)
        imin, imax = minmax(region_inds[0])
        jmin, jmax = minmax(region_inds[1])
        return cube[..., imin:imax+1, jmin:jmax+1]

    sst_sub = bbox_extract_2Dcoords(sst_d, bbox)

    print sst_sub
```

    sea_surface_temperature / (degC)    (time: 1; -- : 209; -- : 199)
         Dimension coordinates:
              time                           x       -         -
         Auxiliary coordinates:
              date                           x       -         -
              latitude                       -       x         x
              longitude                      -       x         x
         Attributes:
              Conventions: CF-1.0
              experiment: 90.9
              history: archv2ncdf2d
              institution: National Centers for Environmental Prediction
              source: HYCOM archive file
              title: HYCOM ATLb2.00


As a reminder, we can collapse a dimension using a mathematical operation rather than just index it using numpy array slicing/indexing notation. Thus, we can quickly whip up a view of the sub-sliced SST data:


``` language-python
    sst_proc = sst_sub.collapsed('time', iris.analysis.MEAN)
    #print sst_proc.shape

    plt.imshow(sst_proc.data[::-1])
```

![png]({static}/images/2015/07/SST_data_27_2.png)


What's especially nice now is that we have a much simpler X-Y/lat-lon coordinate system that doesn't deal with seams across the prime meridian or equator. So we don't even have to re-project our data! We can just plot it using the normal `matplotlib` routines. Below is an example of leveraging `cartopy`/`matplotlib` to build production-quality cartographic images.

``` language-python
    # Extra imports for annotating our map/plot
    from cartopy.feature import NaturalEarthFeature, COLORS
    from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

    # Control feature/boundary resolution
    FEATURE_RES = '50m' # '10m' or '110m'

    # Extract the data and coordinate system, masking any invalid
    # data points for convenience
    sst_proc.data = np.ma.masked_invalid(sst_proc.data)
    lon = sst_proc.coord('longitude').points
    lat = sst_proc.coord('latitude').points

    # Set up the plotting canvas
    fig = plt.figure()
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree())

    # Set map extent
    ax.set_extent([bbox[0], bbox[2], bbox[1], bbox[3]])

    # Add land political boundaries to map
    land_data = NaturalEarthFeature('physical', 'land', FEATURE_RES,
                                    edgecolor='face', # edgecolor == facecolor
                                    facecolor=COLORS['land']) # a nice default
    states = NaturalEarthFeature('cultural',
                                 'admin_1_states_provinces',
                                 FEATURE_RES,
                                 edgecolor='grey', facecolor='none')
    ax.add_feature(land_data)
    ax.add_feature(states)
    ax.coastlines(resolution=FEATURE_RES, lw=1.15)

    # Add some gridlines and use cartopy's convenience functions
    # for formatting them
    # Note - disabled for now, just change 'color' to enable
    grid_style = dict(color='none', linestyle='-', lw=1.5)
    gl = ax.gridlines(draw_labels=True, **grid_style)
    gl.xlabels_top = gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    label_style = dict(size=11, color='black', weight='regular',
                       family='serif')
    gl.xlabel_style = gl.ylabel_style = label_style

    # Plot the actual data, using the projection system as a coordinate
    # transform (I think this is right?)
    pc = ax.pcolormesh(lon, lat, sst_proc.data, transform=ccrs.PlateCarree(),
                       cmap=sst_palette)
    cbar = fig.colorbar(pc, ax=ax, shrink=0.9)
    cbar.ax.set_ylabel(sst_sub.units, labelpad=15., rotation=-90.,
                       fontdict=dict(size=12, weight='bold'))

    ax.set_title("SST data from HYCOM/RTOFS", loc='left',
                 fontdict=dict(size=12, weight='bold'))

```

![png]({static}/images/2015/07/SST_data_30_1.png)
