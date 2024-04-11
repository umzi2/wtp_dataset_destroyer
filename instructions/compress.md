```json
      "compress": {
        "compress_compress": [1, 2],
        "algorithm": ["jpeg", "webp","h264","hevc","mpeg","mpeg2","vp9","jpeg","webp"],
        "target_compress": {
        "h264": [23,32],
        "hevc": [20,34],
        "mpeg": [2,20],
        "mpeg2": [2,20],
        "vp9": [20,35]},
        "jpeg": [40,100],
        "webp": [40,100],

        "comp": [40, 100],
        "prob": 0.5
      }
```
- compress_compress - number of compression repetitions [low,high]
- algorithm - compression algorithm
- target_compress - compression level dictionary for each algorithm separately {"algorithm":[low,high]}
- comp - compression level if target_compress is not implemented for the algorithm
- prob - chance of triggering
