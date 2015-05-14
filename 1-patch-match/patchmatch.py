#!/usr/bin/env python2

import numpy as np
import cv2
from visual import parser, load_frames, show_flow
import random
from itertools import product

import sys
def echo(*args, **kwargs):
    end = kwargs.get('end', '\n')

    if len(args) == 1:
        sys.stdout.write(args[0])
    else:
        for arg in args:
            sys.stdout.write(str(arg))
            sys.stdout.write(' ')

    sys.stdout.write(end)


def ssd(image1, center1, image2, center2, size):
    window1 = image1[center1[0] - size : center1[0] + size,
                     center1[1] - size : center1[1] + size]

    window2 = image2[center2[0] - size : center2[0] + size,
                     center2[1] - size : center2[1] + size]

    diff = window1 - window2

    return np.sum(diff ** 2)


class PatchMatch(object):
    """Dump implementation of the PatchMatch algorithm as described by

    Connelly Barnes, Eli Shechtman, Adam Finkelstein, and Dan B. Goldman.
    PatchMatch: A randomized correspondence algorithm for structural image editing.
    In ACM Transactions on Graphics (Proc. SIGGRAPH), 2009. 2
    """

    def __init__(self, image1, image2, radius=5, maxoffset=10):
        self.image1 = image1
        self.image2 = image2
        self.radius = radius
        self.maxoffset = maxoffset

        self.nrows = self.image1.shape[0]
        self.ncols = self.image1.shape[1]
        self.niterations = 0

        # create an empty matrix with the same x-y dimensions like the first
        # image but with two channels. Each channel stands for an x/y offset
        # of a pixel at this position.
        self.result  = np.zeros(dtype=np.int16, shape=(self.nrows, self.ncols, 2))
        self.quality = np.zeros(dtype=np.float32, shape=(self.nrows, self.ncols))

        # initialize offsets randomly
        self.initialize()

    def __iter__(self):
        border = self.radius + self.maxoffset

        rows = xrange(border, self.nrows - border)
        cols = xrange(border, self.ncols - border)

        for index in product(rows, cols):
            yield index

    def initialize(self):
        for index in self:
            # create a random offset in 
            offset = random.randint(-self.maxoffset, self.maxoffset), random.randint(-self.maxoffset, self.maxoffset)

            # assing random offset
            self.result[index] = offset

            # calculate the center in the second image by adding the offset
            # to the current index
            center = index[0] + offset[0], index[1] + offset[1]

            self.quality[index] = ssd(self.image1, index, self.image2, center, self.radius)

    def iterate(self):
        self.niterations += 1

        # switch between top and left neighbor in even iterations and
        # right bottom neighbor in odd iterations
        neighbor = -1 if self.niterations % 2 == 0 else 1

        for index in self:
            self.propagate(index, neighbor)
            self.random_search(index)

    def propagate(self, index, neighbor):
        indices = (index,                           # current position
                   (index[0] + neighbor, index[1]), # top / bottom neighbor
                   (index[0], index[1] + neighbor)) # left / right neighbor
    
        # create an array of all qualities at the above indices
        qualities = np.array((self.quality[indices[0]],
                              self.quality[indices[1]],
                              self.quality[indices[2]]))

        # get the index of the maximal quality
        maxindex = indices[np.argmax(qualities)]

        # get the offset of the neighbor with the maximal quality
        if maxindex != index:
            self.result[index] = self.result[maxindex]

    def random_search(self, index):
        pass


if __name__ == '__main__':
    # command line parsing
    args = parser.parse_args()
    frame1, frame2 = load_frames(args.image1, args.image2)

    print('initialize ...')
    pm = PatchMatch(frame1, frame2)

    # # do some iterations
    for i in xrange(1):
        print('iteration %d ...' % i)
        pm.iterate()

    # display final result
    # we have to convert the integer offsets to floats, because
    # optical flow could be subpixel accurate
    show_flow(np.float32(pm.result))
