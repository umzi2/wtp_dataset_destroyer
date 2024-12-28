```json
{
  "type": "color",
  "high": [200,255],
  "low": [0,50],
  "gamma": [0.8,1.2],
  "probability": 0.5
}
```

### Parameters
- `high`* - Controls how bright colors can get
  - Format: [min, max]
  - Default: [255, 255]
  - Range: 0-255
  - Example: [200,255] means:
    - Brightest pixels will be randomly mapped to values between 200-255
    - Creates washed-out or faded appearance
  - Lower values reduce contrast in bright areas

- `low`* - Controls how dark colors can get
  - Format: [min, max]
  - Default: [0, 0]
  - Range: 0-255
  - Example: [0,50] means:
    - Darkest pixels will be randomly mapped to values between 0-50
    - Creates lifted blacks or faded shadows
  - Higher values reduce contrast in dark areas

- `gamma`* - Controls overall image brightness curve
  - Format: [min, max]
  - Default: [1.0, 1.0]
  - Values < 1.0: Makes mid-tones darker
  - Values > 1.0: Makes mid-tones brighter
  - Affects middle brightness more than extremes

- `probability`* - Chance of applying effect
  - Default: 1.0
  - Range: 0.0 to 1.0

## Examples:


<div> Raw</div>
<img src="images/color/raw.png" title="raw_img">
<div> Low 100</div>
<img src="images/color/out_low_100.png" title="low_img">
<div> High 150</div>
<img src="images/color/out_high_150.png" title="high_img">
<div> Gamma 3</div>
<img src="images/color/gamma_3.png" title="gamma_img">
