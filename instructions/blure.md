```json
{
  "type": "blur",
  "filter": ["box", "gauss", "blur", "median"],
  "kernel": [0, 8, 1],
  "target_kernel": {
    "box": [0,2,1],
    "gauss": [0,8,1],
    "blur": [0,8,1],
    "median": [0,1,1]
  },
  "probably": 0.5
}
```
- filter - blur type list
- kernel* - blur kernel [low,high,step]
- target_kernel* - separate kernel spread for each blur filter 
- probably* - chance of triggering
