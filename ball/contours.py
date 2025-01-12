import cv2
import numpy as np
import  json 

class Contours:
    def __init__(self, config_path="config.json") -> None:
        self.config = self.load_config(config_path)["CONTOURS"]
   
    def detect(self, combined_mask):
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour = self.select_contour(contours)
        if contour is not None:
            center = self.calculate_center(contour)
            return center 
        return None  
   
    def select_contour(self, contours):
        area_min = self.config["area_min"]
        area_max = self.config["area_max"]
        selected_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area_min < area < area_max:
                if selected_contour is None or area > cv2.contourArea(selected_contour):
                    selected_contour = contour
        return selected_contour
        
    def calculate_center(self, contour):
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            return (cX, cY)
        return None  
    
    def load_config(self, config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
        return config