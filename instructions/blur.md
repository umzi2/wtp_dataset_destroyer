```json
{
    "type": "blur",
    "filter": ["box", "gauss", "median","lens","motion"],
    "kernel": [0, 1],
    "target_kernel": {
      "box": [0,2],
      "gauss": [0,2],
      "median": [0,1],
      "lens":[1,2]
    },

    "motion_size": [0,10],
    "motion_angle": [-30,30],

    "probability": 0.5
    }
```

standard:
- filter - blur type list
- kernel* - blur kernel list[low,high], in all cases except median blur you can use float. 
- target_kernel* - separate kernel spread for each blur filter 
- probability* - chance of triggering


motion:
- motion_size* - motion blur size takes list[uint, uint]
- motion_angle* - rotate motion blur takes list[int, int]