from players.zone import Zone
from utils.filters import Filters, VisualFilters
import cv2
import numpy as np
import math

class PitTracker():
    
    def __init__(self, set_stecche) -> None:
        self.set_stecche = set_stecche
        self.zone = Zone()
        self.filters = Filters()

    
    def detect(self, frame):
        self.frame = frame
        if self.set_stecche.colore == 'blu': mask = self.filters.blu_filter(self.frame)
        elif self.set_stecche.colore == 'rosso': mask = self.filters.red_filter(self.frame)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        figure = self.logica(contours)
        self.draw_pit(figure)
        self.zone.zones(self.frame)
        self.pit_update(figure)
        self.draw_text()
        return self.frame


    def logica(self, contours):
        min_area = 500
        max_area = 5000
        figure = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if min_area < area < max_area:
                figure.append(contour)
        return figure
    
    def draw_pit(self, figure):
        cv2.drawContours(self.frame, figure, -1, (0, 255, 0), 2)

    def pit_update(self, figure):
        por_sx = (0,0)
        por_dx = (0,0)
        att = 0
        cc = 0
        dif = 0
        for fig in figure:
            M = cv2.moments(fig)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                if self.zone.sx[3][0][0] < cX < self.zone.sx[3][1][0] and att < 3: 
                    self.set_stecche.attacco.pitotini[att].update(cX, cY)
                    att = att + 1

                if self.zone.sx[2][0][0] < cX < self.zone.sx[2][1][0] and cc < 5:
                    self.set_stecche.centrocampo.pitotini[cc].update(cX, cY)
                    cc = cc + 1 

                if self.zone.sx[1][0][0] < cX < self.zone.sx[1][1][0] and dif < 2: 
                    self.set_stecche.difensore.pitotini[dif].update(cX, cY)
                    dif = dif + 1
                
                if self.zone.sx[0][0][0] < cX < self.zone.sx[0][1][0] :
                    zX = (self.zone.sx[0][1][0] - self.zone.sx[0][0][0])/2
                    zY = (self.zone.sx[0][1][1] - self.zone.sx[0][0][1])/2
                    if abs(math.sqrt((cX - zX)**2 + (cY - zY)**2)) < abs(math.sqrt((por_sx[0] - zX)**2 + (por_sx[1] - zY)**2)) : por_sx = (cX, cY)

                if self.zone.dx[3][0][0] < cX < self.zone.dx[3][1][0] and att < 3: 
                    self.set_stecche.attacco.pitotini[att].update(cX, cY)
                    att = att + 1

                if self.zone.dx[2][0][0] < cX < self.zone.dx[2][1][0] and cc < 5:
                    self.set_stecche.centrocampo.pitotini[cc].update(cX, cY)
                    cc = cc + 1 

                if self.zone.dx[1][0][0] < cX < self.zone.dx[1][1][0] and dif < 2:
                    self.set_stecche.difensore.pitotini[dif].update(cX, cY)
                    dif = dif + 1 

                if self.zone.dx[0][0][0] < cX < self.zone.dx[0][1][0] :
                    zX = (self.zone.dx[0][1][0] - self.zone.dx[0][0][0])/2 + self.zone.dx[0][0][0]
                    zY = (self.zone.dx[0][1][1] - self.zone.dx[0][0][1])/2
                    if abs(math.sqrt((cX - zX)**2 + (cY - zY)**2)) < abs(math.sqrt((por_dx[0] - zX)**2 + (por_dx[1] - zY)**2)) : por_dx = (cX, cY)

        if por_sx != (0, 0):
            self.set_stecche.portiere.pitotini[0].update(por_sx[0], por_sx[1])
        
        if por_dx != (0, 0):
            self.set_stecche.portiere.pitotini[0].update(por_dx[0], por_dx[1])

    def draw_text(self):
        for pit in self.set_stecche.attacco.pitotini:
            cv2.putText(self.frame,f"ATT {self.set_stecche.colore}", (pit.x-50,pit.y-40), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=3, color= (0,255,0))
            self.frame = cv2.circle(self.frame, (pit.x, pit.y), 7, (255, 255, 255), -1)
            
        for pit in self.set_stecche.centrocampo.pitotini:
            cv2.putText(self.frame,f"CC {self.set_stecche.colore}", (pit.x-50,pit.y-40), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=3, color= (0,255,0))
            self.frame = cv2.circle(self.frame, (pit.x, pit.y), 7, (255, 255, 255), -1)

        for pit in self.set_stecche.difensore.pitotini:
            cv2.putText(self.frame,f"DIF {self.set_stecche.colore}", (pit.x-50,pit.y-40), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=3, color= (0,255,0))
            self.frame = cv2.circle(self.frame, (pit.x, pit.y), 7, (255, 255, 255), -1)

        for pit in self.set_stecche.portiere.pitotini:
            cv2.putText(self.frame,f"POR {self.set_stecche.colore}", (pit.x-50,pit.y-40), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=3, color= (0,255,0))
            self.frame = cv2.circle(self.frame, (pit.x, pit.y), 7, (255, 255, 255), -1)