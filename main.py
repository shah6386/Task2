import cv2
import numpy as np
from flask import Flask, send_file

app = Flask(__name__)


def __draw_label(img, text, end_x, end_y):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    scale = 1
    color = (255, 255, 255)
    thickness = cv2.FILLED
    txt_size = cv2.getTextSize(text, font_face, scale, thickness)
    pos = (int((end_x - txt_size[0][0]) / 2), end_y - 15)

    cv2.rectangle(img, (0, end_y - 50), (end_x, end_y), (255, 0, 0), thickness)
    cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)


@app.route("/addName/<name>")
def add_name(name):

    # Setup camera
    cap = cv2.VideoCapture("C:\\Users\\Mohd Shahzad\\Downloads\\input_video.mp4")

    # Read logo and resize
    logo = cv2.imread('overlay.png')
    size = 128
    logo = cv2.resize(logo, (size, size))

    # Create a mask of logo
    img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    size_video = (frame_width, frame_height)

    result = cv2.VideoWriter('filename.avi',
                             cv2.VideoWriter_fourcc(*'MJPG'),
                             cap.get(5), size_video)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if frame is None:
            break

        mid_h = int((frame.shape[0] - size) / 2)
        mid_w = int((frame.shape[1] - size) / 2)
        roi = frame[-size - mid_h: -mid_h, -size - mid_w: -mid_w]

        roi[np.where(mask)] = 0
        roi += logo

        __draw_label(frame, f'Hi {name}', frame.shape[1], frame.shape[0])

        result.write(frame)

    cap.release()

    return send_file('filename.avi')


if __name__ == "__main__":
    app.run()
