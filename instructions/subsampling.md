```json
{
  "type":"subsampling",
  "down": ["box", "hamming", "linear",  "lagrange", 
           "cubic_catrom", "cubic_mitchell", "cubic_bspline",
           "lanczos", "gauss"],
  "up": ["box", "hamming", "linear",  "lagrange",  
         "cubic_catrom", "cubic_mitchell", "cubic_bspline",
         "lanczos", "gauss"],
  "sampling": ["4:4:4", "4:2:2", "4:2:1", "4:1:1", "4:2:0", "4:1:0", "3:1:1"],
  "yuv": ["601","709","2020"],
  "blur": [0.0,4],
  "probability": 0.5

}
```
`*` = optional parameters

* `down`* - reduction filters `default: nearest`
* `up`* - magnification filters `default: nearest`
* `sampling`* - subsampling format, more details at [wikipedia]( https://en.wikipedia.org/wiki/Chroma_subsampling)`default: 4:4:4`
* `yuv`* - YUV standard, if you repeat whs then it is 601 `default: 601`
* `blur`* - degree of blur of chroma channels `default: None`
* `probability`* - The chance of applying (e.g. 0.5 = 50% chance of being applied) `default: 1`

