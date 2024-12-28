{
  "type":"canny",
  "thread1" : [10,150,1],
  "thread2": [10,100,1],
  "aperture_size":[3,5],
  "white": 0.5,
  "lq_hq": true,
  "probability": 0.5
}

### Edge Detection Parameters
- `thread1`* - First threshold for the Canny edge detector
  - Format: [min, max, step]
  - Default: [10, 10, 1]
  - Controls edge sensitivity: lower values detect more edges

- `thread2`* - Second threshold for the Canny edge detector
  - Format: [min, max, step]
  - Default: [0, 10, 1]
  - Must be less than thread1
  - Helps connect edge segments

- `aperture_size`* - Size of the Sobel operator kernel
  - Format: [min, max]
  - Default: [3, 5]
  - Must be odd numbers (3, 5, 7)
  - Larger values detect stronger edges

### Appearance Control
- `white`* - Controls edge appearance
  - Range: 0.0 to 1.0
  - Default: 0.0
  - Probability of showing edges on white background
  - 0.0 = black background
  - 1.0 = white background

### Processing Options
- `probability`* - Chance of applying the effect
  - Range: 0.0 to 1.0
  - Default: 1.0
  - Example: 0.5 = 50% chance

- `lq_hq`* - Output image control
  - Default: false
  - When true: processed image is used for both low and high quality
  - When false: original image is preserved as high quality

### Examples:
<div> Raw</div>
<img src="images/canny/raw.png" title="raw_img">
<div> canny thread1 = 150 thread2 = 100 aperture_size = 3 white = 0</div>
<img src="images/canny/canny_150_100_3.png" title="canny_150_100_3">
<div> canny thread1 = 150 thread2 = 100 aperture_size = 3 white = 1</div>
<img src="images/canny/canny_white_150_100_3.png" title="canny_white_150_100_3">