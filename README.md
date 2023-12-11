# Zephyr
Zephyr is a simple RTSP library to stream and receive video over RTSP.

## Pre-requisites
- Python 3.8 or higher
- [FFmpeg](https://ffmpeg.org/) to encode and decode video
- [MediaMTX](https://github.com/bluenviron/mediamtx) as RTSP server

## Installation
The easiest way to install Zephyr is using pip:
```bash
$ pip install zephyr
```
But you can also install Zephyr from source:
```bash
$ git clone https://github.com/bpradana/zephyr.git
$ cd zephyr
$ python setup.py install
```

## Usage
Zephyr has 2 main classes, `Stream` and `Client`. `Stream` is used to stream video over RTSP, while `Client` is used to receive video from RTSP stream.
### Stream
To stream video, you need to create a `Stream` object and call `send` with a frame. You can also call `end` to stop the stream.
```python
import cv2
from zephyr import Stream

stream = Stream(
  url="rtsp://localhost:8554/test",
  resolution=(1280, 720),
  fps=30,
  bitrate="2M"
)

cap = cv2.VideoCapture(0)
while True:
  ret, frame = cap.read()
  stream.send(frame)

stream.end()
cap.release()
```
### Client
To receive video, you need to create a `Client` object and call `read` to get the frame. You can also call `release` to stop receiving video.
```python
import cv2
from zephyr import Client

client = Client(url="rtsp://localhost:8554/test")

while True:
  ret, frame = client.read()
  cv2.imshow('frame', frame)

  if cv2.waitKey(1) & 0xFF == ord("q"):
    client.release()
    break
```

## License
Zephyr is licensed under the [MIT License](LICENSE).

## Credits
- Zephyr uses [FFmpeg](https://ffmpeg.org/) to encode and decode video.
- The name Zephyr is inspired by [Zephyr](https://github.com/octavvia/zephyr) a video streaming project by [Octavia](https://github.com/octavvia).
