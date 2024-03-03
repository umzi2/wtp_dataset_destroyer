# Dataset destroer primarily 
designed for web art, is in early beta.
## TODO
* Make more losses.
* Change the structure for more readability.
* Write instructions⏳
# Settings
* = optional parameters 
## image loading settings:
paths:

```json
"input": "/media/umzi/H/датасеты/descreenton/HR",
"output": "/media/umzi/H/датасеты/descreenton/HR2",
```
input - path where files are taken from

output - path where they will be saved 

* tile:
```json
"tile": {
  "size": 512,
  "no_wb": true
}
```
size - size of tiles into which the image will be divided 

no_wb - ignore pure white and pure black tiles

* other:
```json
"gray_or_color": true
"gray": false
```
gray_or_color - since opencv reads images in 3 channels except for the direct instruction, this function simply determines which files are purely grayscale and which are color.
gray - converts all files to grayscale.
## process settings:
```json
"process":{}
```
dictionary containing process settings, also the order of keys depends on the order of execution, i.e. if resize is the first and compress is the last in the dictionary, resize will be the first and compress the last.
```json
    "resize": {
      "alg_lq": ["linear", "catrom", "bspline", "mitchell", "lanczos", "gauss", "down_up", "down_down"],
      "alg_hq": ["catrom"],
      "down_up": {
        "up": [1, 3],
        "alg_up": ["nearest", "linear", "catrom", "bspline", "mitchell", "lanczos", "gauss"],
        "alg_down": ["linear", "catrom", "bspline", "mitchell", "lanczos", "gauss", "down_down"]
      },
      "down_down": {
        "step": 15,
        "alg_down": ["linear", "catrom", "bspline", "mitchell", "gauss"]
      },
      "rand_scale": [1, 2, 0.25],
      "scale": 4
    },
```
alg_lq and alg_hq - list of algorithms from which a random algorithm will be selected, down_down and down_up are custom algorithms, I will tell you more about it further on.
* down_up - algorithm that first enlarges then reduces images, up - list for randrange that randomly selects the image enlargement coefficient. alg_up - enlargement filter cannot include down_down and down_up. alg_down - algorithm of subsequent reduction, it cannot include down_up.  
* down_down - algorithm of image reduction with step. step - up to how many steps can be reduced. alg_down - reduction filter, it can not have down_down and down_up.

rand_scale - list for randrange randomized scatter reduction. I.e. if standard at 2x reduction hq = 512 lq = 256 when setting this parameter you can have a randrange at [1 ,2, 0.25] hq = 512-256 lq = 256-128.

scale - how many times to shrink the image takes only uint values.
```json
    "blur": {
      "filter": ["box", "gauss", "box", "median"],
      "kernel": [0, 6, 1],
      "median_kernel": [0,3,1]
    },
```
filter - list of blur filters, among which a random one will be selected

kernel - list for randrange by which random blur strength will be selected 
* median_kernel - the same as regular kernel, but for median_blure, since it kills scans completely at large kernel size. 
```json
    "halo": {
      "sharpening_factor": [0, 2],
      "kernel_median": [1, 3],
      "box_kernel": [1, 3],
      "laplacian": [1]
    },
```
sharpening_factor - halo power

laplacian - laplacian kernel size, accepts a list from which a random kernel is selected
```json
    "compress": {
      "compress_compress": [1, 3],
      "algorithm": ["jpeg", "webp"],
      "comp": [40, 100]
    }
```
* compress_compress - needed for multiple compression, if this parameter is not present, apply compression 1 time
algorithm - compression algorithm

comp - compressive strength
