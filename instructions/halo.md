```json
{
      "type": "halo",
      "type_halo": ["laplacian","unsharp_mask"],
      "kernel": [0,3],
      "sharpening_factor": [0, 2],
      "amount": [0,1],
      "threshold": [0,20]
}    
```
- type_halo - halo overlay algorithm list
- kernel - applies median blur with a random kernel `list[float|int]` necessary to reduce artifacts
- laplacian:
  - sharpening_factor - sharpness from which we get halo
  - laplacian - sheet from which the random kernel size for the Laplace filter is taken
- unsharp_mask:
  - amount - halo force 
  - threshold - halo effect threshold
- probability* - chance of triggering

ps This piece from the image to which sharpening was applied takes only the white halo and it comes out at 1 bit, so it’s better to use it before blurring
