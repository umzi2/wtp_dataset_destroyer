```json 
    {
      "type": "dithering",
      "dithering_type":["floydsteinberg", "jarvisjudiceninke", "stucki", "atkinson", "burkes", "sierra", "tworowsierra", "sierraLite", "order", "riemersma", "quantize"],
      "color_ch": [2,10],
      "map_size":  [2,4,8,16],
      "history": [10, 15],
      "ratio": [0.1,0.9],
      "probability": 0.5
    },
}

`*` = optional parameters

```
- `dithering_type`* - The list of dithering algorithms to use. One is randomly picked per image
- `color_ch`* - The number of colors per channel. Valid range is `[2,255]`
- `map_size`* - The kernel size is used only for the `order` dithering algorithm
- `history`* - Used for `riemersma`. Uses `[low,high]` 2-inf
- `ratio`* - Used for `riemersma`. Uses `[low,high]` 0.001-0.999
- `probability`* - The chance of applying (e.g. 0.5 = 50% chance of being applied)
