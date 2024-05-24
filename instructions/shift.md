```json
{
  "type": "shift",
  "shift_type": [
    "rgb",
    "cmyk",
    "yuv"
  ],
  "percent": true,
  "rgb": {
    "r": [
      [
        -10,
        10
      ],
      [
        -10,
        10
      ]
    ],
    "g": [
      [
        -10,
        10
      ],
      [
        -10,
        10
      ]
    ],
    "b": [
      [
        -10,
        10
      ],
      [
        -10,
        10
      ]
    ]
  },
  "cmyk": {
    "c": [
      [
        -10,
        10
      ],
      [
        -10,
        10
      ]
    ],
    "m": [
      [
        -10,
        10
      ],
      [
        -10,
        10
      ]
    ],
    "y": [
      [
        -10,
        10
      ],
      [
        -10,
        10
      ]
    ],
    "k": [
      [
        0,
        0
      ],
      [
        0,
        0
      ]
    ]
  },
  "yuv": {
    "y": [
      [
        -10,
        10
      ],
      [
        -10,
        10
      ]
    ],
    "u": [
      [
        -10,
        10
      ],
      [
        -10,
        10
      ]
    ],
    "v": [
      [
        -10,
        10
      ],
      [
        -10,
        10
      ]
    ]
  },
  "not_target": [
    [
      -10,
      10
    ],
    [
      -10,
      10
    ]
  ],
  "probability": 0.5
}
```
- shift_type* - offset types from which a random one is selected, in fact the type is the space in which channel offsets occur.
- percent* - if true the offset values are the offset percentage, otherwise these are the offset values in pixels
- (rgb,cmyk,yuv)* - dictionaries in which the offset is set for each channel of space. Each channel is a list[list[int, int],list[int, int]] the first list is the x offset and the second is the y offset
- not_target* - values that will be used if there are no value values in the channel
- probability* - chance of triggering