class FFMPEG:
    def __init__(self):
        self.command_args = ["ffmpeg"]

    def read(self):
        self.command_args.append("-re")
        return self

    def overwrite(self):
        self.command_args.append("-y")
        return self

    def video_format(self, input_format: str):
        self.command_args.extend(["-f", input_format])
        return self

    def video_codec(self, video_codec: str):
        self.command_args.extend(["-vcodec", video_codec])
        return self

    def pixel_format(self, pixel_format: str):
        self.command_args.extend(["-pix_fmt", pixel_format])
        return self

    def resolution(self, resolution: tuple[int, int]):
        self.command_args.extend(["-s", "{}x{}".format(resolution[0], resolution[1])])
        return self

    def fps(self, fps: int):
        self.command_args.extend(["-r", str(fps)])
        return self

    def input(self, input: str):
        self.command_args.extend(["-i", input])
        return self

    def codec(self, codec: str):
        self.command_args.extend(["-c:v", codec])
        return self

    def preset(self, preset: str):
        self.command_args.extend(["-preset", preset])
        return self

    def rtsp_transport(self, rtsp_transport: str):
        self.command_args.extend(["-rtsp_transport", rtsp_transport])
        return self

    def muxdelay(self, muxdelay: float):
        self.command_args.extend(["-muxdelay", str(muxdelay)])
        return self

    def bitstream_filter(self, bitstream_filter: str):
        self.command_args.extend(["-bsf:v", bitstream_filter])
        return self

    def bitrate(self, bitrate: str):
        self.command_args.extend(["-b:v", bitrate])
        return self

    def output(self, output: str):
        self.command_args.append(output)
        return self

    def build(self):
        return self.command_args
