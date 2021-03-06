#!/usr/bin/env python2

import numpy as np
import cv2
import argparse
import sys


def wait_esc(msg='Press ESC to continue ...'):
    if msg:
        print(msg)
    while True:
        # get LSB (least significant bit) and compare it with keymap
        if cv2.waitKey(0) & 0xff == 27:
            break

def show(img, title='image', wait=False):
    cv2.imshow(title, img)
    if wait:
        wait_esc()
    cv2.destroyWindow(title)

def load_frames(filename1, filename2, flags=0):
    frame1 = cv2.imread(filename1, flags)
    frame2 = cv2.imread(filename2, flags)

    # argument validation
    if frame1 is None:
        sys.stderr.write('Cannot read image 1 %s\n' % filename1)
        sys.exit(1)
    if frame2 is None:
        sys.stderr.write('Cannot read image 2 %s\n' % filename2)
        sys.exit(1)

    return frame1, frame2

def flow2rgb(flow):
    magnitude, angle = cv2.cartToPolar(flow[... , 0], flow[... , 1], angleInDegrees=True)

    # dimension for the HSV image
    dimension = (flow.shape[0], flow.shape[1], 3)

    # create HSV image with the same size as frame 1
    # initialize all pixels with zero
    hsv = np.zeros(dimension, dtype=np.uint8)

    hue        = angle / 2
    saturation = 255
    value      = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)

    hsv[... , 0] = hue        # range [0, 179]
    hsv[... , 1] = saturation # range [0, 255]
    hsv[... , 2] = value      # range [0, 255]

    # convert HSV image back to RGB space
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return rgb

parser = argparse.ArgumentParser()
parser.add_argument('image1', help="First frame")
parser.add_argument('image2', help="Second frame")

if __name__ == '__main__':
    import sys

    args = parser.parse_args()

    # load an color image  in grayscale
    frame1, frame2 = load_frames(args.image1, args.image2, 0)

    # argument validation
    if frame1 is None:
        print('Cannot read image 1 %s' % args.image1)
        sys.exit(1)
    if frame2 is None:
        print('Cannot read image 2 %s' % args.image2)
        sys.exit(1)

    # flow = cv2.calcOpticalFlowFarneback(frame1, frame2, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    flow = cv2.calcOpticalFlowFarneback(frame1, frame2,
        0.5,  # pyramid scale: < 1 to build pyramids for each image. 0.5 means a
              # classical pyramid, where each next layer is twice smalller than the
              # previous one
        3,    # number of pyramid layers
        15,   # averaging windows size. larger values increase the algorithm robustness
              # to image noise and give more chances for fast motion detection, but
              # yields more blurred motion field
        3,    # number of iterations for each pyramid level
        5,    # size of the pixel neighborhood used to find the polynomial expansion
              # in each pixel
        1.2,  # standard deviation of the Gaussian used to smooth derivations
        0     # flags
    )

    rgb = flow2rgb(flow)
    show(rgb)
