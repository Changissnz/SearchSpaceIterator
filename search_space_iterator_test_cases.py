from search_space_iterator import *


def SearchSpaceIterator_case_1():

    bounds = np.array([[0,1],\
                    [0,1],\
                    [0,1]
        ])
    startPoint = np.array([0,1,0])

    # TODO: test w/ this column order
    columnOrder = [0,1,2]
    return SearchSpaceIterator(bounds, startPoint, columnOrder, 2)

def SearchSpaceIterator_case_2():
    bounds = np.array([[0,1],\
                    [0,1],\
                    [0,1]
        ])
    startPoint = np.array([0,0,0])

    # TODO: test w/ this column order
    columnOrder = [2,0,1]
    return SearchSpaceIterator(bounds, startPoint, columnOrder, 5)

def SearchSpaceIterator_case_3():
    bounds = np.array([[0,1],\
                    [0,1],\
                    [0,1]
        ])
    startPoint = np.array([0,0,0])

    # TODO: test w/ this column order
    columnOrder = [0,1,2]
    return SearchSpaceIterator(bounds, startPoint, columnOrder, 3)

def SearchSpaceIterator_case_4():
    bounds = np.array([[0,1],\
                    [0,1],\
                    [0,1],\
                    [0,1],\
                    [0,1]])

    startPoint = np.array([0.0,0.5,0.3, 1,0.75])
    columnOrder = [4,2,0,1,3]
    HopPattern.DEF_INCREMENT_RATIO = round(1/7,10)
    return SearchSpaceIterator(bounds, startPoint, columnOrder,\
        7, "proportional")

def SearchSpaceIterator_case_5():
    ssi = SearchSpaceIterator_case_4()
    HopPattern.DEF_INCREMENT_RATIO = round(1/4,2)
    return ssi

def SearchSpaceIterator_case_6():

    bounds = np.array([[0,10],\
                    [0,10],\
                    [0,10.00],\
                    [0,10],\
                    [0,10.00]])

    startPoint = np.array([5.0, 4.0, 3.0, 8.0, 7.5])
    columnOrder = [4,2,0,1,3]
    ssih = 2
    return SearchSpaceIterator(bounds, startPoint, columnOrder, ssih)

def SearchSpaceIterator_case_7():

    bounds = np.array([[0,10],\
                    [0,10],\
                    [0,10.00],\
                    [0,10],\
                    [0,10.00]])

    bounds = invert_bounds(bounds)
    startPoint = np.array([5.0, 4.0, 3.0, 8.0, 7.5])
    columnOrder = [4,2,0,1,3]
    ssih = 2
    return SearchSpaceIterator(bounds, startPoint, columnOrder, ssih)





########
