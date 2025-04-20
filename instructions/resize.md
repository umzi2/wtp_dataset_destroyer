```hcl
degradation {
  type = "resize"
  alg_lq = ["box", "hermite", "linear", "lagrange", "cubic_catrom", "cubic_mitchell", "cubic_bspline",
    "lanczos", "gauss", "down_up", "down_down", "up_down"]
  alg_hq = ["lagrange"]
  down_up = {
    down = [1, 2]
    alg_up = ["nearest", "box", "hermite", "linear", "lagrange", "cubic_catrom", "cubic_mitchell",
      "cubic_bspline", "lanczos", "gauss", "down_down"]
    alg_down = [ "hermite", "linear",  "lagrange", "cubic_catrom", "cubic_mitchell", "cubic_bspline",
      "lanczos", "gauss"]
  }
  up_down = {
    up = [1, 2]
    alg_up = ["nearest", "box", "hermite", "linear", "lagrange", "cubic_catrom", "cubic_mitchell",
      "cubic_bspline", "lanczos", "gauss"]
    alg_down = [ "hermite", "linear",  "lagrange", "cubic_catrom", "cubic_mitchell", "cubic_bspline",
      "lanczos", "gauss","down_down"]
  }
  down_down = {
    step = [1, 6]
    alg_down = [ "linear", "lagrange", "cubic_catrom", "cubic_mitchell", "cubic_bspline"]
  }
```

### Basic Parameters
- `spread`* - Controls the resolution reduction range
  - Format: [min, max, step]
  - Default: [1, 1, 1]
  - Example: [1, 4, 1] means:
    - For HQ image of size 512x512 and scale=4:
    - Original LQ would be 128x128
    - With spread, LQ size can vary from 128x128 to 32x32
    - Step of 1 means it can be 128, 96, 64, or 32
  - Larger spread values create more aggressive downscaling

- `probability`* - Controls how often resize is applied
  - Default: 1.0 (always apply)
  - Range: 0.0 to 1.0
  - Example: 0.5 means 50% chance to apply resize


### Algorithm Selection
- `alg_lq` - Algorithms for low quality image. One is randomly picked per image
- `alg_hq` - Algorithms for high quality image. One is randomly picked per image
- `scale` - Base scaling factor
### Up-Down Resize
- `up_down` - This algorithm increases the resolution of the image through resizing, then downsizes it again.
- `up` - Scale range for up-down
- `alg_up` - Upscaling algorithms
- `alg_down` - Downscaling algorithms
### Down-Up Resize
- `down_up` - This algorithm reduces the resolution of an image by resizing it and then increases its size again.
- `down` - Scale range for down-up
- `alg_up` - Upscaling algorithms
- `alg_down` - Downscaling algorithms

### Down-Down Resize
- `down_down` - This algorithm downsizes an image through resizing, then downsizes it again.
- `step` - Scale step size
- `alg` - Downscaling algorithms

### Options
- `color_fix`* - Fix colors after resize
- `gamma_correction`* - Apply gamma correction
- `olq`* - Only resize low quality image

## Examples:
<div> Raw</div>
<img src="images/resize/raw.png" title="raw_img">
<div> Box scale = 4</div>
<img src="images/resize/box_4.png" title="box_img">
