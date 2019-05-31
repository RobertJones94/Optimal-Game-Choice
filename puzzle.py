# -*- coding: utf-8 -*-
"""
Created on Tue May 28 13:51:38 2019

@author: Rob


Optiver
Quantative Researcher puzzle

https://www.optiver.com/eu/en/job-opportunities/eu-517702

A B C play a game
All choose number between 0 and 1
Whoever closest to number chosen randomly wins
 
Optimise for A
"""

import numpy as np

def CChoose(A, B, delta = 0.001):
    # this function decides where C should go given A and B
    
    # to agree with handwritten convetion x < y (traditionally A < B)
    x = min(A, B)
    y = max(A, B)
    
    # the three possible areas C can choose
    lowArea = x
    midArea = y - x
    upArea = 1 - y
   
    # half of middle area is lost to A and B automatically 
    # and D can then take one half of the parts itself leaving only quarter
    # guarenteed for C    
    
    Cpos = np.argmax([lowArea, midArea/4, upArea])
    
    if Cpos == 1:
       # middle case is easiest
       # C just chooses the middle
       C = (x + y) / 2
       
    elif Cpos == 0:
        # edge case (lower)
        
        # first check will D choose away from C regardless
        # note this can only happen if half the middle area is bigger
        if lowArea - delta < midArea/2:
            # D chooses middle Area
            # C chooses x - delta
            C = x - delta
        
        else:                   
            # ever go for away from C
            # condition comes from setting
            # wall: z < 1 - y and (x - z)/2 < 1 - y
            # between z < (y - x)/2 and (x-z)/2 < (y-x)/2
            #
            # and then combining
            DtoBandWall = x + 2*y - 2 < 1 - y
            DtoAandB = x < (3*y)/5
            
            if DtoAandB or DtoBandWall:
                # D can be forced away
                C = max(1 - y - delta, (y - x)/2 - delta)
            else:
                # D must be put between C and A
                C = 1/3 * x - delta
    
    else:
        # upper area
        
        # first check will D choose away from C regardless
        # note this can only happen if half the middle area is bigger
        if upArea + delta < midArea/2:
            # D chooses middle Area
            # C chooses x - delta
            C = y  + delta
        
        else:                   
            # ever go for away from C
            # condition comes from setting
            # wall: 1 - z < x and (z - y)/2 < x
            # between 1 - z < (y - x)/2 and (z-y)/2 < (y-x)/2
            #
            # and then combining
            DtoAandWall = 1 - x < 2*x + y
            DtoAandB = 2 + 2*x < 3*y
            
            if DtoAandB or DtoAandWall:
                # D can be forced away
                C = min(1 - x + delta, 1 - (y - x)/2 + delta)
            else:
                # D must be put between C and A
                C = y + 2/3 *(1 - y) + delta

    return(C)
                

def DChoose(A,B,C, delta = 0.001):
    # this part chooses D
    # note that as D can potentially have multiple options we take this into account
    # we must return a list
    
    # sort them.. note convention is x < z < y
    vals = np.sort([0,A,B,C,1])
    x = vals[1]
    y = vals[3]
    
    # Get areas available to D. middle areas only worth half
    areas = np.diff(vals)
    areas[1:3] /= 2
    
    # care is needed here.. D will often have more than one option
    # as we are searching for optimal choice
    # we need to include the possible D values
    
    maxArea = max(areas)
    maxLocs = [i for i, num in enumerate(areas) if abs(num - maxArea) < delta*0.0001]
    D = []
    for Dloc in maxLocs:
        if Dloc == 0:
            # edge lower
            D += [x - delta]
        elif Dloc == 3:
            # edge upper
            D += [y + delta]
        else:
            # one of the middle sections
            mids = (vals[1:] + vals[:-1])/2
            D += [mids[Dloc]]
    
    return(D)
    
def Areas(A,B,C,D):
    # this function gets the areas attributed to each A,B,C,D
    # returns array containing area in that same order
    # note D is a list of all possible D values
    # we get the average area for A, B, C in this case
    
    # areaList a list of lists, where each sublist is the aras of A,B,C,D in order
    areaList = []
    for d in D:
        line = [A, B, C, d]
        lineSorted = np.sort(line)
        
        # keep track of the indices.. find better way to do this!
        # system is [sorted pos] in position of original position
        index = []
        for ii in range(4):
            for jj in range(4):
                if line[ii] == lineSorted[jj]:
                    index += [jj]
        
        # get midpoints
        mids = (lineSorted[1:] + lineSorted[:-1]) / 2
        
        fullLine = np.concatenate(([0],mids,[1]))
        areas = np.diff(fullLine)
        areaList += [list(areas[index])]
        
    # now A and B do not want to risk a zero
    # this part is basically trying to capture the idea that D can have multiple
    # values.
    # The idea is that if A could get flanked by D it will never choose it
    # also with B
    # those that are not getting flanked by D then look at the minimum
    # area they're going to get (Assuming D picks their side)
    if any(x < 3*delta for row in areaList for x in row[:2] ):
        finalList = np.array([0,0,0,0])
    else:
        finalList = np.array(areaList).min(0)
    
    return(finalList)
    

# note we're starting B a little offset to ensure we don't have a tie with A
delta = 0.001
Avals = np.arange(0.0001, 0.5, delta)
Bvals = np.arange(0.999, 0, -delta)



areas = []
# C is the chooser here
# D always chooses max area  

# A wants max but is conditioned by B (which is conditioned by C)
maxA = 0
for A in Avals:
    maxB = 0
    maxC = 0
    for B in Bvals:
        if A == B:
            continue
        
        C = CChoose(A, B, delta)
        D = DChoose(A, B, C, delta)
        
        tmp =  Areas(A,B,C,D)
        # keep track of the areas of A,B,C and which combination of A,B yielded it
        areas += [np.concatenate((np.array([A,B,C]), tmp))]
        
        if tmp[1] >= maxB:
            # get the max B for given A
            maxB = tmp[1]

            if tmp[0] >= maxA:
                # if A is a max and 
                maxA = tmp[0]
                maxC = tmp[2]
                maxAID = A
                maxBID = B
                maxCID = C
                
                

# the optimal choice for A B and then C
print('Optimal Choice for A = ' + str(maxAID))
print('Optimal Choice for B = ' + str(maxBID))
print('Optimal Choice for C = ' + str(maxCID))