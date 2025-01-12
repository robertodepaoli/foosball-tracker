from utils.stream import Video
from utils.stabilizer import Stabilizer
from ball.tracker import BallTracker
from players.biliardino import Biliardino
from players.tracker import PitTracker
import cv2



stream = Video(cap=cv2.VideoCapture(r'./videos/esempio-1.mp4'))
#stream.skip(secondi=60)
stream.start_stream()

stabilizer = Stabilizer(lite = True)

biliardino = Biliardino()
pit_rosso_tracker = PitTracker(biliardino.stecche_rosse)
pit_blu_tracker = PitTracker(biliardino.stecche_blu)

ball_tracker = BallTracker()


while stream.ret:
    
    while True:
        stream.unpack_frame()
        stream.frame = stabilizer.stabilize(stream.frame)
        #stream.frame = pit_rosso_tracker.detect(stream.frame)
        #stream.frame = pit_blu_tracker.detect(stream.frame)
        stream.frame = ball_tracker.detect(stream.frame)
        if stream.frame is not None:
            stream.show_frame()
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    key = cv2.waitKey(0) & 0xFF 
    if key == ord('n'):
        stream.unpack_frame()

        stream.frame = stabilizer.stabilize(stream.frame)

        #stream.frame = pit_rosso_tracker.detect(stream.frame)
        #stream.frame = pit_blu_tracker.detect(stream.frame)

        stream.frame = ball_tracker.detect(stream.frame)

        if stream.frame is not None:
            stream.show_frame()

    if key == ord('q'):
            break


stream.end_stream()


