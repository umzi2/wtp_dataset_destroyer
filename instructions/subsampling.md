```hcl
{
degradation {
  type = "subsampling"
  down = ["box", "nearest", "linear",  "lagrange", "cubic_catrom", "cubic_mitchell", "cubic_bspline",
    "lanczos", "gauss"]
  up = ["box",  "linear", "nearest", "lagrange", "cubic_catrom", "cubic_mitchell", "cubic_bspline",
    "lanczos", "gauss"]
  sampling = ["4:4:4", "4:2:2", "4:2:1", "4:1:1", "4:2:0", "4:1:0", "3:1:1"]
  yuv = ["601","709","2020"]
  blur = [0.0,4]
  probability = 0.5
}
```

### Basic Parameters
- `down`* - Downscaling algorithms for color channels
  - Default: ["nearest"]
  - Options:
    - "nearest": Fast but blocky
    - "bilinear": Smooth but can blur
    - "bicubic": Best quality but slower
  - One algorithm randomly selected per image

- `up`* - Upscaling algorithms for color channels
  - Default: ["nearest"]
  - Same options as `down`
  - Different up/down combinations create unique artifacts

### Color Settings
- `sampling`* - Chroma subsampling formats
  - Default: ["4:4:4"]
  - Options:
    - "4:4:4": No subsampling (full quality)
    - "4:2:2": Half horizontal chroma resolution
    - "4:2:0": Quarter chroma resolution
    - "4:1:1": Quarter horizontal chroma resolution
  - Lower ratios = more color artifacts

- `yuv`* - YUV color space standard
  - Default: ["601"]
  - Options:
    - "601": Standard for SD content (BT.601)
    - "709": Standard for HD content (BT.709)
    - "2020": Standard for UHD content (BT.2020)
  - Affects color conversion accuracy

### Enhancement
- `blur`* - Optional blur kernel size
  - Format: [min, max]
  - Default: None (no blur)
  - Must be odd numbers
  - Larger values create more blur
  - Helps reduce subsampling artifacts

- `probability`* - Chance of applying effect
  - Default: 1.0
  - Range: 0.0 to 1.0
