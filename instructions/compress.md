```json
 {
   "type":"compress",
   "algorithm": ["jpeg", "webp","h264","hevc","mpeg","mpeg2","vp9"],
   "target_compress": {
     "h264": [23,32],
     "hevc": [20,34],
     "mpeg": [2,20],
     "mpeg2": [2,20],
     "vp9": [20,35],
     "jpeg": [40,100],
     "webp": [40,100]
   },
 
   "comp": [40, 100],
   "probability": 0.5
 
 }
```

`*` = optional parameters

- `type` - Ignore this, not configurable
- `algorithm` - The list of compression algorithms to use
- `target_compress`* - A range of compression levels for each algorithm. A value is randomly picked between this range `{"algorithm":[low,high]}`
- `comp`* - The compression level to be used if target_compress is not implemented for the algorithm
- `probability`* - The chance of applying (e.g. 0.5 = 50% chance of being applied)
