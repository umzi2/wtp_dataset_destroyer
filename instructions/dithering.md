```json 
    {
      "type": "dithering",
      "dithering_type":["floydsteinberg", "jarvisjudiceninke", "stucki", "atkinson", "burkes", "sierra", "tworowsierra", "sierraLite", "order", "riemersma", "quantize"],
      "color_ch": [2,10],
      "map_size":  [2,4,8,16],
      "history": [10, 15],
      "ratio": [0.1,0.9],
      "probability": 0.5
    }
```
`*` = optional parameters

- `dithering_type`* - The list of dithering algorithms to use. One is randomly picked per image
- `color_ch`* - The number of colors per channel. Valid range is `[2,255]`
- `map_size`* - The kernel size is used only for the `order` dithering algorithm
- `history`* - Used for `riemersma`. Uses `[low,high]` 2-inf
- `ratio`* - Used for `riemersma`. Uses `[low,high]` 0.001-0.999
- `probability`* - The chance of applying (e.g. 0.5 = 50% chance of being applied)
## Examples:
all color_ch = 8
<div> Raw</div>
<img src="images/dithering/raw.png" title="raw_img">
<div> Quantize</div>
<img src="images/dithering/quantize.png" title="quantize_img">
<div> SierraLite</div>
<img src="images/dithering/sierraLite.png" title="sierraLite_img">
<div> Jarvisjudiceninke</div>
<img src="images/dithering/jarvisjudiceninke.png" title="jarvisjudiceninke_img">
<div> sierra</div>
<img src="images/dithering/sierra.png" title="sierra_img">
<div> Stucki</div>
<img src="images/dithering/stucki.png" title="stucki_img">
<div> Tworowsierra</div>
<img src="images/dithering/tworowsierra.png" title="tworowsierra_img">
<div> Atkinson</div>
<img src="images/dithering/atkinson.png" title="atkinson_img">
<div> Floydsteinberg</div>
<img src="images/dithering/floydsteinberg.png" title="floydsteinberg_img">
<div> Burkes</div>
<img src="images/dithering/burkes.png" title="burkes_img">
<div> Order map_size: 8</div>
<img src="images/dithering/order.png" title="order_img">
<div> Riemersma history: 10 ratio: 0.5</div>
<img src="images/dithering/riemersma.png" title="riemersma_img">


