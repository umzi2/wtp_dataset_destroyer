```json
       "resize": {
        "alg_lq": ["box", "hermite", "hamming", "linear", "hann", "lagrange", "cubic_catrom", "cubic_mitchell", "cubic_bspline", "lanczos", "gauss", "down_up","down_down"],
        "alg_hq": ["lagrange"],
        "down_up": {
          "up": [1, 2],
          "alg_up": ["nearest", "box", "hermite", "hamming", "linear", "hann", "lagrange", "cubic_catrom", "cubic_mitchell", "cubic_bspline", "lanczos", "gauss"],
          "alg_down": ["hermite", "hamming", "linear", "hann", "lagrange", "cubic_catrom", "cubic_mitchell", "cubic_bspline", "lanczos", "gauss","down_down"]
        },
        "down_down": {
          "step": 6,
          "alg_down": ["hermite", "linear", "hann", "lagrange", "cubic_catrom", "cubic_mitchell", "cubic_bspline"]
        },
        "spread": [1, 2, 0.25],
        "scale": 4,
        "color_fix": true,
         "gamma_correction": false,
         "prob": 0.5
      },

```
alg_lq and alg_hq - list of algorithms from which a random algorithm will be selected, down_down and down_up are custom algorithms, I will tell you more about it further on.
* down_up - algorithm that first enlarges then reduces images, up - list for randrange that randomly selects the image enlargement coefficient. alg_up - enlargement filter cannot include down_down and down_up. alg_down - algorithm of subsequent reduction, it cannot include down_up.  
* down_down - algorithm of image reduction with step. step - up to how many steps can be reduced. alg_down - reduction filter, it can not have down_down and down_up.

- spread - list for randrange randomized scatter reduction. I.e. if standard at 2x reduction hq = 512 lq = 256 when setting this parameter you can have a randrange at [1 ,2, 0.25] hq = 512-256 lq = 256-128.
- color_fix* - by 5 points the image crashes, this is necessary since some chainner_ext interpolations can add a grid on white within a radius of up to -5 from the maximum
- gamma_correction* - enable or disable gamma correction in chainner_ext
- prob* - chance of triggering

