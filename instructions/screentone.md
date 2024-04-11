```json
      "screentone": {
        "color": {
          "dot_size": [7],
          "r":[0,7] ,
          "g":[0,7] ,
          "b":[0,7] },
        "dot_size": 7,
        "lqhq": false,
        "prob": 0.5
      }
```
- color* - settings in case the image is 3-dimensional i.e. rgb
  - dot_size - point size accepts a list from which a random size is taken
  - r..b - random placement of dots for each color is essential for creating a variety of patterns, accepts sheet [smaller, larger] for randint
- dot_size - size of points for 2 dimensional images i.e. grayscale accepts a list
- lqhq* - equates hq to lq, assuming screentone is first in line
- prob* - chance of triggering
