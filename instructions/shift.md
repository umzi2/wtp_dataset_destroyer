```hcl
degradation {
  type = "shift"
  shift_type= ["cmyk","rgb","yuv"]
  percent = true
  rgb = {
    r = [[-10,10], [-10,10]]
    g = [[-10,10], [-10,10]]
    b = [[-10,10], [-10,10]]
  }
  cmyk = {
    c = [[-10,10], [-10,10]]
    m = [[-10,10], [-10,10]]
    y = [[-10,10], [-10,10]]
    k = [[0,0], [0,0]]
  }
  yuv = {
    y = [[-10,10], [-10,10]]
    u = [[-10,10], [-10,10]]
    v = [[-10,10], [-10,10]]
  }
  not_target = [[-10,10], [-10,10]]
  probability = 0.5
}
```
`*` = optional parameters

### Basic Parameters
- `shift_type`* - Color spaces to apply shifts in
  - Default: ["rgb"]
  - Options: "rgb", "yuv", "cmyk"
  - Multiple types can be used
  - Each type creates different artifacts

- `percent`* - Controls shift measurement
  - Default: false
  - true: Shifts are % of image size
  - false: Shifts are in pixels

- `probability`* - Chance of applying effect
  - Default: 1.0
  - Range: 0.0 to 1.0

### Channel Shift Settings
Each channel has format: [[x_min,x_max], [y_min,y_max]]
- x values control horizontal shift
- y values control vertical shift
- Positive = right/down shift
- Negative = left/up shift

#### RGB Shifts
- `rgb.r`* - Red channel shift range
- `rgb.g`* - Green channel shift range
- `rgb.b`* - Blue channel shift range
Example: [[0,5], [0,5]] means:
  - Random x shift: 0-5 pixels/percent right
  - Random y shift: 0-5 pixels/percent down

#### YUV Shifts
- `yuv.y`* - Luminance shift range
- `yuv.u`* - Blue-difference shift range
- `yuv.v`* - Red-difference shift range

#### CMYK Shifts
- `cmyk.c`* - Cyan shift range
- `cmyk.m`* - Magenta shift range
- `cmyk.y`* - Yellow shift range
- `cmyk.k`* - Black shift range

## Examples:
### all percent = true
<div> raw</div>
<img src="images/shift/raw.png" title="raw_img">
<div> rgb r = [[-1], [1]] g = [[1], [1]] b = [[-1], [-1]]</div>
<img src="images/shift/rgb.png" title="rgb_img">
<div> cmyk c = [[-1], [1]] m = [[1], [1]] y = [[-1], [-1]] k = [[0], [0]]</div>
<img src="images/shift/cmyk.png" title="cmyk_img">
<div> yuv y = [[-1], [1]] u = [[1], [1]] v = [[-1], [-1]]</div>
<img src="images/shift/yuv.png" title="yuv_img">
