from utils.filters import Filters, VisualFilters
from ball.contours import Contours
from ball.hough import Hough
from ball.kalman import KalmanFilter
from ball.trajectory import BallTrajectory
import numpy as np
import cv2

class BallTracker:

    def __init__ (self):               
        self.hough = Hough()
        self.contours = Contours()
        self.hough_filters = Filters()
        #self.hough_filters = VisualFilters("hough")
        self.contours_filters = Filters()
        #self.contours_filters = VisualFilters("contours")
        self.kalman = KalmanFilter()
        self.trajectory = BallTrajectory()
        self.previous_filtered_hough = None
        self.missing_frames = 0

    def detect(self, frame):
        hough_coordinates = self.hough_process(frame)
        #self.hough_filters.visualize_steps()
        #self.draw_point_on_frame(frame, hough_coordinates)
        contours_coordinates = self.contours_process(frame)
        #self.contours_filters.visualize_steps()
        #self.draw_point_on_frame(frame, contours_coordinates)
        best_coordinates = self.find_best_coordinates(hough_coordinates, contours_coordinates)
        #self.draw_point_on_frame(frame, best_coordinates)
        self.kalman.predict()
        self.kalman.update(best_coordinates)
        x, y, vx, vy = self.kalman.get_state()
        #self.draw_point_on_frame(frame, (x, y), (255, 0, 0))
        chosen_position = self.select_position(
            best_coordinates,
            (x, y, vx, vy),
            distance_threshold=50,  
            max_missing_frames=10  
        )
        #self.draw_point_on_frame(frame, chosen_position, (0,255,0))
        self.trajectory.add_position(chosen_position)
        frame = self.trajectory.draw_trajectory(frame)
        #frame = self.kalman.field_forces.visualize_field(frame)
        return frame

    def hough_process(self, frame):
        frame = self.hough_filters.gray_scale(frame)
        frame = self.hough_filters.diff(frame)
        frame = self.hough_filters.median_blur(frame)
        frame = self.hough_filters.threshold(frame)
        if self.previous_filtered_hough is not None:
            intersection = cv2.bitwise_and(frame, self.previous_filtered_hough)
            frame = cv2.absdiff(frame, intersection)
        self.previous_filtered_hough = frame
        hough_coordinates = self.hough.detect(frame)
        return hough_coordinates
    
    def contours_process(self, frame):
        white = self.contours_filters.white_mask(frame)
        back = self.contours_filters.back_mask(frame)
        frame = self.contours_filters.combine_mask(white, back)
        frame = self.contours_filters.median_blur(frame)
        contours_coordinates = self.contours.detect(frame)
        return contours_coordinates
    
    def find_best_coordinates(self, hough_coordinates, contours_coordinates):
        if contours_coordinates is None:
            return hough_coordinates
        if hough_coordinates is None: 
            if len(self.trajectory.positions)>0 and self.gap(self.trajectory.positions[-1], contours_coordinates)<25:
                 return contours_coordinates
            else: return None
        if self.gap(contours_coordinates, hough_coordinates) > 100:
            return hough_coordinates
        return self.weighted_average(hough_coordinates, contours_coordinates)
    
    def select_position(self, best, kalman_state, distance_threshold=50, max_missing_frames=5):
        if best is None:
            self.missing_frames += 1
            if self.missing_frames > max_missing_frames:
                return None
            return kalman_state[:2]
        self.missing_frames = 0
        distance = self.gap(best, kalman_state[:2])
        if distance > distance_threshold:
            return best
        return kalman_state[:2]

    def gap(self, coord_1, coord_2):
            if coord_1 is not None and coord_2 is not None:
                return np.linalg.norm(np.array(coord_1) - np.array(coord_2))
            else:
                return float('inf')
            
    def weighted_average(self, coord_1, coord_2, w_1 = 0.5, w_2 = 0.5):
            coord_1 = np.array(coord_1)
            coord_2 = np.array(coord_2)
            weighted_avg = (w_1 * coord_1 + w_2 * coord_2) / (w_1 + w_2)          
            return weighted_avg
    
    def draw_point_on_frame(self, frame, coordinates, color=(0, 0, 255), radius=5, thickness=-1):
        if coordinates is not None:
            x, y = int(coordinates[0]), int(coordinates[1])
            cv2.circle(frame, (x, y), radius, color, thickness)