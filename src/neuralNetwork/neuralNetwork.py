def normalizeInputs(xDist, yDist):
    #normalize the inputs to be between 0 and 1
    
    xDist /= 193    # max distance (actually 439 at startup. let's see how it goes)
    
    # max distance (difference of position) between the bird and the gap
    yDist /= 393    # this is between -1 and 1 (gap at top with bird at bottom - vice versa), so:
    # let's normalize it to be between 0 and 1
    yDist = (yDist + 1) / 2 # yDist is 0.5 when bird and gap are aligned vertically

    return xDist, yDist
