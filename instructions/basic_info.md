This document covers basic information on how to configure `wtp_dataset_destroyer`.

### Common Parameters
- All effects support these basic parameters:
  - `probability`: Chance to apply the effect (0.0-1.0)
  - `type`: Name of the effect (required)
  - Parameters marked with `*` are optional

### Effect Types
1. Image Quality Effects:
   - `blur`: Gaussian and motion blur
   - `noise`: Various noise patterns
   - `compress`: JPEG/HEVC compression artifacts
   - `pixelate`: Mosaic/pixel art effect

2. Color Effects:
   - `color`: Brightness and contrast
   - `saturation`: Color intensity
   - `dithering`: Color reduction with patterns
   - `subsampling`: Color channel degradation

3. Artistic Effects:
   - `screentone`: Manga-style patterns
   - `halo`: Light/dark edge artifacts
   - `sin`: Sinusoidal patterns

4. Distortion Effects:
   - `shift`: Color channel misalignment
   - `resize`: Resolution changes

### Disabling degradations
To disable degradations, simply delete the section from your config file. This is what a section looks like:
```py
    {
      "type": "sin",
      "shape": [100,1000,100],
      "alpha": [0.1,0.5],
      "bias": [-1,1],
      "vertical": 0.5,
      "probability": 0.5
    }
```
Notice the { } enclosing the section. This defines a valid section that you can remove.

### Rearranging degradation order
To change the order that degradations are applied in, simply re-arrange sections in the config. Refer to the section example described above.

### Using config
```bash 
python destroyer.py -f configs/default.py
```
It is not necessary to specify the path to the config; by default it uses the path configs/default.py

### Tips
1. Start with low probabilities (0.2-0.5) when combining multiple effects
2. Test effects individually before combining
3. Some effects work better in specific orders
4. Check example images in each effect's documentation
