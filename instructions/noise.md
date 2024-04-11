```json
     "noise": {
        "type": ["perlinsuflet", "perlin", "opensimplex", "simplex", "supersimplex","uniform"],
        "normalize": true,
        "close": {
          "black": 0.1,
          "white": 0.9
        },
        "alpha": [0.01,1.0,0.01],
        "octaves": [1,10,1],
        "frequency": [0.1,0.9,0.1],
        "lacunarity": [0.01,0.5,0.01],
        "prob": 0.5
      }
```
- type - type of noise
- normalize - normalizes noise within -1 - 1 (bool) p.s. I say hello to opensimplex
- close - ignoring noise within the framework we set
   - black - ignores everything below the set value
   - white - ignores everything higher than the set value
- alpha - noise transparency
- prob - chance of triggering
ps further settings for this noise list ("perlinsuflet", "perlin", "opensimplex", "simplex", "supersimplex")
- octaves - noise re-call amount, accepts sheet [low, high, step]
- frequency - division of image point size, takes sheet [low, high, step]
- lacunarity - degree of decrease in frequency when calling again frequency*lacunarity, takes sheet [low, high, step]


