#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 02:44:08 2024

@author: dev
"""

import sys
import cv2
from cv2 import CascadeClassifier as cc
from cv2.data import haarcascades as hc


FACE_CASCADE = cc(hc + 'haarcascade_frontalface_default.xml')
EYE_CASCADE = cc(hc + 'haarcascade_eye.xml')


def track(CAP: cv2.VideoCapture):
    _, frame = CAP.read()

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = FACE_CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=3,
        minSize=(30, 30)
    )
    eyes = [0, 0]

    for (x, y, w, h) in faces:
        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (255, 0, 0),
            2
        )

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        eyes = EYE_CASCADE.detectMultiScale(
            roi_gray,
            minSize=(30, 30),
            maxSize=(50, 50)
        )

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(
                roi_color,
                (ex, ey),
                (ex+ew, ey+eh),
                (0, 255, 0),
                2
            )

        sys.stdout.write(f"\rEyes detected: {len(eyes)}")

    return frame, len(eyes) > 0


if __name__ == "__main__":
    CAP = cv2.VideoCapture(0)

    while 1:
        frame, gaze = track(CAP=CAP)
        if not gaze:
            sys.stdout.write("\r\a")
        cv2.imshow('Face and Eye Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    CAP.release()
    cv2.destroyAllWindows()
