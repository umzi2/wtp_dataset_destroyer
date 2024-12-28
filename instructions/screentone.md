```json
  {
    "type": "screentone",
    "lqhq": false,
    "dot_size": [5,15],
    "color": {
      "type_halftone": ["rgb","cmyk","gray","not_rot","hsv"],
      "c": [15,75],
      "m": [15,75],
      "y": [15,75],
      "k": [15,75],

      "r": [15,75],
      "g": [15,75],
      "b": [15,75],
      "cmyk_alpha": [0.5,1.0],
      "1_ch_dot_type": ["circle"],
      "2_ch_dot_type": ["circle"],
      "3_ch_dot_type": ["circle"],
      "4_ch_dot_type": ["circle"]
    },
    "dot_type": ["circle", "diamond", "line"],
    "angle": [0,90],
    "probability": 0.5
  }
```
`*` = optional parameters

### Basic Parameters
- `dot_size`* - Controls size of screentone pattern
  - Format: [min, max]
  - Default: [7, 7]
  - Larger values create bigger dots/patterns
  - Smaller values create finer details

- `dot_type`* - Controls shape of screentone pattern
  - Default: ["circle"]
  - Options:
    - "circle": Round dots (classic manga style)
    - "diamond": Diamond shapes
    - "line": Linear patterns
  - One type is randomly selected per image

- `angle`* - Controls rotation of pattern
  - Format: [min, max] in degrees
  - Default: [0, 0]
  - Range: 0-360
  - Affects pattern orientation

### Color Settings
- `color`* - These settings apply if the image has 3 channels
- `type_halftone`* - Color separation method
  - Default: ["rgb"]
  - Options:
    - "rgb": Red, Green, Blue separation
    - "cmyk": Cyan, Magenta, Yellow, Black separation

- Channel Angles (c, m, y, k, r, g, b)*
  - Format: [min, max] in degrees
  - Default: [0, 0] for each
  - Controls angle for each color channel
  - Different angles prevent moiré patterns

- `cmyk_alpha`* - CMYK color intensity
  - Format: [min, max]
  - Default: [1.0, 1.0]
  - Range: 0.0-1.0
  - Lower values create lighter colors

- `probability`* - Chance of applying effect
  - Default: 1.0
  - Range: 0.0 to 1.0

### Examples:
### all dot_size = 7
<div> raw</div>
<img src="images/screentone/raw.png" title="raw_img">
<div> not_rot</div>
<img src="images/screentone/not_rot.png" title="not_rot_img">
<div> gray</div>
<img src="images/screentone/gray.png" title="gray_img">
<div> rgb r = -30 g = 0 b = 30 </div>
<img src="images/screentone/rgb.png" title="rgb_img">
<div> cmyk c = -45 m = 30 y = 15 k = 15</div>
<img src="images/screentone/cmyk.png" title="cmyk_img">
<div> cmyk_alpha 0.8</div>
<img src="images/screentone/cmyk_alpha.png" title="cmyk_alpha_img">
