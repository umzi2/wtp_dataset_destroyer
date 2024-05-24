```json
{
  "type": "noise",
  "type_noise": [
    "perlinsuflet",
    "perlin",
    "opensimplex",
    "simplex",
    "supersimplex",
    "uniform",
    "salt",
    "salt_and_pepper",
    "pepper",
    "gauss"
  ],
  "normalize": true,
  "y_noise": 0.3,
  "uv_noise": 0.3,
  "alpha": [
    0.01,
    1.0,
    0.01
  ],
  "octaves": [
    1,
    10,
    1
  ],
  "frequency": [
    0.1,
    0.9,
    0.1
  ],
  "lacunarity": [
    0.01,
    0.5,
    0.01
  ],
  "probability_salt_or_pepper": [
    0,
    0.3
  ],
  "bias": [
    -0.5,
    0.5
  ],
  "probability": 0.5
}
```
- type - type of noise

- alpha* - noise transparency
- probability* - chance of triggering
- y_noise* - the chance that the noise will be superimposed only on the tone component in color images
- uv_noise* - the chance **that noise will only affect color components, ignoring tone in color images**
- bias - noise offset, takes list[int,int] min -1, max 1

further settings for this noise list ("perlinsuflet", "perlin", "opensimplex", "simplex", "supersimplex")
- normalize* - normalizes noise within -1 - 1 (bool) p.s. I say hello to opensimplex
- octaves* - noise re-call amount, accepts sheet [low, high, step]
- frequency* - division of image point size, takes sheet [low, high, step]
- lacunarity* - degree of decrease in frequency when calling again frequency*lacunarity, takes sheet [low, high, step]

ps further settings for this noise list ("salt","pepper","salt_and_pepper")
- probability_salt_or_pepper* - the percentage of salt and pepper in the noises
