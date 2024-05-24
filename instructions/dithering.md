```json 
{
  "type": "dithering",
  "dithering_type": [
    "floydsteinberg",
    "jarvisjudiceninke",
    "stucki",
    "atkinson",
    "burkes",
    "sierra",
    "tworowsierra",
    "sierraLite",
    "order",
    "riemersma",
    "quantize"
  ],
  "color_ch": [
    2,
    10
  ],
  "map_size": [
    2,
    4,
    8,
    16
  ],
  "history": [
    10,
    15
  ],
  "ratio": [
    0.1,
    0.9
  ],
  "probability": 0.5
}

```
- dithering_type* - sheet from which a random dithering and quantization algorithm is chosen 
- color_ch* - number of colors per channel
- map_size* - kernel size is used only for order dithering, it accepts a sheet from which a random size is selected.
- history* - applicable for riemersma sheet [low,high] 2-inf
- ratio* - applicable for riemersma sheet [low,high] 0.001-0.999
- probability* - chance of triggering