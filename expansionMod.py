import heapq
import math

class ExpansionModule:
    def __init__(self, lexicon, totalDoc, R_docs, E_terms):
        self.lexicon = lexicon
        self.totalDoc = totalDoc
        self.R_docs = int(R_docs)
        self.E_terms = int(E_terms)

    # first we need a bag of candidate terms, which is tough
    def getCandidateTerms(self, rankHeap, originalQuery):
        # set up the parameters from the class attributes
        N_docs = self.totalDoc
        R_docs = self.R_docs
        E_terms = self.E_terms

        # get the R_docs first
        relevantDocs = []
        for i in range(R_docs):
            try:
                invScore, docID = heapq.heappop(rankHeap)
                relevantDocs.append(docID)
            except IndexError:
                break
        # Now we get ALL the candidate terms in these docs
        # Hell do I have to through every single lexicon & invList?
        termHeap = []
        for termKey,termItem in self.lexicon.lexiTable.iteritems():
            # for each termItem, go through its invList
            f_t = termItem.getFreq()
            r_t = 0
            for docID,docFreq in termItem.getInvList().toIterative():
                # check if the term is in the R_docs
                if docID in relevantDocs:
                    r_t += 1
            # now we have f_t and r_t
            # so we have the TSV for the term
            if r_t == 0:
                # if the term is not in the relevant docs at all
                continue
            else:
                TSV_t = self.calculateTSV(f_t, r_t, N_docs, R_docs)
                # only the expanded term has the weight downgraded by 1/3, others with 0
                if termKey not in originalQuery:
                    # ! this weight should be stored in the same lexicon
                    # ! that can be accessed from other modules
                    termItem.weight = self.calculateTermWeight(f_t, r_t, N_docs, R_docs)
                # store the term and its TSV in a heap
                # ! Pushing termItem rather than termKey
                heapq.heappush(termHeap, (TSV_t, termItem))
            # and min heap in python always returns the smallest
        # now its time to only select E number of terms
        selectedTerms = []
        for j in range(E_terms):
            tsv,termItem = heapq.heappop(termHeap)
            # ! because we have already changed the weight of terms
            # ! in the lexicon that is universally accessed by mods
            # ! we just append the term string here
            selectedTerms.append(termItem.term)
            # debug: print the selected:
            print "SELECTED Terms: ", tsv, termItem.term
        # now we have the correct list of terms
        # add the original terms as well
        selectedTerms += originalQuery
        return selectedTerms

    def calculateTSV(self, f_t, r_t, N_docs, R_docs):
        # the calculation is NOT final yet!
        # the lecture slides suggest factorial but I think its quite large
        TSV_t = ((f_t / N_docs) ** (r_t)) * (R_docs / (r_t*(R_docs-r_t)))
        return TSV_t

    def calculateTermWeight(self, f_t, r_t, N_docs, R_docs):
        upper = (r_t + 0.5) * (N_docs - f_t + r_t + 0.5)
        lower = (f_t - r_t + 0.5) * (R_docs - r_t + 0.5)
        # modified downward for 1/3 to avoid domination?
        # not too sure about this
        w_t = math.log10(upper / lower) * 0.33
        return w_t