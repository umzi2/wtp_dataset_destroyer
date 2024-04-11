```json 
  "input": "/media/umzi/H/датасеты/descreenton/HR",
  "output": "/media/umzi/H/датасеты/descreenton/HR2",
  "process":{}
  "tile": {
    "size": 512,
    "no_wb": true
  },
  "replays": 1,
  "gray": true
  "gray_or_color"
```
- input - input folder
- output - output folder
- process - a lossy dictionary that will be applied to each image
- tile*  
  - size - tile size
  - no_wb* - ignoring pure white and pure black images (bool)
- replays* - number of repeated passes with losses I.e. we go through hq 2 times and generate a dataset of double size
- gray* - All images are read only in grayscale mode
- gray_or_color* - reads images in rgb and then determines the gradation of the gray image or rgb does not make sense when gray is enabled
