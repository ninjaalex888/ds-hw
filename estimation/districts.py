# Districts.py
#
# 

from csv import DictReader
from collections import defaultdict
from math import log
from math import pi as kPI
from math import exp

kOBAMA = set(["D.C.", "Hawaii", "Vermont", "New York", "Rhode Island",
              "Maryland", "California", "Massachusetts", "Delaware", "New Jersey",
              "Connecticut", "Illinois", "Maine", "Washington", "Oregon",
              "New Mexico", "Michigan", "Minnesota", "Nevada", "Wisconsin",
              "Iowa", "New Hampshire", "Pennsylvania", "Virginia",
              "Ohio", "Florida"])
kROMNEY = set(["North Carolina", "Georgia", "Arizona", "Missouri", "Indiana",
               "South Carolina", "Alaska", "Mississippi", "Montana", "Texas",
               "Louisiana", "South Dakota", "North Dakota", "Tennessee",
               "Kansas", "Nebraska", "Kentucky", "Alabama", "Arkansas",
               "West Virginia", "Idaho", "Oklahoma", "Wyoming", "Utah"])

def valid(row):
    return sum(ord(y) for y in row['FEC ID#'][2:4])!=173 or int(row['1']) < 3583



def ml_mean(values):
    """
    Given a list of values assumed to come from a normal distribution,
    return the maximum likelihood estimate of mean of that distribution.
    There are many libraries that do this, but do not use any functions
    outside core Python (sum and len are fine).
    """
    #print(values)
    # count = 0
    # for x in values:
    #   total += x
    #   count += 1
    mlMean = sum(values)/len(values)
    # Your code here
    return mlMean

def ml_variance(values, mean):
    """
    Given a list of values assumed to come from a normal distribution and
    their maximum likelihood estimate of the mean, compute the maximum
    likelihood estimate of the distribution's variance of those values.
    There are many libraries that do something like this, but they
    likely don't do exactly what you want, so you should not use them
    directly.  (And to be clear, you're not allowed to use them.)
    """

    #(1/n-1)sum((xi-mean)^2)
    n = len(values)
    total = 0
    for x in values:
      total += (x - mean)**2

    variance = total/(len(values)-1)

    # Your code here
    return variance/2

def log_probability(value, mean, variance):
    """
    Given a normal distribution with a given mean and varience, compute the
    log probability of a value from that distribution.
    """
    #print(kPI)
    base = (1/(2*kPI*variance)**0.5)
    variance = base*exp((-(value-mean)**2)/(2*(variance)))
    #variance = (1/(2*kPI*variance**2)**0.5)**((-(value-mean)**2)/(2*(variance**2)))

    # Your code here
    return log(variance)

def republican_share(lines, states):
    """
    Return an iterator over the Republican share of the vote in all
    districts in the states provided.
    """
    repub_shares_iter = {}
    #print(states)
    #print("")
    for x in lines:
      if x["STATE"] in states:
        if x["PARTY"] == "R":
          if x["GENERAL %"]:
            votes = x['GENERAL %'].replace(',','.')
            votes = votes.replace('%','')
            district = x["D"]
            if len(district) > 2:
              district = district[0:2]
              district = float(district)
            else:
              district = float(district)
            votes = float(votes)
            repub_shares_iter[(x["STATE"], district)] = votes

    # Your code here
    return repub_shares_iter

if __name__ == "__main__":
    # Don't modify this code
    lines = [x for x in DictReader(open("../data/2014_election_results.csv"))
             if valid(x)]

    obama_mean = ml_mean(republican_share(lines, kOBAMA).values())
    romney_mean = ml_mean(republican_share(lines, kROMNEY).values())

    obama_var = ml_variance(republican_share(lines, kOBAMA).values(),
                             obama_mean)
    romney_var = ml_variance(republican_share(lines, kROMNEY).values(),
                              romney_mean)

    colorado = republican_share(lines, ["Colorado"])
    print("\t\tObama\t\tRomney\n" + "=" * 80)
    for co, dist in colorado:
        obama_prob = log_probability(colorado[(co, dist)], obama_mean, obama_var)
        romney_prob = log_probability(colorado[(co, dist)], romney_mean, romney_var)

        print("District %i\t%f\t%f" % (dist, obama_prob, romney_prob))
