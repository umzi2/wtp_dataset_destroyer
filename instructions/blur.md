```json
{
    "type": "blur",
    "filter": ["box", "gauss", "median", "lens", "motion", "random"],
    "kernel": [0, 1],
    "target_kernel": {
      "box": [0,2],
      "gauss": [0,2],
      "median": [0,1],
      "lens": [1,2],
      "random": [0,2]
    },
    "motion_size": [1,10],
    "motion_angle": [-30,30],
    "probability": 0.5
}
```

`*` = optional parameters

### Basic Parameters
- `filter` - List of blur algorithms to choose from. One is randomly selected per image
- `probability`* - Chance of applying the blur effect (e.g., 0.5 = 50% chance)

### Kernel Settings
- `kernel`* - Default kernel size range for all blur types: [min, max]
   - Used only when `target_kernel` is not specified for a blur type
   - All types except median blur support float numbers
   - Median blur requires odd integers

- `target_kernel`* - Specific kernel size ranges for each blur type:
  - `box`: Box blur kernel range
  - `gauss`: Gaussian blur kernel range
  - `median`: Median blur kernel range (must be odd integers)
  - `lens`: Lens blur kernel range
  - `random`: Random kernel blur range

### Motion Blur Settings
- `motion_size`* - Length of motion blur effect: [min, max]
  - Default: [1, 2]
- `motion_angle`* - Angle of motion blur in degrees: [min, max]
  - Default: [0, 1]

### Available Blur Types
1. `box` - Simple averaging blur
2. `gauss` - Gaussian blur for smooth, natural-looking effects
3. `median` - Removes noise while preserving edges
4. `lens` - Simulates camera lens blur
5. `motion` - Simulates movement blur
6. `random` - Uses randomly generated kernel

## Examples:


  <div> Raw</div>
  <img src="images/blur/raw.png" alt="raw" title="raw_img">
  <div> Box kernel: 2</div>
  <img src="images/blur/box_2.png" alt="box_2" title="box_img">
  <div> Gauss kernel: 2</div>
  <img src="images/blur/gauss_2.png" alt="gauss_2" title="gauss_img">
  <div> Lens kernel: 2</div>
  <img src="images/blur/lens_2.png" alt="lens_2" title="lens_img">
  <div> Median kernel: 3</div>
  <img src="images/blur/median_3.png" alt="median_3" title="median_img">
  <div> Motion size: 10, angle 30</div>
  <img src="images/blur/motion_10_30.png" alt="motion_10_30" title="motion_img">
