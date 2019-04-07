from Person import Person
import Preference
import math
import random
import matplotlib.pyplot as plt
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

def bordaVote(voters, candidates, num_candidates):
    ##Poll contains the candidates' votes candidate id is the index
    poll = [0] * num_candidates
    rankings = []
    for i in range(len(voters)):
        rankings.append([])
    for vindex, v in enumerate(voters):
        min_dist = float("inf")
        min_index = -1
        ##Find the closest candidate
        ranking = []
        for cindex, c in enumerate(candidates):
            dist = distanceBetween(v, c)
            check = False
            for rindex, candidate in enumerate(ranking):
                if dist <= distanceBetween(v, candidate):
                    check = True
                    ranking.insert(rindex, c)
                    break
            if not check:
                ranking.append(c)
        rankings[vindex] = (ranking)
        assert len(ranking) == 10
    for ranking in rankings:
        for i, candidate in enumerate(ranking):
            poll[candidate.id]+=(len(ranking)-(i+1))
    return poll

def stvVote(voters, candidates, num_candidates, results):
    ##results shows who voted for which candidate
    ##Candidate id is the index
    results = [[]] * num_candidates
    ##Don't want randomness for expected results
    ##"Randomize" the Random Number Generator (RNG)
    ##random.seed(datetime.now())
    for vindex, v in enumerate(voters):
        min_dist = float("inf")
        min_index = -1
        ##Find the closest candidate
        indecisive = [] ##For ties between distances
        for cindex, c in enumerate(candidates):
            dist = distanceBetween(v, c)
            if dist <= min_dist:
                indecisive.append(cindex)
                min_index = cindex
                min_dist = dist
        ##Tie breaking if necessary
        if len(indecisive) != 1:
            min_index = random.randint(0, len(indecisive))
        results[min_index].append(vindex)
    if num_candidates == 2:
        return results
    ##Remove lowest voted candidate
    min_votes = float("inf")
    for index, votes in enumerate(results):
        if len(votes) < min_votes:
            min_votes = index
    new_candidates = list(candidates)
    for candidate in new_candidates:
        if candidate.id == min_votes:
            new_candidates.remove(candidate)
            break
    ##Next election with one less candidate
    #---NEED TO DO---#
    ##Need to archive the past results
    return stvVote(voters, new_candidates, num_candidates - 1, results)

def pluralityVote(voters, candidates, num_candidates):
    ##Polls include who voted for which candidate
    ##Candidate id is the index
    poll = []
    for i in range(num_candidates):
        poll.append([])
    ##Don't want randomness for expected results
    ##"Randomize" the Random Number Generator (RNG)
    ##random.seed(datetime.now())
    ##Starting Election
    x = 0
    for vindex, v in enumerate(voters):
        min_dist = float("inf")
        min_index = -1
        ##Find the closest candidate
        indecisive = [] ##For ties between distances
        for cindex, c in enumerate(candidates):
            dist = distanceBetween(v, c)
            # print(min_index)
            if dist <= min_dist:
                if dist == min_dist:
                    indecisive.append(cindex)
                min_index = cindex
                min_dist = dist
        ##Tie breaking if necessary
        if len(indecisive)-1 > 0:
            min_index = indecisive[random.randint(0, len(indecisive)-1)]
        # assert(min_index!=-1)
        poll[min_index].append(vindex)
    return poll

def main():
    ##print(sys.argv)
    if(len(sys.argv) != 5):
        return "Invalid Arguments\n <exe> <issues> <population> <candidates> <voting rule>\n"
    ##Command line argument 1 is the number of issues
    issues = sys.argv[1]
    issues = int(issues)
    if issues == 0:
        return "No Issues = No Election\n"
    ##Command line argument 2 is the population
    population = sys.argv[2]
    population = int(population)
    if population == 0:
        return "No Population = No Election\n"
    ##Command line argument 3 is the number of candidates
    num_candidates = sys.argv[3]
    num_candidates = int(num_candidates)
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
        candidate = Person(cpref, c, False)
        candidates.append(candidate)
    ##Generate voters and their preferences
    voters = []
    for v in range(population):
        vpref = []
        ##Generate a list of preferences over the issues
        for issue in range(issues):
            vp = random.uniform(0,1)
            vpref.append(vp)
        voter = Person(vpref, v, True)
        voters.append(voter)
    ##Identify the Voting Rule
    vote_type = sys.argv[4]
    vote_type.lower()
    v_t = vote_type[0]
    poll = None
    Plurality = False
    Borda = False
    STV = False
    results = [[]] * num_candidates
    ##Plurality
    if v_t == 'p':
        poll = pluralityVote(voters, candidates, num_candidates)
        Plurality = True
    ##Borda
    elif v_t == 'b':
        poll = bordaVote(voters, candidates, num_candidates)
        Borda = True
    ##Single Transferable Vote (STV) NOT IMPLEMENTED
    elif v_t == 's':
        poll = stvVote(voters, candidates, num_candidates, results)
        STV = True
    ##Invalid or Not Implemented
    else:
        return "Rule Type Not Implemented or Unknown\n"

    x = []
    y = []
    ticks = []
    if Plurality:
        for i in range(num_candidates):
            x.append(i)
            y.append(len(poll[i]))
            ticks.append(candidates[i].id+1)
        plt.bar(x, y, tick_label = ticks, width = .5, color = ['blue'])
        plt.xlabel('Candidate')
        plt.ylabel('Votes')
        plt.title('Plurality Election Outcome')
    elif Borda:
        for i in range(num_candidates):
            x.append(i)
            y.append(poll[i])
            ticks.append(candidates[i].id+1)
        plt.bar(x, y, tick_label = ticks, width = .5, color = ['blue'])
        plt.xlabel('Candidate')
        plt.ylabel('Score')
        plt.title('Borda Election Outcome')
    elif STV:
        for i in range(num_candidates):
            x.append(i)
            y.append(len(poll[i]))
            ticks.append(candidates[i].id+1)
        plt.bar(x, y, tick_label = ticks, width = .5, color = ['blue'])
        plt.xlabel('Candidate')
        plt.ylabel('Votes')
        plt.title('STV Election Outcome')

    winner_score = max(y)
    winner_index = y.index(winner_score)
    winner = candidates[winner_index]
    print("Winner is candidate %d!\n" %(winner.id+1))
    plt.show()

    utilities = []
    ##Utility of Population
    beta = 1
    omega = 1
    total_utility_after = 0
    for vindex, v in enumerate(voters):
        utility = beta * math.exp(-1/2*omega*math.pow(distanceBetween(v, winner), 2))
        total_utility_after += utility
        utilities[vindex] = utility
    
    ##Analysis of poll data
    ##WORK IN PROGRESS

print(main())
