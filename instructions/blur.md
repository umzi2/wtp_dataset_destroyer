```json
{
  "type": "blur",
  "filter": ["box", "gauss", "blur", "median","lens","motion"],
  "kernel": [0, 8, 1],
  "target_kernel": {
    "box": [0,2,1],
    "gauss": [0,8,1],
    "blur": [0,8,1],
    "median": [0,1,1]
  },
  
  "lens_radius": [1, 3],
  "lens_components": [3, 6],
  "lens_gamma": [1.0, 5.0],
  
  "motion_size": [0,10],
  "motion_angle": [-30,30],
  
  "probably": 0.5
}
```

standard:
- filter - blur type list
- kernel* - blur kernel list[low,high,step]
- target_kernel* - separate kernel spread for each blur filter 
- probably* - chance of triggering

lens:
- lens_radius* - lens blur radius blur takes list[uint, uint],
- lens_components* - number of lens blur components occupies list[uint, uint]. min 1, max 6,
- lens_gamma* - blur lens gamma takes list[float, float],

motion:
- motion_size* - motion blur size takes list[uint, uint]
- motion_angle* - rotate motion blur takes list[int, int]