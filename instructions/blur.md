```json
{
  "type": "blur",
  "filter": ["box", "gauss", "blur", "median","lens","motion"],
  "kernel": [0, 8, 1],
  "target_kernel": {
    "box": [0,2,1],
    "gauss": [0,8,1],
    "blur": [0,8,1],
    "median": [0,1,1],
    "lens": [1,2.5]
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


motion:
- motion_size* - motion blur size takes list[uint, uint]
- motion_angle* - rotate motion blur takes list[int, int]