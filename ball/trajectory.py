import numpy as np
import cv2

class BallTrajectory:
    def __init__(self):
        self.positions = []

    def add_position(self, position):
        if position is not None:
            self.positions.append(position)
            if len(self.positions) > 100:
                self.positions.pop(0)

    def get_last_n_positions(self, n):  
        return self.positions[-n:]

    def calculate_direction(self, p1, p2):
        return np.array([p2[0] - p1[0], p2[1] - p1[1]])

    def calculate_angle_between_directions(self, dir1, dir2):
        cos_angle = np.dot(dir1, dir2) / (np.linalg.norm(dir1) * np.linalg.norm(dir2))
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        return np.arccos(cos_angle)
    
    def detect_direction_change(self, trajectory, threshold=0.3):
        if len(trajectory) < 3:
            return False
        dir1 = self.calculate_direction(trajectory[-3], trajectory[-2])
        dir2 = self.calculate_direction(trajectory[-2], trajectory[-1])
        angle = self.calculate_angle_between_directions(dir1, dir2)
        return angle > threshold

    def draw_direction(self, frame):
        if len(self.positions) < 2:
            return frame       
        start_point = tuple(map(int, self.positions[-2]))
        end_point = tuple(map(int, self.positions[-1]))
        color = (0, 255, 0)  
        thickness = 2
        cv2.arrowedLine(frame, start_point, end_point, color, thickness, tipLength=0.3)
        return frame

    def calculate_speed(self):
        if len(self.positions) < 2:
            return None
        dist = np.linalg.norm(np.array(self.positions[-1]) - np.array(self.positions[-2]))
        return dist 

    def apply_low_pass_filter(self, data, alpha=0.2):
        if len(data) < 2:
            return data

        filtered_data = [data[0]]  
        for i in range(1, len(data)):
            prev = np.array(filtered_data[-1])
            curr = np.array(data[i])
            filtered_point = alpha * curr + (1 - alpha) * prev
            filtered_data.append(tuple(filtered_point))
        filtered_data[-1] = data[-1]  
        return filtered_data

    def calculate_speed_points(self, points):
        speeds = []
        for i in range(1, len(points)):
            dist = np.linalg.norm(np.array(points[i]) - np.array(points[i - 1]))
            speeds.append(dist)
        return speeds
    
    def draw_trajectory(self, frame, n=20, alpha=0.1, direction_threshold=0.2, max_speed = 50):
        if len(self.positions) == 0 or self.positions[-1] is None:
            return frame
        self.positions = [p for p in self.positions if p is not None]
        trajectory = self.get_last_n_positions(n)
        if len(trajectory) < 2:
            return frame
        if self.detect_direction_change(trajectory, threshold=direction_threshold):
            self.positions = [trajectory[-1]]
        smoothed_trajectory = self.apply_low_pass_filter(trajectory, alpha=alpha)
        speeds = self.calculate_speed_points(smoothed_trajectory)
        avg_speed = np.mean(speeds) if speeds else 0
        normalized_speed = min(avg_speed / max_speed, 1) 
        red = int(normalized_speed * 255)
        green = int((1 - normalized_speed) * 255)
        color = (0, green, red) 
        total_points = len(smoothed_trajectory)
        for i in range(1, total_points):
            thickness = int(6 * (i / total_points)) + 1
            start = tuple(map(int, smoothed_trajectory[i - 1]))
            end = tuple(map(int, smoothed_trajectory[i]))
            cv2.line(frame, start, end, color, thickness)
        return frame