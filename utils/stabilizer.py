import cv2
import numpy as np
from utils.filters import Filters, VisualFilters

class Stabilizer():
    
    def __init__(self, lite = False) -> None:
        #self.filters = VisualFilters("stabilizer")
        self.filters = Filters()
        self.frame_count = 0
        self.corners_buffer = []
        self.lite = lite

    def stabilize(self, frame):
        self.frame = frame
        
        if self.lite == False and self.frame_count>30:
            self.fix_frame()
            return self.frame
        
        self.detect()
        if self.frame_count%30 == 0:
            self.current = self.corners
        self.fix_frame()
        self.frame_count += 1
        #self.filters.visualize_steps((1,1))
        return self.frame

    def detect(self):
        height, width = self.frame.shape[:2]
        self.height = height
        self.width = width
        self.center_x = width//2
        self.center_y = height//2
        self.corners = []

        brown_mask = self.filters.brown_mask(self.frame)
        contours, _ = cv2.findContours(brown_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.contours_to_corners(contours)
        self.get_corners()

    
    def contours_to_corners(self, contours):
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        sorted_contours = sorted_contours[:4]
        sorted_contours = sorted(sorted_contours, key=lambda contour: cv2.pointPolygonTest(contour, (self.center_x, self.center_y), True))
        # Assicurati che ci siano almeno 4 contorni
        if len(sorted_contours) < 4:
            return
        for contour in sorted_contours: 
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            min_distance = float('inf')
            closest_corner = None
            for point in approx:
                x, y = point[0]
                distance = np.sqrt((x - self.center_x) ** 2 + (y - self.center_y) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    closest_corner = (x, y)
            x, y, w, h = cv2.boundingRect(contour)
            if closest_corner[1] > self.center_y:
                closest_corner = (closest_corner[0], closest_corner[1] + w)
            else:
                closest_corner = (closest_corner[0], closest_corner[1] - w)
            self.corners.append(closest_corner)
        self.fix_pos()
        self.corners_buffer.append(self.corners)
        
    def fix_frame(self):
        corner_points = np.array(self.current, dtype=np.float32)
        corner_points = corner_points.reshape(-1, 2)
        original_points = np.float32([[0, 0], [self.width, 0], [0, self.height], [self.width, self.height]])
        perspective_transform = cv2.getPerspectiveTransform(corner_points, original_points)
        self.frame = cv2.warpPerspective(self.frame, perspective_transform, (self.width, self.height))
        
    def get_corners(self):
        if len(self.corners_buffer)>30: 
            self.corners_buffer.pop(0)
        self.corners = [tuple(sum(values) / len(self.corners_buffer) for values in zip(*subset)) for subset in zip(*self.corners_buffer)]

    def fix_pos(self):
        corners = []
        x0, y0 = self.corners[0]
        x1, y1 = self.corners[1]
        x2, y2 = self.corners[2]
        x3, y3 = self.corners[3]
        somme = [x0+y0, x1+y1, x2+y2, x3+y3]
        corners.append(self.corners[somme.index(min(somme))])
        corners.append(self.corners[somme.index(max(somme))])
        residui = [i for i in self.corners if i not in corners]
        if residui[0][0]>residui[1][0]:
            corners.insert(1, residui[0])
            corners.insert(2, residui[1])
        else:
            corners.insert(1, residui[1])
            corners.insert(2, residui[0])
        self.corners = corners
