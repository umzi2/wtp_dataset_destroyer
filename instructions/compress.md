```json
 {
   "type":"compress",
   "algorithm": ["jpeg", "webp","h264","av1","mpeg","mpeg2","vp9"],
   "jpeg_sampling": [
        "4:4:4", "4:4:0", "4:2:2", "4:2:0"
      ],
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
- `jpeg_sampling`* - jpeg_sampling: A list of sampling factors for JPEG compression. Sampling factors determine the chroma subsampling method used to reduce color information in the image, which helps in compressing the image more efficiently. Common values include "4:4:4", "4:2:2", and "4:2:0", where lower ratios imply higher compression and loss of color detail.
- `target_compress`* - A range of compression levels for each algorithm. A value is randomly picked between this range `{"algorithm":[low,high]}`
- `comp`* - The compression level to be used if target_compress is not implemented for the algorithm
- `probability`* - The chance of applying (e.g. 0.5 = 50% chance of being applied)
## Examples:

<div> Raw</div>
<img src="images/compress/raw.png" title="raw_img">
<div> Jpeg 50 4:2:0</div>
<img src="images/compress/jpeg_50.png" title="jpeg_img">
<div> Jpeg 50 4:4:4</div>
<img src="images/compress/jpeg_50_4_4_4.png" title="jpeg_img">
<div> Webp 50</div>
<img src="images/compress/webp_50.png" title="webp_img">
<div> h264 32</div>
<img src="images/compress/h264_32.png" title="h264_img">
<div> av1 35</div>
<img src="images/compress/av1_35.png" title="av1_img">
<div> Mpeg 20</div>
<img src="images/compress/mpeg_20.png" title="mpeg_img">
<div> Mpeg2 20</div>
<img src="images/compress/mpeg2_20.png" title="mpeg2_img">
<div> Vp9 35</div>
<img src="images/compress/vp9_35.png" title="vp9_img">
