input  = "input"
output = "output"


degradation {
  type = "resize"
  options = {
    alg_lq = ["c_box", "i_gaussian", "c_hamming", "s_catmullrom", "i_hamming", "s_box", "s_gaussian", "s_hamming", "i_lanczos3", "s_mitchell", "c_catmullrom", "i_mitchell", "c_lanczos3", "c_bilinear", "c_mitchell", "i_bilinear", "i_box", "c_gaussian", "s_lanczos3", "s_bilinear", "i_catmullrom", "nearest", ]
    alg_hq = ["dpid_0.5"]

    spread = [0.5, 1, 0.05]
    scale  = 2
  }
}
degradation {
  type = "lines"
  options = {
    probability = 0.2
  }
}
degradation {
  type = "blur"
  options = {
    filters        = ["box", "gauss", "lens", "airy", "triangle"]
    kernel         = [0.01, 1.5]
    ring_thickness = [1, 1]
    probability    = 0.75
  }
}
degradation {
  type = "halo"
  options = {
    blur = {
      filters        = ["box", "gauss", "lens", "airy", "triangle", "ring", ]
      kernel         = [0.01, 2]
      ring_thickness = [1, 1]
    }
  }
  probability = 0.5
}
degradation {
  type = "dithering"
  options = {

    probability = 0.2
  }
}
degradation {
  type = "compress"
  options = {
    algorithm      = ["jpeg", "webp", "avif", "j2000"]
    compress       = [50, 100]
    samplings      = ["444", "440", "441", "422", "420", "411", "410"]
    quantize_table = ["default", "flat", "mssim", "psnr", "im", "ksc", "dxr", "vdm", "idm"]
    target_compress = {
      avif = [20, 32]
    }
    probability = 1
  }
}
degradation {
  type = "halo"
  options = {
    blur = {
      filters        = ["box", "gauss", "lens", "airy", "triangle", "ring", ]
      kernel         = [0.01, 1]
      ring_thickness = [1, 1]
    }
  }

  probability = 0.1
}
degradation {
  type = "compress"
  options = {
    algorithm      = ["jpeg", "webp", "avif", "j2000"]
    compress       = [40, 75]
    samplings      = ["444", "440", "441", "422", "420", "411", "410"]
    quantize_table = ["default", "flat", "mssim", "psnr", "im", "ksc", "dxr", "vdm", "idm"]
    target_compress = {
      avif = [30, 36]
    }
    probability = 0.3
  }
}

debug    = true
map_type = "process"
