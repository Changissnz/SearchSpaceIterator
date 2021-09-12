from matrix_methods import *
import math

"""
class uses a 1-d number line as reference
number line is finite between `minBound` and `maxBound`.
"""
class HopPattern:

    DEF_INCREMENT_RATIO = 0.5

    DEFAULT_TRAVEL_DIRECTION = 1 # | -1

    def __init__(self, initialValue, minBound, maxBound, cycleLog = False, DIR = 0.2):

        self.value = initialValue
        self.ptrValue1,self.ptrValue2 = self.value,None
        self.bounds = [minBound,maxBound]

        ### TODO: mod here
        self.bounds = [min(self.bounds),max(self.bounds)]
        self.DIR = DIR

        # cycle counter
        self.cycleCounter = 0
        self.cycled = False
        self.hopDirection = None
        self.initialized = False
        self.head = None
        self.headIndex = None
        self.calculate_hop_directions()
        self.elementCount = 0

        self.cycleLogActive = cycleLog
        self.cycleLog = []

        return

    def clear_pointer_values(self):
        self.ptrValue1,self.ptrValue2 = None,None
        self.ptrAlternator = None

    ############## start: declaring hop directions

    def head_(self):
        return self.value

    """
    description:
    - hop direction shape will vary if cycle is doubly-hopped.

    ## (hopfloat, hopbound)_L, (hopfloat, hopbound)_R

    """
    def calculate_hop_directions(self):
        self.clear_pointer_values()

        if self.value == self.bounds[0]:
            self.hopDirection = np.array([float(self.bounds[1] - self.bounds[0]) * self.DIR,\
                                self.bounds[1]])

        elif self.value == self.bounds[1]:
            self.hopDirection = np.array([float(self.bounds[0] - self.bounds[1]) * self.DIR,\
                                self.bounds[0]])

        else:
            dir = self.DIR * HopPattern.DEFAULT_TRAVEL_DIRECTION
            self.hopDirection = np.array([float(self.bounds[1] - self.bounds[0]) * dir,\
                                self.bounds[1]])

        self.ptrValue1 = self.value
        self.head = self.head_()

    """
    length of cycle is number of iterations required to cross the bounds
    """
    def length_of_cycle(self):
        return math.ceil(abs(self.bounds[1] - self.bounds[0]) / self.hopDirection[0])

    #TODO:
    def set_manual_hop_direction(self, hopDirection):
        return

    ############## end: declaring hop directions
    def __next__(self):
        if not self.initialized:
            self.initialized = not self.initialized
            self.elementCount += 1
            if self.cycleLogActive:
                self.cycleLog = [self.value]
            return self.value

        return self.hop_one()

    """
    description:
    - reverse-next
    """
    def rev__next__(self):
        if not self.initialized:
            self.initialized = not self.initialized
            self.elementCount += 1
            return self.value
        return self.hop_one(True)

    def value_at(self):
        # case: double
        if self.hopDirection.shape == (2,2):
            if not self.ptrAlternator:
                b = np.array([self.bounds[0], self.value])
                return HopPattern.modulo_hop(self.ptrValue1, 0.0,b,1)
            b = np.array([self.value, self.bounds[1]])
            return HopPattern.modulo_hop(self.ptrValue2, 0.0, b, 0)

        # case: single
            # l -> r
            # r -> l
        head = 0 if self.hopDirection[0] >= 0 else 1
        return HopPattern.modulo_hop(self.ptrValue1, 0.0, self.bounds, head)

    """
    calculates the reverse of hop directions
    """
    def reverse_directions(self):
        return np.array([-self.hopDirection[0], self.hopDirection[1]])

    """
    hops one
    """
    def hop_one(self, rev = False):
        q = np.copy(self.hopDirection) if not rev else self.reverse_directions()

        if self.headIndex == None:
            # make assumption based on hop direction
            head = 0 if q[0] >= 0.0 else 1
        else:
            head = self.headIndex
        q2 = HopPattern.modulo_hop(self.ptrValue1, q[0], self.bounds, head)

        self.ptrValue1 = q2
        self.elementCount += 1

        # logs value if logging is on
        if self.cycleLogActive:
            if self.did_cycle():
                self.cycleLog = [q2]
            else:
                self.cycleLog.append(q2)
        return q2

    """
    set n = 5

    to solve over-rounding errors:
        n_ = n + 2
    to solve under-rounding errors:
        n_ = n - 2

    round value to three place
    """
    @staticmethod
    def boundary_round_value(value, bounds):
        # try rounding
        v = round(value,3)

        if abs(bounds[0] - v) <= 10 ** -3: # 5
            return bounds[0]

        elif abs(bounds[1] - v) <= 10 ** -3: # 5
            return bounds[1]
        return value

    """
    'hops' the value by modulo: if hop is on
    the non-head bound,

    """
    @staticmethod
    def modulo_hop(value, hop, bounds, head):
        assert head in [0,1], "invalid head {}".format(head)

        v = value
        value = round(value + hop,5)
        value = HopPattern.boundary_round_value(value, bounds)
        # case: value at [0] or [1], endpoints,
        if value == bounds[0]:
            if head: value = bounds[1]
        elif value == bounds[1]:
            if not head: value = bounds[0]

        # case: value below [0]
        elif value < bounds[0]:
            diff = value - bounds[0]
            value = round(bounds[1] + diff,5)

        # case: value above [1]
        elif value > bounds[1]:
            diff = value - bounds[1]
            value = round(bounds[0] + diff,5)
        else:
            pass
        return round(value,5)

    ################### start: cycle checker

    def did_cycle(self):
        if not self.initialized: return self.initialized
        return True if abs(self.head - self.ptrValue1) < 10 ** -3 and self.elementCount > 1 else False

    """
    checks for cycle and updates pointer values to their modulo versions.
    """
    # TODO: check modulo_hop for head
    def cycle_check(self):
        if self.did_cycle():
            self.cycleCounter += 1
            return True
        return False

    """
    """
    def percentage_of_cycle_run(self):
        # double
        if self.hopDirection.shape == (2,2):
            # get % left
            left = (self.value - self.ptrValue1) / (self.value - self.bounds[0])

            # get % right
            right = (self.ptrValue2 - self.value) / (self.bounds[1] - self.value)
            return left, right

        #single
        else:
            return (self.ptrValue1 - self.bounds[0]) / (self.bounds[1] - self.bounds[0])

    ################### end: cycle checker

'''
'''
def cycle_hop_pattern(hopPattern):
    l = []
    while not hopPattern.did_cycle():
        q2 = next(hopPattern)
        l.append(q2)

    return np.round(np.array(l), 5)
