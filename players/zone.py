import numpy as np
import cv2

class Zone():

    def zones(self, frame):

        self.frame = frame
        self.height = self.frame.shape[0]
        self.width = self.frame.shape[1]
        x1 = 0
        x2 = self.width // 8
        x3 = 2 * (self.width // 8)
        x4 = 3 * (self.width // 8)
        x5 = 4 * (self.width // 8)
        x6 = 5 * (self.width // 8)
        x7 = 6 * (self.width // 8)
        x8 = 7 * (self.width // 8)
        self.sx = [((x1, 0), (x2, self.height)) , ((x2, 0), (x3, self.height)), ((x4, 0), (x5, self.height)), ((x6, 0), (x7, self.height))]
        self.dx = [((x8, 0), (self.width, self.height)), ((x7, 0), (x8, self.height)), ((x5, 0), (x6, self.height)), ((x3, 0), (x4, self.height))]


    def show_zones(self, frame):     
        self.zones(frame)
        for zona_sx in self.sx:
            cv2.rectangle(self.frame, zona_sx[0], zona_sx[1], (0, 255, 0), 2)
        for zona_dx in self.dx:
            cv2.rectangle(self.frame, zona_dx[0], zona_dx[1], (0, 0, 255), 2)     
        return self.frame