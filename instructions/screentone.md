```json
{
  "type": "screentone",
  "lqhq": false,
  "dot_size": [
    7
  ],
  "color": {
    "type_halftone": [
      "rgb",
      "cmyk",
      "gray",
      "not_rot"
    ],
    "c": [
      -45,
      45
    ],
    "m": [
      -45,
      45
    ],
    "y": [
      -45,
      45
    ],
    "k": [
      -45,
      45
    ],
    "r": [
      -45,
      45
    ],
    "g": [
      -45,
      45
    ],
    "b": [
      -45,
      45
    ],
    "cmyk_alpha": [
      0.5,
      1.0
    ]
  },
  "probability": 0.5
}
```
- color* - settings in case the image is 3-dimensional i.e. rgb
  - type_halftone* - sheet from which a random halftone algorithm is chosen
  - c..k and r..b* - accepts a list for each channel in [low, high] format. A random number will be selected in this range to be used for channel rotation.
  - cmyk_alpha* - transparency of cmyk halftones is necessary to get closer to real comics list[uint, uint]
- dot_size - size of points accepts a list
- lqhq* - equates hq to lq, assuming screentone is first in line
- probability* - chance of triggering
