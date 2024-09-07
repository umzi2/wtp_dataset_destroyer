```json
{
  "type":"canny",
  "thread1" : [10,150,1],
  "thread2": [10,100,1],
  "aperture_size":[3,5],
  "white": 0.5,
  "lq_hq": true,
  "probability": 0.5
}
```
- `thread1`* - Range for the first threshold of the Canny edge detector, specified as [low, high, step]. Values within this range will be used as possible thresholds. `Defaults` to [10, 150, 1], meaning values from 10 to 150 with a step of 1.
- `thread2`* -  Range for the second threshold of the Canny edge detector, specified as [low, high, step]. Values will be added to the value of thread1. `Defaults` to [10, 100, 1], meaning values from 10 to 100 with a step of 1.
- `aperture_size`* - List of possible values for the aperture size of the Sobel operator. `Defaults` to [3, 5].
- `white`* - Probability of replacing detected edges with a white background. `Defaults` to 0.0.
- `probability`* - Probability of applying the Canny edge detection. `Defaults` to 1.0.
- `lq_hq`* - If True, use the processed low-quality image as the high-quality image. `Defaults` to False.
<div> Raw</div>
<img src="images/canny/raw.png" title="raw_img">
<div> canny thread1 = 150 thread2 = 100 aperture_size = 3 white = 0</div>
<img src="images/canny/canny_150_100_3.png" title="canny_150_100_3">
<div> canny thread1 = 150 thread2 = 100 aperture_size = 3 white = 1</div>
<img src="images/canny/canny_white_150_100_3.png" title="canny_white_150_100_3">