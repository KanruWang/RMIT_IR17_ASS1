# RMIT_IR17_ASS1
**Proudly coded by: Ryan Jiang**

####Team:

Yuanqing Jiang S3289950 

Yuwei Zhang S3492095

#### The code is written in Python, so invoke the program with the following commands:

(The code is well commented for further review.)
#### With indexing:


`python index.py [-s <stoplist>] [-p] <sourcefile>`

#### With searching:
`python search.py lexicon invlists map <QueryTerm>...`

#### Output Files:

* lexicon
* map
* invlists

#### Debug output file:

* testLexi

#### Custom Data structures:

* util.py

---------------

# RMIT_IR17_ASS2
## Team:
Yuanqing Jiang S3289950

Kanru Wang S3559697

## Invoke commands:

#### 1. Indexing:
`Same as in Ass1`
#### 2. Ranked Search
*1. Boolean query search has been replaced with this Ranked Search Module*

*2. Given the complexity of the invoke commands we assume that the user will always input the correct commands to start the application*

`python search.py -BM25 -q <query-label> -n <num-results> -l <lexicon> -i<invlists> -m <map> [-s <stoplist>] <queryterm-1> [<queryterm-2> ...<queryterm-N>]`

#### 3. Okapi Query Expansion
*1. This module is built on top of Ranked Search, so the change of the first invoke parameter -BM25 to -OkapiExp will invoke the auto query expansion*

*2. The module will take 2 additional parameters with flags: -r & -e, as required in the assignment sheet* 

*3. Again we assume that the user will input correct flags and parameters to run the application*`python search.py -OkapiExp -q <query-label> -n <num-results> -l <lexicon> -i<invlists> -m <map> -r <R-top-ranked> -e <NumberOf-E-terms> [-s <stoplist>] <queryterm-1> [<queryterm-2> ...<queryterm-N>]`