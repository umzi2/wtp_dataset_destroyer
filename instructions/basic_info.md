This document covers basic information on how to configure `wtp_dataset_destroyer`.

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

