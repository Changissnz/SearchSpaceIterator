from globalls import *
import numpy as np
import math

def equal_iterables(i1, i2, roundPlaces = 5):

    if len(i1) != len(i2): return False
    if np.all(np.equal(np.round(i1, roundPlaces), np.round(i2, roundPlaces)) == True): return True
    return False

def is_2dmatrix(m):
    if type(m) is not np.ndarray: return False
    if len(m.shape) != 2: return False
    return True

def is_bounds_vector(b):
    q = is_2dmatrix(b)
    if not q: return q
    return b.shape[1] == 2

def is_vector(m):
    if type(m) is not np.ndarray: return False
    if len(m.shape) != 1: return False
    return True

def is_valid_point(point):
    assert not type(point) is np.ndarray, "point cannot be np.ndarray"
    if len(point) != 2: return False
    if not type(point[0]) in [int, float, np.int64, np.float64]: return False# or type(point[0]) is float): return False
    if not type(point[1]) in [int, float, np.int64, np.float64]: return False
    return True

######## start: some methods on bounds

"""
return:
- (start)::float,(end)::float,(distance)::float
"""
def largest_subrange_of_coincidence_between_ranges(r1,r2, roundDepth = 5, hop = 0.05):
    assert hop > 0, "hop > 0!"

    # sort
    assert len(r1) == 2 and len(r2) == 2, "invalid ranges {} and {}".format(r1,r2)
    r1,r2 = sorted(r1), sorted(r2)

    coin = False
    longest = 0.0
    start, end = float('inf'), float('inf')
    now = 0.0
    startN, endN = float('inf'), float('inf')

    q = r1[0]
    while q <= r1[1]:
        # coincides
        if q >= r2[0] and q <= r2[1]:
            # start coincidence
            if not coin:
                coin = True
                now = 0.0
                startN = q
                endN = float('inf')

            # update coincidence
            else:
                now += hop
                endN = q

        # no longer coincides
        else:
            if coin:
                coin = False
                if now > longest:
                    longest = now
                    start,end = startN, endN

                startN,endN = float('inf'), float('inf')

        q = round(q + hop, roundDepth)

    # update longest
    if now > longest:
        longest = now
        start,end = startN, endN

    return round(start, roundDepth) , round(end, roundDepth), round(longest, roundDepth)

'''

'''
def intersection_of_bounds(b1,b2):
    # check for each column
    assert is_2dmatrix(b1) and is_2dmatrix(b2),"invalid bounds {}\n\n\t{}".format(b1,b2)
    assert b1.shape == b2.shape, "must have equal shape"

    # check for each index
    bx = []
    for i in range(b1.shape[0]):
        q1,q2 = b1[i],b2[i]
        start,end,dist = largest_subrange_of_coincidence_between_ranges(q1,q2,5,DEFAULT_TRAVELLING_HOP)
        if dist != 0:
            bx.append([start,end])
        else:
            return None
    return np.array(bx)

def subbound_of_bound(b, boundRange):
    assert is_2dmatrix(b), "invalid type for bounds"
    assert b.shape[1] == 2, "invalid shape for bounds"

    assert is_valid_point(boundRange), "[0] invalid bound range"
    assert np.all(np.array(boundRange) >= 0) and np.all(np.array(boundRange) <= 1), "[1] invalid bound range"
    assert len(boundRange) == 2, "[2] invalid bound range"

    diff = b[:,1] - b[:,0]

    s = b[:,0] + (diff * boundRange[0])
    e = b[:,0] + (diff * boundRange[1])
    return np.vstack((s,e)).T

def n_partition_for_bound(b, partition):

    q = (b[:,1] - b[:,0]) / float(partition)
    x0 = np.copy(b[:,0])
    partition = [x0]
    for i in range(partition):
        x1 = x0 + q
        x0 = np.copy(x1)
        partition.append(x0)
    return partition


def invert_bounds(b):
    assert is_bounds_vector(b), "invalid bounds vector"
    b2 = np.empty((b.shape[0],2))

    b2[:,0] = np.copy(b[:,1])
    b2[:,1] = np.copy(b[:,0])
    return b2

def to_proper_bounds_vector(b):
    assert is_bounds_vector(b), "invalid bounds vector"

    b2 = np.empty((b.shape[0],2))
    b2[:,0] = np.min(b,axis=1)
    b2[:,1] = np.max(b,axis=1)
    return b2

def is_proper_bounds_vector(b):
    assert is_bounds_vector(b), "invalid bounds vector {}".format(b)
    return np.all(b[:,0] <= b[:,1])

def partial_invert_bounds(b, indices):
    return -1

######## end: some methods on bounds
