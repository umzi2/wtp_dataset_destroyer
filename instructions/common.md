```json 
  "input": "/media/umzi/H/датасеты/descreenton/HR",
  "output": "/media/umzi/H/датасеты/descreenton/HR2",
  "process":[]
  "tile": {
    "size": 512,
    "no_wb": true
  },
  "num_workers": 16,
  "map_type": "process",
  "laplace_filter": 0.02,
  "size": 1000,
  "shuffle_dataset": true,
  "gray": true
  "gray_or_color":true
```
- input - input folder
- output - output folder
- process - a lossy dictionary that will be applied to each image
- num_workers* - number of processes for parallel processing
- map_type* - processing type: process, thread and for
- size* - how many scans to take from the input folder 
- laplace_filter* - It filters out low saturation images using the laplace operator, accepts a float value, I advise you to experiment with value
- shuffle_dataset* - shuffles the file list
- tile*  
  - size - tile size
  - no_wb* - ignoring pure white and pure black images (bool)
- gray* - All images are read only in grayscale mode
- gray_or_color* - reads images in rgb and then determines the gradation of the gray image or rgb does not make sense when gray is enabled
