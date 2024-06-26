```json
    {
      "type": "sin",
      "shape": [100, 1000, 100],
      "alpha": [0.1, 0.5],
      "bias": [-1.0, 1.0],
      "vertical": 0.5,
      "probability": 0.5
    }
```
`*` = optional parameters

- `shape`* - Controls the sinusoidal pattern frequency. `[low, high, step]`
- `alpha`* - Controls how transparent the pattern is when applied to the image
- `bias`* - Pattern displacement.
  - -1 rotates it by -45 degrees
  - 1 rotates it by 45
  - Valid range is -1, 1
- `vertical`* - The chance that the pattern will be vertical rather than horizontal.
  - Coupled with a 90 degree radius. This allows you to make any degree of pattern
- `probability`* - The chance of applying (e.g. 0.5 = 50% chance of being applied)
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

