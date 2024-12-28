input = "path/to/input"
output = "path/to/output"

degradation {
  type = "resize"
  alg_lq = ["box", "hermite", "linear", "lagrange", "cubic_catrom", "cubic_mitchell", "cubic_bspline",
    "lanczos", "gauss"]
  alg_hq = ["lagrange"]
  spread = [1,1.6, 0.25]
  scale = 4
  color_fix = true
  gamma_correction = false
}

degradation {
  type = "halo"
  type_halo = ["unsharp_gray"]
  kernel = [0,2]
  amount = [0,2]
  probability = 0.3
}

degradation {
  type = "blur"
  filter = ["box", "gauss", "lens"]
  target_kernel = {
    box = [0,2]
    gauss = [0,2]
    lens =[1,2]
  }
  probability = 0.8
}

degradation {
  type ="compress"
  algorithm = ["jpeg", "webp"]
  jpeg_sampling = [
    "4:4:4", "4:4:0", "4:2:2", "4:2:0"
  ]
  compress = [40, 100]
  probability = 0.9
}

num_workers = 8
map_type = "thread"
shuffle_dataset = true
tile = {
  size = 1024
  no_wb = true
}