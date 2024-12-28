```json
{
  "type": "pixelate",
  "size": [1,10],
  "probability": 0.5
}
```
`*` = optional parameters

### Parameters
- `size`* - Controls pixel block size
  - Format: [min, max]
  - Default: [1, 1]
  - Example: [1,10] means:
    - Original pixels are grouped into blocks
    - Block size varies from 1x1 (no effect) to 10x10
    - Each block becomes a single color (average)
    - Larger values create more obvious "mosaic" effect
  - Values ≤ 1 have no effect
  - Integer values work best

- `probability`* - Chance of applying effect
  - Default: 1.0
  - Range: 0.0 to 1.0

## Examples:
<div> Raw</div>
<img src="images/pixelate/raw.png" title="raw_img">
<div> Size 10 </div>
<img src="images/pixelate/size_10.png" title="size_img">