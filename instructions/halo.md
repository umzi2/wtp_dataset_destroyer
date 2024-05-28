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
`*` = optional parameters

- `type_halo` - The list of halo algorithms to use
- `kernel` - This applies median blur with a random kernel `list[float|int]` (necessary to reduce artifacts)
  - `laplacian`:
    - `sharpening_factor` - Controls the sharpening strength which generates the halo
    - `laplacian` - The range from which the random kernel size for the Laplace filter is taken
  - `unsharp_mask`:
    - `amount` - Strength of the halo
    - `threshold` - Controls the halo threshold
- `probability`* - The chance of applying (e.g. 0.5 = 50% chance of being applied)

Note: It's better to apply this before blurring. It takes only the white halo and it comes out at 1 bit
