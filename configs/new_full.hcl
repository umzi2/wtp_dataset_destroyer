input = "/run/media/umzi/H/resselt_new/detect/test/in/"
output = "output"

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

degradation {
  type = "screentone"
  lqhq = false
  dot_size = [7]
    color {
      type_halftone = ["rgb","cmyk","gray","not_rot"]
      dot{
        angle = [-45,45]
        type = ["circle"]
      }
      dot{
        angle = [-45,45]
        type = ["ellipse"]
      }
      dot{
        angle = [-45,45]
        type = ["circle"]
      }
      dot{
        angle = [-45,45]
        type = ["circle"]
      }
      cmyk_alpha = [0.5,1.0]
    }
  dot_type = ["circle"]
  angle = [-45,45]
  probability = 0.5
}

degradation {
  type = "canny"
  thread1 = [10, 150, 1]
  thread2 = [10, 100, 1]
  aperture_size = [3, 5]
  scale = [0, 1, 0.25]
  white = 0.5
  lq_hq = true
  probability = 0.5
}

degradation {
  type = "dithering"
  dithering_type = ["floydsteinberg", "jarvisjudiceninke", "stucki", "atkinson", "burkes", "sierra",
        "tworowsierra", "sierraLite","order","riemersma","quantize"]
  color_ch = [2,10]
  map_size = [2,4,8,16]
  history = [10, 15]
  ratio = [0.1,0.9]
  probability = 0.5
}

degradation {
  type = "resize"
  alg_lq = ["box", "hermite", "linear", "lagrange", "cubic_catrom", "cubic_mitchell", "cubic_bspline",
    "lanczos", "gauss", "down_up", "down_down", "up_down"]
  alg_hq = ["lagrange"]
  down_up = {
    down = [1, 2]
    alg_up = ["nearest", "box", "hermite", "linear", "lagrange", "cubic_catrom", "cubic_mitchell",
      "cubic_bspline", "lanczos", "gauss", "down_down"]
    alg_down = [ "hermite", "linear",  "lagrange", "cubic_catrom", "cubic_mitchell", "cubic_bspline",
      "lanczos", "gauss"]
  }
  up_down = {
    up = [1, 2]
    alg_up = ["nearest", "box", "hermite", "linear", "lagrange", "cubic_catrom", "cubic_mitchell",
      "cubic_bspline", "lanczos", "gauss"]
    alg_down = [ "hermite", "linear",  "lagrange", "cubic_catrom", "cubic_mitchell", "cubic_bspline",
      "lanczos", "gauss","down_down"]
  }
  down_down = {
    step = [1, 6]
    alg_down = [ "linear", "lagrange", "cubic_catrom", "cubic_mitchell", "cubic_bspline"]
  }

  spread = [1, 2, 0.05]
  scale = 4
  color_fix = true
  gamma_correction = false
}

degradation {
  type = "subsampling"
  down = ["box", "nearest", "linear",  "lagrange", "cubic_catrom", "cubic_mitchell", "cubic_bspline",
    "lanczos", "gauss"]
  up = ["box",  "linear", "nearest", "lagrange", "cubic_catrom", "cubic_mitchell", "cubic_bspline",
    "lanczos", "gauss"]
  sampling = ["4:4:4", "4:2:2", "4:2:1", "4:1:1", "4:2:0", "4:1:0", "3:1:1"]
  yuv = ["601","709","2020"]
  blur = [0.0,4]
  probability = 0.5
}

degradation {
  type = "pixelate"
  size = [0, 4]
  probability = 0.5
}

degradation {
  type = "halo"
  type_halo = ["unsharp_mask","unsharp_halo","unsharp_gray"]
  kernel = [0,3]
  amount = [0,1]
  threshold = [0,0.5]
  probability = 0.5
}

degradation {
  type = "blur"
  filter = ["box", "gauss", "median","lens","motion","random"]
  kernel = [0, 1]
  target_kernel = {
    box = [0,1]
    gauss = [0,1]
    median = [0,1]
    lens =[0,1]
    random = [0,1]
  }
  motion_size = [0,10]
  motion_angle = [-30,30]
  probability = 0.5
}

degradation {
  type = "color"
  high = [240,255]
  low = [0,15]
  gamma = [0.9,1.1]
}

degradation {
   type = "sin"
   shape = [100,1000,100]
   alpha = [0.1,0.5]
   bias = [-1,1]
   vertical = 0.5
   probability = 0.5
}

degradation {
  type = "saturation"
  rand = [0.5,1.0]
  probability = 0.5
}

degradation {
  type = "noise"
  type_noise = ["perlinsuflet", "perlin", "opensimplex", "simplex",
    "supersimplex","uniform","salt","salt_and_pepper","pepper","gauss"]
  clip = [0.3,0.5]
  normalize = true
  y_noise = 0.3
  uv_noise = 0.3
  alpha = [0.01,0.5,0.01]
  scale {
    size = [1, 2]
    sigma = [1, 2]
    amount = [1, 3]
    probability = 0.4
  }
  motion {
    size = [1, 3]
    angle = [1, 360]
    sigma = [0,1]
    amount = [0,1]
    probability = 0.4
  }
  octaves = [1,10,1]
  frequency = [0.1,0.9,0.1]
  lacunarity = [0.01,0.5,0.01]
  probability_salt_or_pepper = [0,0.02]

  bias =  [-0.5, 0.5]
  probability =  1
}

degradation {
  type ="compress"
  algorithm = ["jpeg", "webp", "h264", "hevc", "mpeg2", "vp9"]
  jpeg_sampling = [
    "4:4:4", "4:4:0", "4:2:2", "4:2:0"
  ]
  target_compress = {
    h264 = [23,32]
    av1 = [20,34]
    hevc = [20,34]
    mpeg = [2,20]
    mpeg2 = [2,20]
    vp9 = [20,35]
    jpeg = [40,100]
    webp = [40,100]
  }
  compress = [40, 100]
  probability = 0.5
}
laplace_filter = 0.02
size = 1000
shuffle_dataset = true
num_workers = 16
map_type = "thread"
debug = false
only_lq = false
real_name = false
out_clear = true
tile = {
  size = 512
  no_wb = true
}
gray = false