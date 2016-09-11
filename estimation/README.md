
Estimating Distribution Parameters
===============

Overview
---------------

This program will be autograded.  That means that it's important to
not change function names and to not add additional functionality that
may improve the program but produce different results.  Make sure that
your unit tests pass.  This what a successful set of unit tests will
look like:

    $ python3 tests.py
    .....
    ----------------------------------------------------------------------
    Ran 5 tests in 0.002s
    
    OK

District Margins (15 points)
----------------------------

In the US, our legislature is made up of representatives of individual
*districts* (unlike proportional representation systems).  Some of
these districts are competitive, meaning that the winner of the
election is not a "sure thing" based on the voters in the districts.
However, for a variety of reasons, many of these districts are not
very competitive.  

Words Presidents Use (15 points)
-------------------------------

Each year, the president of the United States is required to make a
speech to congress describing the "State of the Union".  We are going
to create a simple *bigram language model* with *add one (Laplace)*
smoothing.

Writeup (10 points)
-----------------------

Finally, include a brief plain-text file (not PDF, not Word, just a
plain ASCII text file) that:
* Describes whether Colorado's congression districts look more like
  the congressional districts of states that Obama won or that Romeny
  won
* Plot a
  [histogram](http://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html)
  of both the Obama and Romney states.  Is it resonable to assume that
  these are a normal distribution?
* Gives an interesting example of a *word* that Obama said that no
  previous president said
* Gives an interesting example of a *bigram* that Obama said that no
  previous president said
* The code prints out the probability of each president who is not a
  Republican or Democrat gave a speech associated with one of the
  parties.  Investigate why this happened for at least one president's
  speech.

Submitting Your Code
-----------------------

You'll need to submit your assignment (lm.py, districts.py, histogram.png,
and writeup.txt) on
[Moodle](https://moodle.cs.colorado.edu/course/view.php?id=49) as an
upload.
