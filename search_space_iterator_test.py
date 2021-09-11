from search_space_iterator_test_cases import *
import unittest

# TODO: write tests on inverted bounds [1,0]

def test__SearchSpaceIterator__set_hop_pattern_fo():
    HopPattern.DEF_INCREMENT_RATIO = 0.5
    ssi = SearchSpaceIterator_case_1()
    ssi.set_hop_pattern_for_columns()

    for (i,x) in enumerate(ssi.hopPatterns):
        print("hop for ", i)
        print(x.hopDirection)
        print()

class TestSearchSpaceIteratorClass(unittest.TestCase):


    def test__SearchSpaceIterator__next__1(self):

        ssi = SearchSpaceIterator_case_1()

        """
        make sure cycle of correct length
        """
        c = 0
        while True:
            c += 1
            next(ssi)
            #print(next(ssi))
            if ssi.reached_end(): break
        assert c == 8, "c is wrong"

    """
    write data out to file
    `message_data/search_space/ssi_case_2.txt`
    """
    def test__SearchSpaceIterator__next__2(self):

        # case 2
        ssi2 = SearchSpaceIterator_case_2()
        ssi2.cycleOn = True

        # check correct endpoint
        ##print("endpoint: ", ssi2.endpoint)
        assert equal_iterables(ssi2.endpoint,np.array([0.8,0.8,0.8])), "invalid endpoint"

        # check correct number of elements in cycle
        # loop entirely
        c = 0
        while True:
            c += 1
            next(ssi2)
            #print(next(ssi2))
            if ssi2.reached_end(): break
        assert c == 125, "incorrect number of elements {}".format(c)

    def test__SearchSpaceIterator__next__3(self):

        ssi3 = SearchSpaceIterator_case_3()

        c = 0
        while c < 1000:
            c += 1
            next(ssi3)
            #print(next(ssi3))
            if ssi3.reached_end(): break
        assert c == 27, "c turns out to be more wrong than right"
        return

    '''
    '''
    def test__SearchSpaceIterator__next__4(self):
        ssi = SearchSpaceIterator_case_4()
        ssi.cycleIs = 1
        ssi.adjust_hop_pattern_heads()

        # print out hop pattern for each
        cycleLengths = []
        for hp in ssi.hopPatterns:
            s = cycle_hop_pattern(hp)
            cycleLengths.append(len(s))

        # all are length 7
        cycleLengths = np.array(cycleLengths)
        assert np.all(cycleLengths == cycleLengths[0])
        return

#-------------------------------------------------------------

    '''
    checks that the endpoint is correct for SSI case 6.
    '''
    def test__SearchSpaceIterator__CASE_6_endpoint(self):
        ssi = SearchSpaceIterator_case_6()
        sol = np.array([0.,9.,8.,3.,2.5])
        assert equal_iterables(ssi.endpoint,sol), "incorrect endpoint for case 6"

    def test__SearchSpaceIterator__rev__next__(self):
        ssi = SearchSpaceIterator_case_6()
        ssi.cycleOn = True
        ssi.cycleIs = 0

        q = [np.copy(ssi.referencePoint)]
        c = 0
        while not ssi.reached_end():
            ssi.rev__next__()
            q.append(np.copy(ssi.referencePoint))
            c += 1

            if c == 100:
                break
        assert c == 32, "[0] incorrect number of elements for search space"

        q = np.unique(q,axis = 0)
        assert q.shape[0] == 32 and q.shape[1] == 5, "[0] incorrect shape of q"

        # forward loop
        c = 1
        q = [np.copy(next(ssi))]
        while not ssi.reached_end():
            q.append(np.copy(next(ssi)))

            ##print("V ", next(ssi), "\tF ", ssi.reached_end())
            c += 1
            if c == 100:
                break

        assert c == 32, "[1] incorrect number of elements for search space"
        q = np.unique(q,axis = 0)
        assert q.shape[0] == 32 and q.shape[1] == 5, "[0] incorrect shape of q"


    # FAILS:
    def test__SearchSpaceIterator__rev__next__2(self):
        stat = True

        try:
            ssi = SearchSpaceIterator_case_7()
            stat = not stat
        except:
            pass

        assert stat, "invalid bounds for SSI 7"
        return

# TODO
def test__SearchSpaceIterator__rinc1():
    HopPattern.DEF_INCREMENT_RATIO = 0.5
    ssi = SearchSpaceIterator_case_1()

    # TODO: 
    ssi.cycleIs = 1
    ssi.adjust_hop_pattern_heads()

    for i in range(10):
        q = ssi.rev__next__()
        #next(ssi)
        #print("Q: ",ssi.referencePoint)

    """
    print("forwarding then ")
    q = ssi.inc1()
    print("q: ", q)

    q = ssi.inc1()
    print("q: ", q)
    return
    """

if __name__ == "__main__":
    unittest.main()
