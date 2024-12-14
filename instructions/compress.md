```json
{
  "type": "compress",
  "algorithm": ["jpeg", "webp", "h264", "av1", "mpeg", "mpeg2", "vp9", "hevc"],
  "jpeg_sampling": [
    "4:4:4", "4:4:0", "4:2:2", "4:2:0"
  ],
  "target_compress": {
    "jpeg": [40,100],
    "webp": [40,100],
    "h264": [23,32],
    "hevc": [20,34],
    "av1": [20,35],
    "vp9": [20,35],
    "mpeg": [2,20],
    "mpeg2": [2,20]
  },
  "comp": [40, 100],
  "probability": 0.5
}
```

### Basic Parameters
- `algorithm` - List of compression algorithms to choose from
  - One is randomly selected per image
  - Note: HEVC encoding may cause errors (pts<dts or memory segmentation)

- `probability`* - Chance of applying compression
  - Range: 0.0 to 1.0
  - Default: 1.0
  - Example: 0.5 = 50% chance

### Compression Settings
- `target_compress`* - Algorithm-specific compression ranges
  - Format: `{"algorithm": [min, max]}`
  - Values are randomly selected from the specified ranges
  - If not specified for an algorithm, falls back to `comp` value

- `comp`* - Default compression range
  - Format: [min, max]
  - Default: [90, 100]
  - Used when algorithm has no `target_compress` entry

### JPEG-Specific Settings
- `jpeg_sampling`* - Chroma subsampling options
  - Default: ["4:2:2"]
  - Available options:
    - "4:4:4": No subsampling, highest quality
    - "4:4:0": Reduced vertical chroma resolution
    - "4:2:2": Horizontal chroma subsampling
    - "4:2:0": Both horizontal and vertical subsampling

### Compression Ranges by Algorithm
1. Image Formats:
   - JPEG: 40-100 (higher = better quality)
   - WebP: 40-100 (higher = better quality)

2. Video Codecs:
   - H.264: 23-32 (lower = better quality)
   - HEVC: 20-34 (lower = better quality)
   - AV1: 20-35 (lower = better quality)
   - VP9: 20-35 (lower = better quality)
   - MPEG: 2-20 (lower = better quality)
   - MPEG2: 2-20 (lower = better quality)

### Examples:

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
