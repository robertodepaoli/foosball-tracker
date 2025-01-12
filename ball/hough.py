import cv2
import numpy as np
import json

class Hough:
    def __init__(self, config_path="config.json"):
        self.config = self.load_config(config_path)["HOUGH"]
    
    def detect(self, gray_frame):
        if gray_frame is not None:
            circles = cv2.HoughCircles(
                gray_frame, 
                cv2.HOUGH_GRADIENT, 
                dp=self.config["dp"], 
                minDist=self.config["minDist"], 
                param1=self.config["param1"], 
                param2=self.config["param2"], 
                minRadius=self.config["minRadius"], 
                maxRadius=self.config["maxRadius"]
            )
            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")
                center, _ = self.calculate_circles_center_and_radius(circles)
                return center
        return None  

    def calculate_circles_center_and_radius(self, circles):
        centers = circles[:, :2]
        radii = circles[:, 2]
        center_x = np.mean(centers[:, 0])
        center_y = np.mean(centers[:, 1])
        avg_radius = np.mean(radii)
        return (int(center_x), int(center_y)), int(avg_radius)
    
    def load_config(self, config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
        return config