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
    margins = {}
    districts = []
    count = 0
    for row in state_lines:
        state = row['STATE']
        #if count == 0:
            #print("IN STATE: " + state)
        if row['D']:
            if row['D'] != "H":
                if(row['GENERAL %']):
                    #print("In ditrict: " + row['D'])
                    #print("General Vote %" + row['GENERAL %'])
                    districts.append(row['D'])
        count = count + 1
    districts = list(set(districts))
    #print(districts)
    for x in districts:
        districtVotes = []
        for row in state_lines:
            if districts:
                if row['D'] == x:
                    if(row['GENERAL %']):
                        votes = row['GENERAL %'].replace(',','.')
                        votes = votes.replace('%','')
                        districtVotes.append(float(votes))
        #print(districtVotes)
        if districtVotes:
            first = max(districtVotes)
            districtVotes.remove(first)
            #print(first)
            margin = first
        if districtVotes:
            second = max(districtVotes)
            margin = first - second
            #print(second)
        if len(x) > 2: #if district is in format XX - UNEXPIRED TERM
            #print("Before cut" + x)
            x = x[0:2]
            #print("After cut" + x)
            margins[int(x)] = margin
        else:
            margins[int(x)] = margin
    #print(state)
    #print(margins)
    #print("===========================================")
    return margins
    # district_votes = []
    # districts = []
    # count = 0 
    # for row in state_lines:
    #     if row['D'] != "H":
    #         if row['D']:
    #             state = row['STATE']
    #             #print("STATE IS " + state)
    #             #print(row['D'])
    #             #print(count)
    #             count = count + 1

    #             districts.append(row['D'])
        
    # #districts.remove('H')
    # districts = filter(None, districts)
    # districts = list(districts)
    # #print(districts)
    # #print("SET OF DISTRICTS")
    # #print(set(districts))
    # secondPlace = 0
    # #print("STATE IS " + state)
    # for x in set(districts):

    #     #print("In ditrict: " + x)
    #     for row in state_lines:
    #         if row['D'] == x:
    #             if(row['GENERAL %']):
    #                 votes = row['GENERAL %'].replace(',','.')
    #                 votes = votes.replace('%','')
    #                 district_votes.append(float(votes))
    #                 #print("General Vote %" + row['GENERAL %'])
    #     #print(district_votes)
    #     firstPlace = max(district_votes)
    #     #print("Before first")
    #     #print(district_votes)
    #     district_votes.remove(firstPlace)
    #     if district_votes:
    #         secondPlace = max(district_votes)
    #     #print("After first ")
    #     #print(district_votes)
    #     #print("First is " + str(firstPlace) + " Second is " + str(secondPlace))
    #     margin = firstPlace-secondPlace
    #     if len(x) > 2: #if district is in format XX - UNEXPIRED TERM
    #         #print("Before cut" + x)
    #         x = x[0:2]
    #         #print("After cut" + x)
    #         margins[int(x)] = margin
    #     else:
    #         margins[int(x)] = margin
    # #print(margins[0])
    # # Complete this function
    # #return dict((int(x["D"]), 25.0) for x in state_lines if x["D"] and x["D"] != "H")
        
    #     #if(margins):
    #         #print("MARGINS")
    #         #print(margins)
    #return margins

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
    # for ii in lines[:10]:
    #     print(ii)
    #     print("")
        #yield ii
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