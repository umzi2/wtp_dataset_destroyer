```hcl
degradation {
  type = "saturation"
  rand = [0.5,1.0]
  probability = 0.5
}
```
`*` = optional parameters

### Parameters
- `rand`* - Controls color saturation level
  - Format: [min, max]
  - Default: [0.5, 1.0]
  - Range: 0.0-1.0
  - Example: [0.1,0.9] means:
    - Values randomly chosen between 0.1-0.9
    - 0.0 = Complete grayscale
    - 0.5 = Half saturation
    - 1.0 = Full original saturation
  - Lower values create faded/washed-out look

- `probability`* - Chance of applying effect
  - Default: 1.0
  - Range: 0.0 to 1.0
  - No effect on grayscale images

## Examples:
<div> Raw</div>
<img src="images/saturation/raw.png" title="raw_img">
<div> Rand 2</div>
<img src="images/saturation/rand_2.png" title="rand_2_img">
<div> Rand 0.5</div>
<img src="images/saturation/rand_0_5.png" title="rand_0_5_img">
