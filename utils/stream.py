import cv2

class Video():
    
    def __init__(self, cap) -> None:
        self.cap = cap
        self.ret = True

    def skip(self, secondi):
        secondi_da_tagliare = secondi  
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        frame_da_tagliare = secondi_da_tagliare * fps

        for _ in range(frame_da_tagliare):
            ret, frame = self.cap.read()
            if not ret:
                break

    def start_stream(self):
        cv2.namedWindow('video', cv2.WINDOW_NORMAL)

    def unpack_frame(self):
        ret, self.frame = self.cap.read()
        if not ret:
            self.ret = False

    def show_frame(self):    
        cv2.imshow('video', self.frame)
    
    def end_stream(self):
        self.cap.release()
        cv2.destroyAllWindows()