```json
{
  "type": "sin",
  "shape": [100,1000,100],
  "alpha": [0.1,0.5],
  "bias": [0.8,1.2],
  "vertical": 0.5,
  "probability": 0.5
}
```
### Parameters
- `shape`* - Controls sinusoidal pattern frequency
  - Format: [min, max, step]
  - Default: [100, 1000, 100]
  - Example: [100,1000,100] means:
    - Values: 100, 200, 300, ..., 1000
    - Lower values = wider waves
    - Higher values = tighter waves
  - Affects pattern density

- `alpha`* - Controls pattern intensity
  - Format: [min, max]
  - Default: [0.1, 0.5]
  - Range: 0.0-1.0
  - Lower values = subtle effect
  - Higher values = stronger effect

- `bias`* - Controls pattern brightness
  - Format: [min, max]
  - Default: [0.8, 1.2]
  - Values < 1.0 darken the pattern
  - Values > 1.0 brighten the pattern

- `vertical`* - Controls pattern orientation
  - Default: 0.5
  - Range: 0.0-1.0
  - Higher values = more likely vertical
  - Lower values = more likely horizontal

- `probability`* - Chance of applying effect
  - Default: 1.0
  - Range: 0.0 to 1.0

## Examples:
### all shape = 200  alpha = 0.3
<div> raw</div>
<img src="images/sin/raw.png" title="raw_img">
<div> sin</div>
<img src="images/sin/sin.png" title="sin_img">
<div> sin_vertical</div>
<img src="images/sin/sin_vertical.png" title="sin_vertical_img">
<div> sin_bias_0_5</div>
<img src="images/sin/sin_bias_0_5.png" title="sin_bias_0_5_img">
<div> sin_bias_-0_5</div>
<img src="images/sin/sin_bias_-0_5.png" title="sin_bias_-0_5_img">
