from collections import defaultdict
from csv import DictReader, DictWriter
import csv
import heapq

kHEADER = ["STATE", "DISTRICT", "MARGIN"]

def district_margins(state_lines):
    """
    Return a dictionary with districts as keys, and the difference in
    percentage between the winner and the second-place as values.

    @lines The csv rows that correspond to the districts of a single state
    """
    #print(state_lines)
    margins = {}
    district_votes = []
    districts = []
    for row in state_lines:
        districts.append(row['D'])
    districts.remove('H')
    districts = filter(None, districts)
    districts = list(districts)
    for x in set(districts):
        for row in state_lines:
            if row['D'] == x:
                if(row['GENERAL %']):
                    votes = row['GENERAL %'].replace(',','.')
                    votes = votes.replace('%','')
                    district_votes.append(float(votes))
                    #print(row['GENERAL VOTES '])
        firstPlace = max(district_votes)
        district_votes.remove(firstPlace)
        secondPlace = max(district_votes)
        #print("First is " + str(firstPlace) + " Second is " + str(secondPlace))
        margin = firstPlace-secondPlace
        margins[int(x)] = margin
    # Complete this function
    #return dict((int(x["D"]), 25.0) for x in state_lines if x["D"] and x["D"] != "H")
    return margins

def all_states(lines):
    """
    Return all of the states (column "STATE") in list created from a
    CsvReader object.  Don't think too hard on this; it can be written
    in one line of Python.
    """

    listOfStates = []
    for row in lines:
        listOfStates.append(row['STATE'])
    if None in listOfStates: listOfStates.remove(None)
    #print(set(listOfStates))
    #print(set(["Alaska"]))


    # Complete this function
    return set(listOfStates)

def all_state_rows(lines, state):
    """
    Given a list of output from DictReader, filter to the rows from a single state.

    @state Only return lines from this state
    @lines Only return lines from this larger list
    """
    
    #print("STATE IS " + state)
    listStateRows = []
    for row in lines:
        #print("STATE IS " + state + " Lines is " + row['STATE'])
        if row['STATE'] == state:
            listStateRows.append(row)
        
    #print(listOfStates)
    # Complete/correct this function
    # sfor ii in lines[:10]:
    #     yield ii
    return listStateRows

if __name__ == "__main__":
    # You shouldn't need to modify this part of the code
    lines = list(DictReader(open("../data/2014_election_results.csv")))
    output = DictWriter(open("district_margins.csv", 'w'), fieldnames=kHEADER)
    output.writeheader()

    summary = {}
    for state in all_states(lines):
        margins = district_margins(all_state_rows(lines, state))

        for ii in margins:
            summary[(state, ii)] = margins[ii]

    for ii, mm in sorted(summary.items(), key=lambda x: x[1]):
        output.writerow({"STATE": ii[0], "DISTRICT": ii[1], "MARGIN": mm})
