import argparse
import time
import sys
import os
import ctypes

class FakeCanvas():

    def __init__(self):
        self.width = 64
        self.height = 32
        self.buffer = bytearray(3*self.width*self.height)

class FakeMatrix():

    def __init__(self):
        pass
    
    def CreateFrameCanvas(self):
        return FakeCanvas()

    def SwapOnVSync(self, context):
        return FakeCanvas()

class FakeBase(object):
    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser()
        self.matrix = FakeMatrix()

    def usleep(self, value):
        time.sleep(value / 1000000.0)

    def run(self):
        print("Running")

    def GebeFarbe(self, r, g, b):
        # return ctypes.c_ulong( (r & 0xff) | ((g & 0xff) << 8) | ((b & 0xff) << 16) )
        x = bytearray(3)
        x[0] = r
        x[1] = g
        x[2] = b
        return x

    def DrawBlock(self, canvas, x1, y1, x2, y2, color):
        if x2 < x1:
            x2, x1 = x1, x2
        if y2 < y1:
            y2, y1 = y1, y2        
        for y in range(y1,y2+1):
            o = 3*(y*canvas.width+x1)
            for _ in range(x1,x2+1):
                canvas.buffer[o+0] = color[0]
                canvas.buffer[o+1] = color[1]
                canvas.buffer[o+2] = color[2]
                o += 3

    def DrawSprite(self, canvas, x1, y1, x2, y2, colors):
        pass

    def process(self):
        self.args = self.parser.parse_args()

        try:
            # Start loop
            print("Press CTRL-C to stop sample")
            self.run()
        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)

        return True
