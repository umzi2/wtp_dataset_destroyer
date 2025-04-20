```hcl
degradation {
  type = "noise"
  type_noise = ["perlinsuflet", "perlin", "opensimplex", "simplex",
    "supersimplex","uniform","salt","salt_and_pepper","pepper","gauss"]
  clip = [0.3,0.5]
  normalize = true
  y_noise = 0.3
  uv_noise = 0.3
  alpha = [0.01,0.5,0.01]
  scale {
    size = [1, 2]
    sigma = [1, 2]
    amount = [1, 3]
    probability = 0.4
  }
  motion {
    size = [1, 3]
    angle = [1, 360]
    sigma = [0,1]
    amount = [0,1]
    probability = 0.4
  }
  octaves = [1,10,1]
  frequency = [0.1,0.9,0.1]
  lacunarity = [0.01,0.5,0.01]
  probability_salt_or_pepper = [0,0.02]

  bias =  [-0.5, 0.5]
  probability =  1
}
```
`*` = optional parameters

### Basic Parameters
- `type` - The type of noise to apply. One is randomly selected from the list for each image
- `alpha`* - Controls noise intensity. Format: [min, max, step]
- `probability`* - Chance of applying the noise effect (e.g., 0.5 = 50% chance)
- `clip`* - Restricts noise to areas where image values are between [min, max]
- `bias`* - Offset added to noise values. Range: [-1, 1]
### Scale*
- `size`* - degree of increase in gauss or uniform noise.
- `sigma`* - Sharping size
- `amoiunt`* - Sharpe power
- `probability`* - Chance of applying scale (e.g., 0.5 = 50% chance)
### Motion*
- `size`* - Length of motion blur effect
- `angle`* - Angle of motion blur 
### Channel Control
- `y_noise`* - Probability of applying noise only to luminance (Y channel)
- `uv_noise`* - Probability of applying noise only to chrominance (UV channels)
- `sigma`* - Sharping size
- `amoiunt`* - Sharpe power
- `probability`* - Chance of applying scale (e.g., 0.5 = 50% chance)
### Procedural Noise Parameters
(For "perlinsuflet", "perlin", "opensimplex", "simplex", "supersimplex")
- `normalize`* - Normalizes noise to range [-1, 1]
- `octaves`* - Number of noise layers to combine. Format: [min, max, step]
- `frequency`* - Controls noise pattern size. Format: [min, max, step]
  - Lower values create larger patterns, higher values create finer details
- `lacunarity`* - Controls frequency change between octaves. Format: [min, max, step]
  - Higher values create more detail in subsequent octaves

### Salt and Pepper Parameters
(For "salt", "pepper", "salt_and_pepper")
- `probability_salt_or_pepper`* - Percentage of pixels affected by the noise
  - For "salt": pixels set to 1 (white)
  - For "pepper": pixels set to 0 (black)
  - For "salt_and_pepper": pixels randomly set to either 0 or 1

## Examples 1:
### all alpha: 0.5
<div> raw</div>
<img src="images/noise/raw.png" title="raw_img">
<div> uniform</div>
<img src="images/noise/uniform.png" title="uniform_img">
<div> gauss</div>
<img src="images/noise/gauss.png" title="gauss_img">

### all octaves: 10 frequency: 0.5 lacunarity: 0.5
<div> perlinsuflet</div>
<img src="images/noise/perlinsuflet.png" title="perlinsuflet_img">
<div> opensimplex</div>
<img src="images/noise/opensimplex.png" title="opensimplex_img">
<div> perlin</div>
<img src="images/noise/perlin.png" title="perlin_img">
<div> simplex</div>
<img src="images/noise/simplex.png" title="simplex_img">
<div> supersimplex</div>
<img src="images/noise/supersimplex.png" title="supersimplex_img">

### all probability_salt_or_pepper: 0.05
<div> salt</div>
<img src="images/noise/salt.png" title="salt_img">
<div> pepper</div>
<img src="images/noise/pepper.png" title="pepper_img">
<div> salt_and_pepper</div>
<img src="images/noise/salt_and_pepper.png" title="salt_and_pepper_img">

## Examples 2:
### all alpha = 0.5
<div> uniform y_noise = 1.0</div>
<img src="images/noise/uniform_y.png" title="uniform_y_img">
<div> uniform uv_noise = 1.0</div>
<img src="images/noise/uniform_uv.png" title="uniform_uv_img">
