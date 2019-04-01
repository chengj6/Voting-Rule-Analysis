import Person.py
import Preference.py
import math
import random
import sys

##Euclidian distance between two issue-dimensional points
def distanceBetween(v1, v2):
    p1 = v1.pref
    p2 = v2.pref
    result = 0.0
    assert(len(p1) == len(p2))
    for issue in range(len(p1)):
        dif = p2[issue] - p1[issue]
        result += math.pow(dif, 2)
    return math.sqrt(result)

def bordaVote(voters, candidates):
    poll = [[]] * candidates
    return poll

def stvVote(voters, candidates):
    poll = [[]] * candidates
    return poll

def pluralityVote(voters, candidates):
    ##Poll Results
    poll = [[]] * candidates
    ##"Randomize" the Random Number Generator (RNG)
    random.seed(datetime.now())
    ##Starting Election
    for vindex, v in enumerate(voters):
        min_dist = float("inf")
        min_index = -1
        ##Find the closest candidate
        indecisive = [] ##For ties between distances
        for cindex, c in enumerate(candidates):
            dist = distanceBetween(v, c, issues)
            if dist <= min_dist:
                indecisive.append(cindex)
                min_index = cindex
                min_dist = dist
        ##Tie breaking if necessary
        if len(indecisive) != 1:
            min_index = random.randint(0, len(indecisive))
        poll[min_index] = vindex
    return poll

def main(argv, len(argv)):
    if(len(argv) != 5):
        return "Invalid Arguments\n <exe> <issues> <population> <candidates> <voting rule>\n"
    ##Command line argument 1 is the number of issues
    issues = argv[1]
    if issues == 0:
        return "No Issues = No Election\n"
    ##Command line argument 2 is the population
    population = argv[2]
    if population == 0:
        return "No Population = No Election\n"
    ##Command line argument 3 is the number of candidates
    num_candidates = argv[3]
    if num_candidates == 0:
        return "No Candidates = No Election\n"
    ##Seed Random Number Generator for reusability of results
    random.seed(9001)
    ##Generate Candidates and their preferences
    candidates = []
    for c in range(num_candidates):
        cpref = []
        ##Generate a list of preferences over the issues
        for issue in range(issues):
            cp = random.uniform(0,1)
            cpref.append(cp)
        v = Person(cpref, c, False)
    ##Generate voters and their preferences
    voters = []
    for v in range(population):
        vpref = []
        ##Generate a list of preferences over the issues
        for issue in range(issues):
            vp = random.uniform(0,1)
            vpref.append(vp)
        v = Person(vpref, v, True)

    ##Identify the Voting Rule
    vote_type = argv[4]
    vote_type.lower()
    v_t = vote_type[0]
    poll = None
    ##Plurality
    if v_t == 'p':
        poll = pluralityVote(voters, candidates)
    ##Borda
    elif v_t == 'b':
        poll = bordaVote(voters, candidates)
    ##Single Transferable Vote (STV)
    elif v_t == 's':
        poll = stvVote(voters, candidates)
    ##Invalid or Not Implemented
    else:
        return "Rule Type Not Implemented or Unknown\n"

    ##Analysis of poll data
    ##WORK IN PROGRESS
