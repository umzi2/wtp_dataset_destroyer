input = "path/to/input"
output = "path/to/output"


degradation {
  type = "resize"
  alg_lq = ["box", "hermite", "linear", "lagrange", "cubic_catrom", "cubic_mitchell", "cubic_bspline",
    "lanczos", "gauss"]
  alg_hq = ["lagrange"]
  spread = [0.75, 2.004, 0.05]
  scale = 4
  color_fix = true
  gamma_correction = false
}

shuffle_dataset = true
num_workers = 5
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