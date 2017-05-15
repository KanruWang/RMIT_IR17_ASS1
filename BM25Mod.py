"""
The object representation of the BM25 algorithm, all related calculations
are handled and returned from here:

"""
# import built-in libraries and data structures
import math

class BM25:
    def __init__(self, totalDocCount, avgDocLength):
        # ==== initial algorithm constants, params given at instantiation ====
        # k1 & b
        self._const_k1 = 1.2
        self._const_b = 0.75
        # N: Total number of docs in collection
        if totalDocCount is not None:
            self._const_N = int(totalDocCount)
        # AL: Average Doc Length, should be calculated at initial query time
        if avgDocLength is not None:
            self._const_AL = float(avgDocLength)

    """
    This function gets called in the ranking module, should return the
    similarity score for a specific document D; follows the BM25 algo.
    Params passed:
    1. queryTerms = a List() of processed QueryTerm tuples => [(xx,xx), (yy,yy)...]
        1.1 Tuple content: (f_dt, f_t);
        f_dt = number of occurrences of t in d
        f_t = the number of documents containing term t
    2.L_d: document length

    check the BM25 algo for details

    In case the input of a number is a string, int() turns a string into an integer;
    it gives an error when passed with an empty string or a decimal;
    it gives a zero when passed with a null reference.
    """
    def getSimScore(self, f_dt, f_t, Ld):
        # the final calculated score to return to the caller
        finalScore = 0
        if Ld is not None:
            Ld = int(Ld)
        K = self._const_k1 * ((1. - self._const_b) + self._const_b * Ld / self._const_AL)
        f_dt = int(f_dt)
        f_t = int(f_t)
        #print f_dt, f_t
        finalScore = (math.log10((self._const_N - f_t + 0.5)/(f_t + 0.5))) * ((self._const_k1 + 1.) * f_dt / (K + f_dt))
        #print finalScore
        return finalScore

    # ... other functions that separate the behaviors ...
    def getWeightedScore(self, w_t, f_dt, Ld):
        finalScore = 0
        if Ld is not None:
            Ld = int(Ld)
        K = self._const_k1 * ((1. - self._const_b) + self._const_b * Ld / self._const_AL)
        finalScore = w_t * ((self._const_k1 + 1.) * f_dt / (K + f_dt))
        return finalScore