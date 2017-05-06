import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

class SiftSolve:

    def __init__(self):
        self.sif = cv2.SIFT()
        self.maxSize = 384*384


    # def __
