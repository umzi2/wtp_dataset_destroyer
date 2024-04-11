```json
      "blur": {
        "filter": ["box", "gauss", "box", "median"],
        "kernel": [0, 8, 1],
        "median_kernel": [0,3,1],
        "prob": 0.5
      }
```
- filter - blur type
- kernel - blur kernel [low,high,step]
- median_kernel - median blur kernel [low,high,step]
- prob - chance of triggering
