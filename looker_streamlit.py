#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 01:37:00 2024

@author: dev
"""

from looker import track, cv2
import streamlit as st
import time
import psutil
import os
import sys
try:
    import pyautogui
except:
    print("Unable to run tab closing feature")


st.title("Gaze-Detector")
image_placeholder = st.empty()

CTR = 0
FRAME_BUFFER = 120
GAZE_SUM = 0
TOLERANCE = 30

if st.button("Close Feed"):
    try:
        pyautogui.hotkey('ctrl', 'w')
    except:
        pass
    pid = os.getpid()
    p = psutil.Process(pid)
    p.terminate()

    sys.exit()

start = time.time()


if "--st" in sys.argv:

    CAP = cv2.VideoCapture(0)
    print(CAP.read())

    while 1:
        frame, gaze = track(CAP)
        GAZE_SUM += gaze
        image_placeholder.image(
            frame,
            f"{str(CTR/(time.time() - start))[:4]} frames/second"
        )

        CTR += 1
        if CTR > FRAME_BUFFER:

            if GAZE_SUM < CTR - TOLERANCE:
                st.toast("Please look toward your screen")
                sys.stdout.write('\r\a')
                CTR = 0
                GAZE_SUM = 0
                start = time.time()

            CTR = 0
            GAZE_SUM = 0
            start = time.time()
