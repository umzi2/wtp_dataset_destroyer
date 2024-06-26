```json
  {
    "type": "color",
    "high": [240,255],
    "low": [0,15],
    "gamma": [0.9,1.1]
  }
```

`*` = optional parameters

- `low`* - Shifts the minimum color level of the image. Uses `[low,high]`
- `high`* - Shifts the maximum color level of the image. Uses `[low,high]`
- `gamma`* - Shifts the gamma of each image. Uses `[low, high]`
- `probability`* - The chance of applying (e.g. 0.5 = 50% chance of being applied)
## Examples:


<div> Raw</div>
<img src="images/color/raw.png" title="raw_img">
<div> Low 100</div>
<img src="images/color/out_low_100.png" title="low_img">
<div> High 150</div>
<img src="images/color/out_high_150.png" title="high_img">
<div> Gamma 3</div>
<img src="images/color/gamma_3.png" title="gamma_img">



