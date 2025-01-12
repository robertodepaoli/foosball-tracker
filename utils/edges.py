import cv2
import numpy as np

class TableEdges:
    def __init__(self, table_size):
        self.table_width, self.table_height = table_size
        self.edges = [
            # Bordo superiore
            {"start": (0, 40), "end": (self.table_width, 40), "normal": (0, 1)},
            # Bordo inferiore
            {"start": (0, self.table_height-80), "end": (self.table_width, self.table_height-80), "normal": (0, -1)},
            # Bordo sinistro
            {"start": (110, 0), "end": (110, self.table_height), "normal": (1, 0)},
            # Bordo destro
            {"start": (self.table_width-110, 0), "end": (self.table_width-110, self.table_height), "normal": (-1, 0)},
        ]

    def get_bounce_normal(self, x, y):
        threshold = 10  
        point = np.array([x, y])  
        for edge in self.edges:
            start, end = np.array(edge["start"]), np.array(edge["end"])
            edge_vector = end - start
            edge_length = np.linalg.norm(edge_vector)
            edge_direction = edge_vector / edge_length if edge_length != 0 else edge_vector
            projected_length = np.dot(point - start, edge_direction)
            projected_length = np.clip(projected_length, 0, edge_length) 
            closest_point = start + projected_length * edge_direction
            distance = np.linalg.norm(point - closest_point)
            if distance <= threshold:
                return edge["normal"]
        return None 

    def visualize_edges(self, frame):
        overlay = frame.copy()
        for edge in self.edges:
            start, end = edge["start"], edge["end"]
            normal = edge["normal"]
            cv2.line(overlay, start, end, (255, 0, 0), 2)
            center = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
            arrow_tip = (int(center[0] + normal[0] * 50), int(center[1] + normal[1] * 50))
            cv2.arrowedLine(overlay, center, arrow_tip, (0, 255, 0), 2, tipLength=0.4)
        alpha = 0.5
        return cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
