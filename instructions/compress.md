```json
 {
  "type": "compress",
  "algorithm": [
    "jpeg",
    "webp",
    "h264",
    "hevc",
    "mpeg",
    "mpeg2",
    "vp9"
  ],
  "target_compress": {
    "h264": [
      23,
      32
    ],
    "hevc": [
      20,
      34
    ],
    "mpeg": [
      2,
      20
    ],
    "mpeg2": [
      2,
      20
    ],
    "vp9": [
      20,
      35
    ],
    "jpeg": [
      40,
      100
    ],
    "webp": [
      40,
      100
    ]
  },
  "comp": [
    40,
    100
  ],
  "probability": 0.5
}
```
- algorithm - compression algorithm list
- target_compress* - compression level dictionary for each algorithm separately {"algorithm":[low,high]}
- comp* - compression level if target_compress is not implemented for the algorithm
- probability* - chance of triggering
