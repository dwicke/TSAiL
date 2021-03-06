#!/usr/bin/env python

import os
import numpy as np
import math
import time
from util import SaxTerminal
import itertools 

class DictionarySizeIsNotSupported(Exception): pass


class SAX(object):
    """
    This class is for computing the Symbolic Aggregate approXimation
    adapted from https://github.com/nphoff/saxpy
    and was under an MIT liscence
    """

    def __init__(self, wordSize = 8, alphabetSize = 7, epsilon = 0.001):
        ## 0.001 fro epsilon is standard see https://github.com/jMotif/SAX/search?utf8=%E2%9C%93&q=SAX_NORM_THRESHOLD&type=
        if alphabetSize < 3 or alphabetSize > 20:
            raise DictionarySizeIsNotSupported()
        self.aOffset = ord('a')
        self.wordSize = wordSize
        self.alphabetSize = alphabetSize
        self.eps = epsilon
        self.breakpoints = {'3' : [-0.43, 0.43],
                            '4' : [-0.67, 0, 0.67],
                            '5' : [-0.84, -0.25, 0.25, 0.84],
                            '6' : [-0.97, -0.43, 0, 0.43, 0.97],
                            '7' : [-1.07, -0.57, -0.18, 0.18, 0.57, 1.07],
                            '8' : [-1.15, -0.67, -0.32, 0, 0.32, 0.67, 1.15],
                            '9' : [-1.22, -0.76, -0.43, -0.14, 0.14, 0.43, 0.76, 1.22],
                            '10': [-1.28, -0.84, -0.52, -0.25, 0, 0.25, 0.52, 0.84, 1.28],
                            '11': [-1.34, -0.91, -0.6, -0.35, -0.11, 0.11, 0.35, 0.6, 0.91, 1.34],
                            '12': [-1.38, -0.97, -0.67, -0.43, -0.21, 0, 0.21, 0.43, 0.67, 0.97, 1.38],
                            '13': [-1.43, -1.02, -0.74, -0.5, -0.29, -0.1, 0.1, 0.29, 0.5, 0.74, 1.02, 1.43],
                            '14': [-1.47, -1.07, -0.79, -0.57, -0.37, -0.18, 0, 0.18, 0.37, 0.57, 0.79, 1.07, 1.47],
                            '15': [-1.5, -1.11, -0.84, -0.62, -0.43, -0.25, -0.08, 0.08, 0.25, 0.43, 0.62, 0.84, 1.11, 1.5],
                            '16': [-1.53, -1.15, -0.89, -0.67, -0.49, -0.32, -0.16, 0, 0.16, 0.32, 0.49, 0.67, 0.89, 1.15, 1.53],
                            '17': [-1.56, -1.19, -0.93, -0.72, -0.54, -0.38, -0.22, -0.07, 0.07, 0.22, 0.38, 0.54, 0.72, 0.93, 1.19, 1.56],
                            '18': [-1.59, -1.22, -0.97, -0.76, -0.59, -0.43, -0.28, -0.14, 0, 0.14, 0.28, 0.43, 0.59, 0.76, 0.97, 1.22, 1.59],
                            '19': [-1.62, -1.25, -1, -0.8, -0.63, -0.48, -0.34, -0.2, -0.07, 0.07, 0.2, 0.34, 0.48, 0.63, 0.8, 1, 1.25, 1.62],
                            '20': [-1.64, -1.28, -1.04, -0.84, -0.67, -0.52, -0.39, -0.25, -0.13, 0, 0.13, 0.25, 0.39, 0.52, 0.67, 0.84, 1.04, 1.28, 1.64]
                            }
        self.beta = self.breakpoints[str(self.alphabetSize)]
        self.paaTime = 0.
    

    def to_letter_rep(self, x):
        """
        Function takes a series of data, x, and transforms it to a string representation
        """
        (paaX, indices) = self.to_PAA(self.normalize(x))
        return (self.alphabetize(paaX), indices)

    def normalize(self, x):
        """
        Function will normalize an array (give it a mean of 0, and a
        standard deviation of 1) unless it's standard deviation is below
        epsilon, in which case it returns an array of zeros the length
        of the original array.
        """
        start = time.time()
        X = np.asanyarray(x)
        stdDev = X.std()
        if stdDev < self.eps:
            normalized =  [0 for entry in X]
            end = time.time()
            self.paaTime += end - start
            return normalized
        normalized =  (X-X.mean())/stdDev
        end = time.time()
        self.paaTime += end - start
        return normalized

    def to_PAA(self, x):
        """
        Function performs Piecewise Aggregate Approximation on data set, reducing
        the dimension of the dataset x to w discrete levels. returns the reduced
        dimension data set, as well as the indices corresponding to the original
        data for each reduced dimension
        """
        
        n = len(x)
        stepFloat = n/float(self.wordSize)
        step = int(math.ceil(stepFloat))
        frameStart = 0
        approximation = [0.0]*self.wordSize
        indices = [[0,0]]*self.wordSize
        i = 0
        while frameStart <= n-step:
            
            #thisFrame = x[frameStart:int(frameStart + step)]  
            #start = time.time()
            mysum = 0.
            count = 0.
            for a in range(frameStart,int(frameStart + step)):
                mysum += x[a]
                count += 1.
            
            #end = time.time()
            #approximation.append(mysum / count)
            approximation[i] = mysum / count
            
            #approximation.append(mysum / float(len(thisFrame)))
            #approximation.append(np.mean(thisFrame))
            #indices.append((frameStart, int(frameStart + step)))
            indices[i] = frameStart, int(frameStart + step)
            
            i += 1
            frameStart = int(i*stepFloat)
            
            #self.paaTime += end - start
        return (approximation, indices)

    def alphabetize(self,paaX):
        """
        Converts the Piecewise Aggregate Approximation of x to a series of letters.
        """
        alphabetizedX = ''
        for i in range(0, len(paaX)):
            letterFound = False
            for j in range(0, len(self.beta)):
                if paaX[i] < self.beta[j]:
                    alphabetizedX += chr(self.aOffset + j)
                    letterFound = True
                    break
            if not letterFound:
                alphabetizedX += chr(self.aOffset + len(self.beta))
        return alphabetizedX

    def sliding_window(self, x, windowSize = 100):
        
        self.windowSize = windowSize
        moveSize = 1
        ptr = 0
        n = len(x)
        stringRep = []

        while ptr < n-self.windowSize+1:
            thisSubRange = x[ptr:ptr+self.windowSize]
            (thisStringRep,indices) = self.to_letter_rep(thisSubRange)
            if len(stringRep) == 0 or stringRep[-1].getStringRep() != thisStringRep:
                stringRep.append(SaxTerminal(thisStringRep, (ptr, ptr+self.windowSize), len(stringRep)))
            elif len(stringRep) != 0 and stringRep[-1].getStringRep() == thisStringRep:
                stringRep[-1].addWindow((ptr, ptr+self.windowSize))
            ptr += moveSize
        return stringRep

    def set_window_size(self, windowSize):
        self.windowSize = windowSize
