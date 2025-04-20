This document covers basic information on how to configure `wtp_dataset_destroyer`.

### Common Parameters
- All Degradations support these basic parameters:
  - `probability`: Chance to apply the effect (0.0-1.0)
  - `type`: Name of the effect (required)
  - Parameters marked with `*` are optional

### Available Degradations
   - `blur`: Gaussian and motion blur
   - `noise`: Various noise patterns
   - `compress`: JPEG/HEVC compression artifacts
   - `pixelate`: Mosaic/pixel art effect
   - `color`: Brightness and contrast
   - `saturation`: Color intensity
   - `dithering`: Color reduction with patterns
   - `subsampling`: Color channel degradation
   - `screentone`: Manga-style patterns
   - `halo`: Light/dark edge artifacts
   - `sin`: Sinusoidal patterns
   - `shift`: Color channel misalignment
   - `resize`: Resolution changes
   - `and`:  If the first degradation group triggers, the second one will also be executed.
   - `or`: If the first degradation group does not trigger, the second one will be executed.
### Disabling degradations
To disable degradations, simply delete the section from your config file. This is what a section looks like:
```hcl
degradation {
   type = "sin"
   shape = [100,1000,100]
   alpha = [0.1,0.5]
   bias = [-1,1]
   vertical = 0.5
   probability = 0.5
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
1. Start with low probabilities (0.2-0.5) when combining multiple Degradations
2. Test Degradations individually before combining
3. Some Degradations work better in specific orders
4. Check example images in each effect's documentation
