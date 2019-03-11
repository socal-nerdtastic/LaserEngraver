#!/usr/bin/env python3

import serial
import time
import threading

RX_BUFFER_LINES = 10
VERBOSE = True

class FakeSerial:
    def __init__(self, port, speed):
        pass
    def write(self, text):
        pass
    def readline(self):
        return ""
    def flushInput(self):
        pass

# debug line
serial.Serial = FakeSerial

class GrblControl:
    def __init__(self, port):
        self.port = port
        self.filename = None
        self.ser = serial.Serial(port, 115200)

    def start(self, filename, callback=None):
        self.t = threading.Thread(target=self._run, args=(filename,callback))
        self.t.daemon = True
        self.t.start()

    def stop(self):
        '''call this to abort a running process'''
        self._running = False

    def _run(self, filename, callback):
        self._running = True
        try:
            with open(filename, 'rb') as f:
                data = f.readlines()
        except:
            data = ['']*30

        # Wake up grbl
        print("Initializing grbl...")
        self.ser.write(b"\r\n\r\n")
        # Wait for grbl to initialize and flush startup text in serial input
        time.sleep(2)
        self.ser.flushInput()

        self.current_line = 0
        self.total_lines = len(data)
        f = iter(data)

        # send the first lines without waiting for response
        for _ in range(RX_BUFFER_LINES):
            self.ser.write(next(f))
        self.current_line = RX_BUFFER_LINES

        # send the remaining lines only after response from grbl
        for line in f:
            self.ser.readline() # blocks
            if not self._running:
                return self.stop()
            self.ser.write(line)
            self.current_line += 1

        # read the last responses
        for _ in range(RX_BUFFER_LINES):
            self.ser.readline()
            if not self._running:
                return self.stop()
        self.current_line += RX_BUFFER_LINES

        if callback:
           callback()
        self.stop()

    def close(self):
        self.ser.close()
