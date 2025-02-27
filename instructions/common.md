```hcl
input = "path/to/input"
output = "path/to/output"
degradation {}...
tile = {
  size = 512
  no_wb = true
}
num_workers = 16
map_type = "thread"
laplace_filter = 0.02
size = 1000
shuffle_dataset = true
gray = false
gray_or_color = true
debug = false
only_lq = false
real_name = false
out_clear = true
```

# Common Parameters and Concepts

## Parameter Formats

### Ranges
Many effects use range formats for randomization:
- `[min, max]`: Random value between min and max
- `[min, max, step]`: Random value between min and max in steps
  - Example: [1, 5, 2] means choose from [1, 3, 5]

### Probabilities
- All effects support `probability`
- Format: 0.0 to 1.0
  - 0.0 = Never apply
  - 0.5 = 50% chance
  - 1.0 = Always apply
- Default: 1.0 if not specified

### Color Spaces
Several effects work in different color spaces:
1. RGB (Red, Green, Blue)
   - Standard color space
   - Each channel 0-255
   - Used by most effects

2. YUV/YCbCr
   - Y: Brightness
   - U/Cb: Blue difference
   - V/Cr: Red difference
   - Used by: compress, shift, subsampling

3. CMYK
   - C: Cyan
   - M: Magenta
   - Y: Yellow
   - K: Black
   - Used by: screentone, shift

### Image Types
Effects handle different image types:
- Color (RGB/BGR): 3 channels
- Grayscale: 1 channel
- Alpha channel: Preserved if present

### Optional Parameters
- Marked with `*` in documentation
- Have default values
- Can be omitted from configuration

### Effect Order
- Effects are applied in sequence
- Order can affect final result
- Some effects work better early/late in chain

### Examples:
- `input` - input folder
- `output` - output folder (saves new HQ and LQ images)
- `degradation` - The degradations that will be applied to your images
- `num_workers`* - The number of processes for parallel processing. It's best to use your CPU core count
- `map_type`* - Valid processing types: `process`, `thread` and `for`
  - If you run into issues on Windows, swap to `thread`
- `size`* - How many images to process from the input folder 
- `laplace_filter`* - It filters out images based on low saturation using the laplace operator. Accepts a float value. (experiment with it)
- `shuffle_dataset`* - Determines whether or not the images will be shuffled
- `tile`* - This section enables automatic tiling of your images. For example, if you choose `size` 512, it'll split a single image into multiple 512x512 images.  
  - `size` - tile size
  - `no_wb`* - Ignore pure white and pure black images (bool)
- `gray`* - All images are read only in grayscale mode
- `gray_or_color`* - If an image has shades transitioning smoothly from light to dark and all RGB values for each pixel are almost the same, it gets converted to grayscale.
  - This is very performance intensive.
- `debug`* - Creates a `debug` folder if it doesn't exist, and in it creates a `debug.log` file where all random values during degradation processes will be logged. When enabled, it ignores map_type by setting it to `for`.
- `out_clear`* - Cleans the output directory out_path/lq|hq if it exists and contains files. Just to make the tests easier

Doesn't work with tile:
- `only_lq`* - Saves only lq files without hq. `spread` in resize causes discrepancies, so turn it off
- `real_name`* - When saving, the names do not change
