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
  "gray": false
  "gray_or_color":true
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
- `gray_or_color`* - Reads images in RGB, then determines the gradation of the gray image or rgb does not make sense when gray is enabled
