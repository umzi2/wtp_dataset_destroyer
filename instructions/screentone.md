```json
  {
    "type": "screentone",
    "lqhq": false,
    "dot_size": [7],
    "color": {
      "type_halftone": ["rgb","cmyk","gray","not_rot"],
      "c": [-45,45],
      "m": [-45,45],
      "y": [-45,45],
      "k": [-45,45],

      "r": [-45,45],
      "g": [-45,45],
      "b": [-45,45],
      "cmyk_alpha": [0.5,1.0]
    },
    "probability": 0.5
  }
```
`*` = optional parameters

- `color`* - These setting apply if the image is RGB or otherwise 3 dimensional
  - `type_halftone`* - The list of halftone algorithms from which a random halftone algorithm is chosen
  - `c..k` and `r..b`* - Takes in a value from the `[low, high]` format. A random number will be selected in this range to be used for channel rotation.
  - `cmyk_alpha`* - This controls the transparency of applied cmyk halftones. This is necessary to get closer to real comics list. Accepts `[uint, uint]`
- `dot_size` - Controls the size of generated points. Accepts a range
- `lqhq`* - Equates hq to lq, assuming the screentone is first in line
- `probability`* - The chance of applying (e.g. 0.5 = 50% chance of being applied)
