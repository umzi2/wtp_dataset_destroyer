```json
    {
      "type": "sin",
      "shape": [100, 1000, 100],
      "alpha": [0.1, 0.5],
      "bias": [0.8, 1.2],
      "vertical": 0.5,
      "probability": 0.5
    }
```
`*` = optional parameters

- `shape`* - Controls the sinusoidal pattern frequency. `[low, high, step]`
- `alpha`* - Controls how transparent the pattern is when applied to the image
- `bias`* - Pattern displacement.
  - -1 rotates it by -45 degrees
  - 1 rotates it by 45
  - Valid range is -1, 1
- `vertical`* - The chance that the pattern will be vertical rather than horizontal.
  - Coupled with a 90 degree radius. This allows you to make any degree of pattern
- `probability`* - The chance of applying (e.g. 0.5 = 50% chance of being applied)
