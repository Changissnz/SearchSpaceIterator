"""
generates the next value to be searched and logged
"""
from hop_pattern import *
from copy import deepcopy

"""
iterator operates in a sequential/linear manner.
"""
class SearchSpaceIterator:

    """
    columnOrder := vector<column indices>, first is left head
    """
    def __init__(self,bounds, startPoint, columnOrder, SSIHop = 7,cycleOn = False, cycleIs = 0):
        assert is_proper_bounds_vector(bounds), "invalid bounds"
        assert is_vector(startPoint), "invalid start point"
        assert cycleIs in [0,1], "cycle-is is wrong"

        # TODO: check column order
        self.bounds = bounds
        self.startPoint = startPoint
        self.referencePoint = np.copy(self.startPoint)
        self.cycleIs = cycleIs# 0 for left end, 1 for right end

        self.startPointContext = self.analyze_startpoint_in_bounds()
        self.columnOrder = columnOrder # alternative: could do column weights
        self.columnOrderPtr = 0  # TODO: delete, unused.
        self.hopPatterns = []

        self.cycleOn = cycleOn
        self.ssiHop = SSIHop

        self.set_hop_pattern_for_columns(self.ssiHop)
        self.calculate_endpoint()
        self.cache = np.copy(self.startPoint)
        self.initialized = False

        # use the below variable if the cycle is on.
        self.cycleIs = cycleIs# 0 for left end, 1 for right end

        # TODO: move this code
        # adjust hop pattern heads based on `cycleIs`
        self.adjust_hop_pattern_heads()
        return

    '''
    adjusts the heads of hop pattern instances to match
    `cycleIs`
    '''
    def adjust_hop_pattern_heads(self):

        for (i,hp) in enumerate(self.hopPatterns):

            if hp.value == self.bounds[i,0] or hp.value == self.bounds[i,1]:
                hp.head = self.bounds[i,self.cycleIs]
                hp.headIndex = self.cycleIs
            else:
                pass
        return

    """
    returns vector of floats v in [0,1]
    """
    def analyze_startpoint_in_bounds(self):
        # TODO: assert start point in bounds
        v = np.asarray(self.bounds[:,1] - self.bounds[:,0], dtype=float)
        q = np.asarray(self.startPoint - self.bounds[:,0], dtype = float)
        return q / v

    def calculate_endpoint(self):

        # decrement each one
        self.endpoint = np.empty((len(self.columnOrder),))
        for (i,x) in enumerate(self.hopPatterns):
            q = deepcopy(x)
            q.rev__next__()
            self.endpoint[i] = q.rev__next__()

            # round the value to head
            q = 0 if self.cycleIs else 1
            otherV = self.bounds[i,q]
            if abs(self.endpoint[i] - otherV) < 10 ** -4.7:
                self.endpoint[i] = self.bounds[i,self.cycleIs]

        return np.round(self.endpoint,5)

    '''
    '''
    def set_hop_pattern_for_columns(self, dividor):
        for (i,c) in enumerate(self.startPoint):
            hp = HopPattern(c, self.bounds[i,0], self.bounds[i,1], DIR = round(dividor ** -1, 10))
            self.hopPatterns.append(hp)
    ###------------------------------------------------------------

    def finished(self):
        return not self.cycleOn and self.reached_end()

    def __next__(self):
        q = self.reached_end()
        if not self.cycleOn and q:
            print("done with iteration")
            return np.copy(self.referencePoint)

        # check if reached end
        self.cache = np.copy(self.referencePoint)
        if q:
            self.referencePoint = np.copy(self.bounds[:,self.cycleIs])
            copi = np.copy(self.referencePoint)
        else:
            # initialize here
            copi = self.inc1()
            self.referencePoint = copi
        return np.copy(copi)

    def rev__next__(self):
        self.referencePoint = np.copy(self.rinc1())

    def rinc1(self):

        # inishiaadoe
        q = self.initiado()

        if type(q) != type(None):
            return q

        self.cache = np.empty((self.startPoint.shape[0],))

        # increment the first hop pattern
        index = len(self.columnOrder) - 1

        x = self.hopPatterns[self.columnOrder[index]].rev__next__()
        self.cache[self.columnOrder[index]] = x

        # carry-over
        index = self.carry_over(index, "finite", True)

        # for remaining indices, add value
        for i in range(index):
            self.cache[self.columnOrder[i]] = self.hopPatterns[self.columnOrder[i]].value_at()
        return np.round(self.cache, 5)

    def initiado(self):

        if not self.initialized:
            self.initialized = not self.initialized
            for i in range(len(self.hopPatterns)):
                next(self.hopPatterns[i])
            return np.copy(self.referencePoint)
        return None

    def inc1(self):
        q = self.initiado()
        if type(q) != type(None):
            return q

        # TODO: make this reference point instead
        self.cache = np.empty((self.startPoint.shape[0],))

        # increment the first hop pattern
        index = 0
        x = next(self.hopPatterns[self.columnOrder[index]])
        self.cache[self.columnOrder[index]] = x

        # carry-over
        index = self.carry_over(index, "finite")
        diff = len(self.columnOrder) - index # TODO: error here???
        for i in range(diff):
            columnOrderIndex = index + i
            columnIndex = self.columnOrder[columnOrderIndex]
            self.cache[columnIndex] = self.hopPatterns[columnIndex].value_at()
        return np.round(self.cache, 5)

    # TODO: run tests on `carryOverType`
    """
    """
    def carry_over(self, lastIndex, carryOverType = "finite", rev = False):
        assert carryOverType in ["infinite", "finite"], "carry-over type"

        if not rev:
            lf = lambda li: True if li >= len(self.columnOrder) else False
            increment = 1
        else:
            lf = lambda li: True if li < 0 else False
            increment = -1

        # check for column carry-over
        while True:
            if carryOverType == "finite" and lf(lastIndex):
                break

            modIndex = lastIndex % len(self.columnOrder)

            # check index
            if self.hopPatterns[self.columnOrder[modIndex]].did_cycle():
                modIndex2 = (modIndex + increment) % len(self.columnOrder)

                if rev:
                    x = self.hopPatterns[self.columnOrder[modIndex2]].rev__next__()
                else:
                    x = next(self.hopPatterns[self.columnOrder[modIndex2]])
                self.cache[self.columnOrder[modIndex2]] = x
            else:
                break
            lastIndex += increment

        return lastIndex

    """
    used for rounding errors for method `HopPattern.rev__next__`
    """
    def reached_end(self):

        # minus
        diff = self.referencePoint - self.endpoint
        diffThreshold = 2 * (10 ** -5)
        diff = abs(diff)
        return np.all(diff <= diffThreshold)
