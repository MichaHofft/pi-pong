import argparse
import time
import sys
import os
import ctypes
import mmap
import fastfakemodule as fastfake

class FakeCanvas():

    def __init__(self):
        self.width = 64
        self.height = 64
        self.buffer = bytearray(3*self.width*self.height)

class FakeMatrix():

    def __init__(self):
        self.shm = mmap.mmap(0, 12292, "Local\\Test")
        # if self.shm:
        #     self.shm.write(bytes("5", 'UTF-8'))
        #     self.shm.write(bytes("Hello", 'UTF-8'))
        #     print("GOOD")
    
    def CreateFrameCanvas(self):
        return FakeCanvas()

    def SwapOnVSync(self, context):
        if self.shm is not None:
            self.shm.seek(0)
            self.shm.write(context.buffer)
        return context

class FastFakeBase(object):
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
        fastfake.DrawBlock(canvas.buffer, canvas.width, canvas.height, x1, y1, x2, y2, color)

    def DrawSprite(self, canvas, x1, y1, x2, y2, sprite):
        fastfake.DrawSprite(canvas.buffer, canvas.width, canvas.height, x1, y1, x2, y2, sprite)

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
