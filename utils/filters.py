import numpy as np
import json
import  cv2

class Filters:

    def __init__(self, config_path="config.json"):

        self.config = self.load_config(config_path)['FILTERS']
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2()
        self.previous_frame = None
        self.difference_frame = None

    def white_mask(self, frame):
        if frame is None: return None
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_white = np.array(self.config["white_mask"]["lower_white"])
        upper_white = np.array(self.config["white_mask"]["upper_white"])
        white_mask = cv2.inRange(hsv_frame, lower_white, upper_white)
        return white_mask
    
    def blu_filter(self, frame):
        if frame is None: return None
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_blu = np.array(self.config["blu_filter"]["lower_blu"])
        upper_blu = np.array(self.config["blu_filter"]["upper_blu"])
        blu_mask = cv2.inRange(hsv_frame, lower_blu, upper_blu)
        return blu_mask
    
    def red_filter(self, frame):
        if frame is None: return None
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array(self.config["red_filter"]["lower_red"])
        upper_red = np.array(self.config["red_filter"]["upper_red"])
        red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)
        return red_mask
    
    def brown_mask(self, frame):
        if frame is None: return None
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_brown = np.array(self.config["brown_filter"]["lower_brown"])
        upper_brown = np.array(self.config["brown_filter"]["upper_brown"])
        brown_mask = cv2.inRange(hsv_frame, lower_brown, upper_brown)
        return brown_mask
    
    def gray_scale(self, frame):
        if frame is None: return None
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return gray_frame
    
    def median_blur(self, frame):
        if frame is None: return None
        filtered_frame = cv2.medianBlur(frame, ksize=self.config["median_blur"]["kernel_size"])
        return filtered_frame
    
    def threshold(self, gray_frame):
        if gray_frame is None: return None
        _, binary_frame = cv2.threshold(gray_frame, self.config["threshold"]["threshold_value"], 255, cv2.THRESH_BINARY)
        return binary_frame

    def gaussian_blur(self, frame): 
        if frame is None: return None    
        blurred_frame = cv2.GaussianBlur(frame, (self.config["gaussian_blur"]["kernel_size"], self.config["gaussian_blur"]["kernel_size"]), self.config["gaussian_blur"]["sigma"])        
        return blurred_frame

    def back_mask(self, frame):
        if frame is None: return None
        back_mask = self.background_subtractor.apply(frame)
        return back_mask
    
    def combine_mask(self, mask1, mask2):
        if (mask1 is None) or (mask2 is None): return None
        combined_mask = cv2.bitwise_and(mask1, mask2)
        combined_mask = cv2.erode(combined_mask, None, iterations=2)
        combined_mask = cv2.dilate(combined_mask, None, iterations=2)
        return combined_mask

    def diff(self, current_frame):
        if current_frame is None: return None
        if self.previous_frame is not None:
            self.difference_frame = cv2.absdiff(current_frame, self.previous_frame)
        self.previous_frame = current_frame.copy()
        return self.difference_frame

    def load_config(self, config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
        return config
    

class VisualFilters(Filters):

    def __init__(self, name, config_path="config.json"):
        super().__init__(config_path)
        self.name = name
        self.processed_frames = []

    def white_mask(self, frame):
        white_mask = super().white_mask(frame)
        self.processed_frames.append((white_mask, "white_mask"))
        return white_mask
    
    def blu_filter(self, frame):
        blu_mask = super().blu_filter(frame)
        self.processed_frames.append((blu_mask, "blu_filter"))
        return blu_mask
    
    def red_filter(self, frame):
        red_mask = super().red_filter(frame)
        self.processed_frames.append((red_mask, "red_filter"))
        return red_mask
    
    def brown_mask(self, frame):
        brown_mask = super().brown_mask(frame)
        self.processed_frames.append((brown_mask, "brown_mask"))
        return brown_mask
    
    def gray_scale(self, frame):
        gray_frame = super().gray_scale(frame)
        self.processed_frames.append((gray_frame, "gray_scale"))
        return gray_frame
    
    def median_blur(self, frame,):
        filtered_frame = super().median_blur(frame)
        self.processed_frames.append((filtered_frame, "median_blur"))
        return filtered_frame
    
    def threshold(self, gray_frame):
        binary_frame = super().threshold(gray_frame)
        self.processed_frames.append((binary_frame, "threshold"))
        return binary_frame

    def gaussian_blur(self, frame):     
        blurred_frame = super().gaussian_blur(frame)
        self.processed_frames.append((blurred_frame, "gaussian_blur"))  
        return blurred_frame

    def back_mask(self, frame):
        back_mask = super().back_mask(frame)
        self.processed_frames.append((back_mask, "back_mask"))
        return back_mask
    
    def combine_mask(self, mask1, mask2):
        combined_mask = super().combine_mask(mask1, mask2)
        self.processed_frames.append((combined_mask, "combined_mask"))
        return combined_mask

    def diff(self, current_frame):
        difference_frame = super().diff(current_frame)
        self.processed_frames.append((difference_frame, "diff"))
        return difference_frame

    def visualize_steps(self, grid_size = (2, 2)):
        if not self.processed_frames:
            raise ValueError("Nessun frame da visualizzare nella pipeline.")
        rows, cols = grid_size
        original_height, original_width = self.processed_frames[0][0].shape[:2] if self.processed_frames[0][0] is not None else (1, 1)
        scale_factor = 1 
        resized_height, resized_width = int(original_height * scale_factor), int(original_width * scale_factor)
        canvas_height, canvas_width = rows * resized_height, cols * resized_width
        canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)
        for idx, (frame, name) in enumerate(self.processed_frames):
            r, c = divmod(idx, cols)
            start_y, start_x = r * resized_height, c * resized_width
            end_y, end_x = start_y + resized_height, start_x + resized_width
            if frame is None:
                frame = np.zeros((original_height, original_width, 3), dtype=np.uint8)
            if len(frame.shape) == 2:
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            frame_resized = cv2.resize(frame, (resized_width, resized_height), interpolation=cv2.INTER_AREA)
            canvas[start_y:end_y, start_x:end_x] = frame_resized
            font_scale = 1.5  # Aumenta la dimensione del font
            thickness = 2  # Aumenta lo spessore del testo
            color = (0, 255, 0)  # Colore verde
            position = (start_x + 10, start_y + 40)  # Posizione del testo, regolata per evitare sovrapposizioni
            cv2.putText(canvas, name, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness, cv2.LINE_AA)
        self.processed_frames = []
        cv2.namedWindow(f"{self.name} Pipeline Visualization", cv2.WINDOW_NORMAL)
        cv2.imshow(f"{self.name} Pipeline Visualization", canvas)
        cv2.waitKey(1)