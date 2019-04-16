from Person import Person
import Preference
import math
import random
import matplotlib.pyplot as plt
import sys

def utilcompare(p):
    return p.utility

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

def stvVote(voters, candidates, num_candidates, results, round):
    ##results shows who voted for which candidate
    ##Candidate id is the index
    results = []
    for i in range(num_candidates):
        results.append([])
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
            # print(min_index)
            if dist <= min_dist:
                if dist == min_dist:
                    indecisive.append(cindex)
                min_index = cindex
                min_dist = dist
        ##Tie breaking if necessary
        if len(indecisive) > 0:
            min_index = indecisive[random.randint(0, len(indecisive)-1)]
        # print(min_index, len(results))
        # if len(results) <10:
        #     print(num_candidates)
        #     print(results)
        # assert(len(results) == 10)
        # assert(min_index!=-1)
        results[min_index].append(vindex)
    if num_candidates == 2:
        return results, candidates
    ##Show each round's results
    x = []
    y = []
    ticks = []
    for i in range(len(results)):
        x.append(i)
        y.append(len(results[i]))
        ticks.append(candidates[i].id+1)
    plt.bar(x, y, tick_label = ticks, width = .5, color = ['blue'])
    plt.xlabel('Candidate')
    plt.ylabel('Votes')
    plt.title("STV Election Round %i" %(round))
    plt.show()
    ##Remove lowest voted candidate
    min_votes = float("inf")
    min_index = -1
    for index, votes in enumerate(results):
        if len(votes) < min_votes:
            min_votes = len(votes)
            min_index = index
    new_candidates = candidates.copy()
    assert(min_index != -1)
    rem_candidate = new_candidates[min_index]
    new_candidates.remove(rem_candidate)
    ##Next election with one less candidate
    ##Need to archive the past results <-- Future work?
    round += 1
    return stvVote(voters, new_candidates, num_candidates - 1, results, round)

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
        if len(indecisive) > 0:
            min_index = indecisive[random.randint(0, len(indecisive)-1)]
        # assert(min_index!=-1)
        poll[min_index].append(vindex)
    return poll

def removalGraph(voters, utilities, ten_percent, total_utility_after, high, Plurality, Borda, STV, median):
    copy_voters = voters.copy()
    copy_utilities = utilities.copy()
    x = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    y = [total_utility_after]
    copy_voters.sort(reverse = high, key = utilcompare)
    while len(copy_voters) != 0:
        ## ten_percent = 2
        ## len(copy_voters) = 20
        ## 0 1 2 3 4 5 6 7 8 /9 10/ 11 12 13 14 15 16 17 18 19
        for i in range(ten_percent):
            median_start_index = int(len(copy_voters)/2 - ten_percent/2)
            if len(copy_voters) == 0:
                break
            if ten_percent>=len(copy_voters):
                copy_utilities = []
                copy_voters = []
                break;
            rem_index = i
            if median:
                # print(median_start_index)
                rem_index = median_start_index + i
                # print(i, rem_index, len(copy_voters))
            voter_to_remove = copy_voters[rem_index]
            copy_voters.remove(voter_to_remove)
            copy_utilities[voter_to_remove.id] = 0
        y.append(sum(copy_utilities))
    plt.plot(x,y,'r-')
    plt.xlabel('Percent of Voters Removed')
    plt.ylabel('Total Utility')
    if high:
        if Plurality:
            plt.title('Highest Utility Targeted Population Removal vs Total Utility (Plurality)')
        if Borda:
            plt.title('Highest Utility Targeted Population Removal vs Total Utility (Borda)')
        if STV:
            plt.title('Highest Utility Targeted Population Removal vs Total Utility (STV)')
    elif median:
        if Plurality:
            plt.title('Median Utility Targeted Population Removal vs Total Utility (Plurality)')
        if Borda:
            plt.title('Median Utility Targeted Population Removal vs Total Utility (Borda)')
        if STV:
            plt.title('Median Utility Targeted Population Removal vs Total Utility (STV)')
    else:
        if Plurality:
            plt.title('Lowest Utility Targeted Population Removal vs Total Utility (Plurality)')
        if Borda:
            plt.title('Lowest Utility Targeted Population Removal vs Total Utility (Borda)')
        if STV:
            plt.title('Lowest Utility Targeted Population Removal vs Total Utility (STV)')
    plt.show()

def main():
    ##print(sys.argv)
    if(len(sys.argv) != 5):
        return print("Invalid Arguments\npy <exe> <issues> <population> <candidates> <voting rule>\n")

    ##Command line argument 1 is the number of issues
    issues = sys.argv[1]
    issues = int(issues)
    if issues == 0:
        return print("No Issues = No Election\n")

    ##Command line argument 2 is the population
    population = sys.argv[2]
    population = int(population)
    if population == 0:
        return print("No Population = No Election\n")

    ##Command line argument 3 is the number of candidates
    num_candidates = sys.argv[3]
    num_candidates = int(num_candidates)
    if num_candidates == 0:
        return print("No Candidates = No Election\n")

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

    ## Find Utility of Population Before Election
    beta = 1.0
    omega = 1.0
    total_utilities_before = []
    for c in candidates:
        total_utility_before = 0.0
        for v in voters:
            utility = beta * math.exp(-1.0/2.0*omega*math.pow(1.0/distanceBetween(v, c), 2))
            total_utility_before += utility
        total_utilities_before.append(total_utility_before)

    optimal_utility = max(total_utilities_before)
    optimal_candidate_index = total_utilities_before.index(optimal_utility)
    optimal_candidate = candidates[optimal_candidate_index]

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
        poll, end_candidates = stvVote(voters, candidates, num_candidates, results, 1)
        STV = True
    ##Invalid or Not Implemented
    else:
        return print("Rule Type Not Implemented or Unknown\n")

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
        for i in range(len(poll)):
            x.append(i)
            y.append(len(poll[i]))
            ticks.append(end_candidates[i].id+1)
        plt.bar(x, y, tick_label = ticks, width = .5, color = ['blue'])
        plt.xlabel('Candidate')
        plt.ylabel('Votes')
        plt.title('STV Election Outcome')

    ## Find Winner
    winner_score = max(y)
    winner_index = y.index(winner_score)
    winner = candidates[winner_index]
    if STV:
         winner = end_candidates[winner_index]
    print("Winner is candidate %d!\n" %(winner.id+1))
    print("The Optimal candidate is candidate %d\n" %(optimal_candidate.id+1))
    plt.show()

    utilities = []
    ##Utility of Population After Election
    beta = 1.0
    omega = 1.0
    total_utility_after = 0.0
    for vindex, v in enumerate(voters):
        utility = beta * math.exp(-1.0/2.0*omega*math.pow(1.0/distanceBetween(v, winner), 2))
        total_utility_after += utility
        v.addUtility(utility)
        utilities.append(utility)

    ## WORK IN PROGRESS
    ## Distortion Analysis
    print("Total Utility After Election: %f" %(total_utility_after))
    print("Optimal Utility: %f" %(optimal_utility))
    # print("%s" %(utilities))

    ## Analysis of poll data
    ## Random Population Removal Model and Graph
    copy_voters = voters.copy()
    copy_utilities = utilities.copy()
    ten_percent = math.ceil(population*0.1)
    x = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    y = [total_utility_after]
    while len(copy_voters) != 0:
        for i in range(ten_percent):
            if len(copy_voters) == 0:
                break
            rem_index = random.randint(0, len(copy_voters)-1)
            voter_to_remove = copy_voters[rem_index]
            copy_voters.remove(voter_to_remove)
            copy_utilities[voter_to_remove.id] = 0
        y.append(sum(copy_utilities))
    plt.plot(x,y,'r-')
    plt.xlabel('Percent of Voters Removed')
    plt.ylabel('Total Utility')
    if Plurality:
        plt.title('Random Population Removal vs Total Utility (Plurality)')
    if Borda:
        plt.title('Random Population Removal vs Total Utility (Borda)')
    if STV:
        plt.title('Random Population Removal vs Total Utility (STV)')
    plt.show()

    ## Targeted removal (Lowest utility)
    removalGraph(voters, utilities, ten_percent, total_utility_after, False, Plurality, Borda, STV, False)
    ## Targeted removal (Highest utility)
    removalGraph(voters, utilities, ten_percent, total_utility_after, True, Plurality, Borda, STV, False)
    ## Targeted removal (Median Utility)
    removalGraph(voters, utilities, ten_percent, total_utility_after, False, Plurality, Borda, STV, True)

main()
