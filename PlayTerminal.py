import os
import time
import shutil
from types import MappingProxyType
import cv2
from draw_image import draw_image

class PlayTerminal:
    """
    ターミナルで再生するためのクラス。
    """
    def __init__(self, video_path: str, height_ratio=2):
        if os.path.isfile(video_path):
            self.video_path = video_path
            self.height_ratio = height_ratio
        else:
            raise FileNotFoundError
    
    def play(self):
        start_time = time.time()

        video = cv2.VideoCapture(self.video_path)

        if not video.isOpened():
            return

        frame_rate = video.get(cv2.CAP_PROP_FPS)
        frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        os.system("cls" if os.name == "nt" else "clear")

        last_terminal_size = shutil.get_terminal_size()

        while True:
            terminal_size = shutil.get_terminal_size()
            if terminal_size != last_terminal_size:
                os.system("cls" if os.name == "nt" else "clear")
                
            current_frame = self.__get_current_frame(start_time, frame_rate)

            resize_width, resize_height = self.__resize_to_fit(frame_width, frame_height / self.height_ratio, terminal_size.columns, terminal_size.lines)
            print_size = MappingProxyType({"width": resize_width, "height": resize_height-1})

            self.__play_loop(current_frame, video, print_size)

            last_terminal_size = terminal_size
            if current_frame >= frame_count:
                break
        
        os.system("cls" if os.name == "nt" else "clear")

    def __play_loop(self, current_frame: int, video: cv2.VideoCapture, print_size: MappingProxyType[str, int]):
            
        video.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        ret, frame = video.read()

        if ret == True:
            img = cv2.resize(frame, (print_size["width"], print_size["height"]))
            draw_image(img)

    def __get_current_frame(self, start_time: float, frame_rate: float):
        elapsed = time.time() - start_time
        return int(elapsed * frame_rate)

    def __resize_to_fit(self, image_w, image_h, terminal_w, terminal_h):
        scale = min( terminal_w / image_w, terminal_h / image_h)
        
        new_w = int(round(image_w * scale))
        new_h = int(round(image_h * scale))
        return new_w, new_h
        