Title: Simple Ray Tracer in NumbaPro-CUDA
Slug: simple-ray-tracer-in-numbapro-cuda
Date: 2015-06-11 22:07
Modified: 2015-07-03 13:26
Authors: Daniel Rothenberg
 
For a long time, I've been looking for a good application of CUDA/GPGPU programming to some of the basic analysis I do in my research. Unfortunately, there really hasn't ever been any low-hanging fruit. That coupled with my desire to avoid pure C-programming at all costs was an ideal combination for avoiding learning the CUDA basics!

That all changed last week and I decided to dive into things by working through [CUDA by Example]. As an added bonus, I decided to port everything I learned to Python using [NumbaPro](http://docs.continuum.io/numbapro/), which enables extensions for very easily compiling CUDA kernels. 

One of the really neat little projects in [CUDA by Example] is a simple ray tracer viewing a scene with random spheres:

![Random spheres!]({filename}/images/2015/06/ray_C.png)

The thing is *bleeding* fast on a GPU, but is so unbearably slow on a CPU (using a naive algorithm) that it's not worth attempting[^1]. It turns out, it's nearly as fast using NumbaPro and its CUDA/GPU extensions, and just as easy to write.

### Porting to Python

We start with a simple data structure for encapsulating information for each of our spheres. The easiest way to bind such a structure from the CPU->GPU in Python is a NumPy record array using a user-defined datatype:

```language-python
Sphere = np.dtype([
    # RGB color values (floats from [0, 1])
    ('r', 'f4'),  ('g', 'f4'), ('b', 'f4'), 
    # sphere radius 
    ('radius', 'f4'),
    # sphere (x, y, z) coordinates 
    ('x', 'f4'),  ('y', 'f4'), ('z', 'f4'),], align=True) 
Sphere_t = numbapro.from_dtype(Sphere)
```

The only fancy thing we have to do here is bind our `Sphere` type to something Numba recognizes via the last line; the rest of the Sphere data should be self-explanatory. 

Two helper functions will come in handy in our calculation. First, it would be nice to have a function that computes whether or not a ray starting at (x, y) actually hits a given sphere. We write a `hit()` method compute this:

```language-python
def hit(ox, oy, sph):
    """ Compute whether a ray parallel to the z-axis originating at 
    (ox, oy, INF) will intersect a given sphere; if so, return the 
    distance to the surface of the sphere.
    """
    dx = ox - sph.x
    dy = oy - sph.y
    rad = sph.radius
    if ( dx*dx + dy*dy < rad*rad ):
        dz = sqrt( rad*rad - dx*dx - dy*dy )
        return dz + sph.z
    else:
        return -INF
```

Note that we use an attribute syntax to get `Sphere` data, rather than a `dict`-like lookup. This is an idiosyncrasy of Numba. To turn this into a function that runs on the GPU, we annotate it with a decorator from NumbaPro, `@cuda.jit(restype=float32, argtypes=[float32, float32, Sphere_t], device=True, inline=True)`. This just tells NumbaPro to create a function which returns a float given three inputs: two floats and one `Sphere`. We then tell it to compile this function to run specially on the GPU.

Now, we need a function that iterates over *all* of the spheres to compute potential intersections at each observer pixel. This is the core 'kernel' which we'll run on the GPU, and it would look something like this:

``` language-python
@cuda.jit(argtypes=(Sphere_t[:], int16[:,:,:]))
def kernel(spheres, bitmap):
    
    x, y = cuda.grid(2) # alias for threadIdx.x + ( blockIdx.x * blockDim.x ),
                        #           threadIdx.y + ( blockIdx.y * blockDim.y )
    # shift the grid to [-DIM/2, DIM/2]
    ox = x - DIM/2
    oy = y - DIM/2

    r = 0. 
    g = 0.
    b = 0.
    maxz = -INF

    i = 0 # emulate a C-style for-loop, exposing the idx increment logic
    while (i < SPHERES):
        t = hit(ox, oy, spheres[i])
        rad = spheres[i].radius

        if (t > maxz):
            dz = t - spheres[i].z # t = dz + z; inverting hit() result
            n = dz / sqrt( rad*rad )
            fscale = n # shades the color to be darker as we recede from 
                       # the edge of the cube circumscribing the sphere

            r = spheres[i].r*fscale
            g = spheres[i].g*fscale
            b = spheres[i].b*fscale
            maxz = t
        i += 1

    # Save the RGBA value for this particular pixel
    bitmap[x,y,0] = int(r*255.)
    bitmap[x,y,1] = int(g*255.)
    bitmap[x,y,2] = int(b*255.)
    bitmap[x,y,3] = 255
```

There's nothing fancy going on here. NumbaPro gives us an alias (`cuda.grid()`) to the prototypical thread-index lookup mathematics we'd normally undertake. The way we've designed the kernel, a different thread on the GPU will compute the ray trace for each observer pixel in our image. It's virtually identically to the logic we'd use in pure CUDA. One difference is that we can take advantage of the fact our image data-structure is a 2D array (ignoring the RGBA dimension), and directly associate threads with a particular address in that array, rather than use linear offsets.

Just like in pure CUDA, we need to manage data transfers between host and device. For instance, we can initialize some device memory for working with our resulting image and storing our Spheres:

``` language-python
    # Create a container for the pixel RGBA information of our image
    bitmap = np.zeros([DIM, DIM, 4], dtype=np.int16)
   
    # Copy to device memory 
    d_bitmap = cuda.to_device(bitmap)
    # Create empty container for our Sphere data on device
    d_spheres = cuda.device_array(SPHERES, dtype=Sphere_t)

    # Create an empty container of spheres on host
    temp_spheres = np.empty(SPHERES, dtype=Sphere_t)
    # ... sphere creation steps ...
    # Copy the sphere data to the device
    cuda.to_device(temp_spheres, to=d_spheres) 
```

The command for `bitmap` is similar to a `malloc` and assignment all in one. To initialize `d_bitmap` on the device, we can just copy over `bitmap`. Then we call a command similar to `cudaMalloc` to ready an array to contain our sphere data. Finally, we initialize `temp_spheres` on the host like using `malloc`,  populate it, and explicitly copy it to device into the memory already assigned for it.

At this point, the device has all the data we need to run the calculation, so we do can go ahead and call the `kernel`:

``` language-python
    grids = (DIM/16, DIM/16)
    threads = (16, 16)

    # Execute the kernel
    kernel[grids, threads](d_spheres, d_bitmap)

    # Copy the result from the kernel ordering the ray tracing back to host
    bitmap = d_bitmap.copy_to_host()
```

In the first two commands, we set up a grid of (DIM/16 x DIM/16) blocks, each with an array of (16 x 16) threads. If DIM is a reasonable power of 2, this will totally cover the image with one thread for each pixel. On my GeForce GTX 750ti, I can successfully compute images with DIM <= 2**14 before I run out of memory[^2]. Executing the kernel with this grid configuration is just like using the `<<< >>>` notation in CUDA, except we use brackets here and call the function with its arguments like normal. In the final step, we copy the resulting calculation from disk memory back to the host.

Then, we can render our image using matplotlib:

``` language-python
    bitmap = np.transpose(bitmap/255., (1, 0, 2)) # swap image's x-y axes
    plt.imshow(bitmap)
```

and voila!

![Spheres in Python rendered via CUDA!]({filename}/images/2015/06/ray_py-1.png)

Amazingly, the NumbaPro-generated CUDA solution performs within a factor of 2 against the original CUDA implementation, including memory transfers. That's pretty amazing considering it's doing everything automatically!

Full code for this toy project is available as a [gist](https://gist.github.com/darothen/f53bb3e40edbceb38904).

---

<!--Footnotes-->
[^1]: You can see in the full code that we compute vertical rays from +/- scene Z-infinity for each pixel. We could easily improve on this by pre-computing the x-y coverage of the sphere ensemble and only compute rays for pixels we *know* will intercept a sphere, and then only sample the top "layer" of spheres by inspecting their z-position and radii.
[^2]: And this is just using a simple algorithm where we compute the whole image simultaneously! We could probably chunk it and compute even larger scenes.

<!--Bookmarks-->
[CUDA by Example]: http://www.amazon.com/CUDA-Example-Introduction-General-Purpose-Programming/dp/0131387685
