import math
import struct
import zlib


class Figure:
    def __init__(self):
        self.data = None

    def savefig(self, buf, format="png"):
        if self.data is None:
            self.data = [[0]]
        png_bytes = _to_png(self.data)
        buf.write(png_bytes)


class Axes:
    def __init__(self):
        self.data = None

    def imshow(self, data, origin="lower", cmap=None):
        if origin == "upper":
            self.data = data
        else:
            self.data = list(reversed(data))

    def set_title(self, title):
        pass


class _Subplots:
    def __init__(self):
        self.fig = Figure()
        self.ax = Axes()


def subplots():
    s = _Subplots()
    return s.fig, s.ax


def close(fig=None):
    pass


def _to_png(matrix):
    height = len(matrix)
    width = len(matrix[0]) if height else 0
    flat_min = min(min(row) for row in matrix)
    flat_max = max(max(row) for row in matrix)
    span = flat_max - flat_min if flat_max != flat_min else 1
    pixels = []
    for row in matrix:
        row_scaled = [int((val - flat_min) / span * 255) for val in row]
        pixels.append(bytes(row_scaled))

    raw_data = b"".join(b"\x00" + row for row in pixels)
    compressor = zlib.compressobj()
    compressed = compressor.compress(raw_data)
    compressed += compressor.flush()

    def chunk(tag, data):
        return struct.pack("!I", len(data)) + tag + data + struct.pack(
            "!I", zlib.crc32(tag + data) & 0xFFFFFFFF
        )

    png = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack("!IIBBBBB", width, height, 8, 0, 0, 0, 0)
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", compressed)
    png += chunk(b"IEND", b"")
    return png
