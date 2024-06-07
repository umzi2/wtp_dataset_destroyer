```json
    {
      "type": "pixelate",
      "size": [0, 10],
      "probability": 0.9
    }
```
`*` = optional parameters

- `size` - the degree of pixelation accepts an array `[low, high]`. It is important to note that it works not with int sizes, but with float.
- `probability`* - The chance of applying (e.g. 0.5 = 50% chance of being applied)
## Examples 1:
### all alpha: 0.5
<div> Raw</div>
<img src="images/pixelate/raw.png" title="raw_img">
<div> Size 10 </div>
<img src="images/pixelate/size_10.png" title="size_img">