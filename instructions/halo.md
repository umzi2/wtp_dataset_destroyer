```json
      "halo": {
        "sharpening_factor": [0, 2],
        "kernel": [1, 3],
        "laplacian": [1],
        "prob": 0.5
      }
```
- sharpening_factor - sharpness from which we get halo
- kernel - applies median blur with a random kernel [low,high] necessary to reduce artifacts
- laplacian - sheet from which the random kernel size for the Laplace filter is taken
- prob* - chance of triggering
ps This piece from the image to which sharpening was applied takes only the white halo and it comes out at 1 bit, so it’s better to use it before blurring
