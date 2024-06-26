```json 
  "input": "path/to/input",
  "output": "path/to/output",
  "process":[]
  "tile": {
    "size": 512,
    "no_wb": true
  },
  "num_workers": 16,
  "map_type": "process",
  "laplace_filter": 0.02,
  "size": 1000,
  "shuffle_dataset": true,
  "gray": false,
  "gray_or_color":true,
  "debug": false,
  "only_lq": false,
  "real_name": false,
  "out_clear": true,
```

- `input` - input folder
- `output` - output folder (saves new HQ and LQ images)
- `process` - The degradations that will be applied to your images
- `num_workers`* - The number of processes for parallel processing. It's best to use your CPU core count
- `map_type`* - Valid processing types: `process`, `thread` and `for`
  - If you run into issues on Windows, swap to `thread`
- `size`* - How many images to process from the input folder 
- `laplace_filte`r* - It filters out images based on low saturation using the laplace operator. Accepts a float value. (experiment with it)
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
