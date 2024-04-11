```json
      "sin": {
        "shape": [100,1000,100],
        "alpha": [0.1,0.5],
        "bias": [-1.0,1.0],
        "vertical": 0.5,
        "prob": 0.5
      }
```
- shape - sinusoidal pattern frequency [low, high, step]
- alpha - pattern transparency
- bias - Pattern displacement at -1 rotates it by -45 degrees, 1 +45. don't go beyond -1 1
- vertical - the chance that the pattern will be vertical rather than horizontal coupled with a 90 degree radius allows you to make any degree of pattern
- prob - chance of triggering
