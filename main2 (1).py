import csv
import datetime as dt
from itertools import combinations
from collections import Counter



# get each location with its visitor
# keep earlist visit for each visitor
loc_dict = dict()

with open('loc-gowalla_totalCheckins.txt') as f:
    for line in f:
        # parsing the string
        line = line.strip().split('\t')

        # type casting
        # string to integer for lower memory usage
        # casting to datetime for being able to compare 
        user_id = int(line[0])
        user_dt = dt.datetime.strptime(line[1], '%Y-%m-%dT%H:%M:%SZ')
        loc_id = int(line[4])

        # if first time
        if not (loc_id in loc_dict.keys()):

            # add location with the first visitor
            loc_dict[loc_id] = {user_id: user_dt}

        # else it is already exists in loc_dict
        else:
            # check the user whether visited there
            # and update dt if neccesary
            if user_id in loc_dict[loc_id].keys():
                if loc_dict[loc_id][user_id] > user_dt:
                    # update the datetime for the user as the earliest visit
                    loc_dict[loc_id][user_id] = user_dt
            
            # first time to visit loc_id for user_id
            # thus, add the user_id to loc_id
            else:
                loc_dict[loc_id][user_id] = user_dt

# friends set
# since it is given as undirected graph
# and for easy comparison
# (a,b) and (b,a) are stored with set
friends = set()
with open('loc-gowalla_edges.txt' , newline='\n') as f:
    f_reader = csv.reader(f, delimiter='\t')
    for line in f_reader:
        a = int(line[0])
        b = int(line[1])
        friends.add((a,b))
        friends.add((b,a))

# counting is done with collections.Counter()
friends_counter = Counter()
non_friends_counter = Counter()

for loc in loc_dict.keys():
    # sort the visiter in time order for each location
    loc_dict[loc] = sorted(loc_dict[loc], key=loc_dict[loc].get)
    
    # form stalker pairs with combination(,2)
    for couple in combinations(loc_dict[loc], 2):
        # check the stalker pair is in friends set
        # and count
        if couple in friends:
            friends_counter[couple] +=1 
        else:
            non_friends_counter[couple] +=1 

print(f"Friend pair that has the highest score {friends_counter.most_common(1)}")

print(f"Non-friend pair that has the highest score {non_friends_counter.most_common(1)}")

# Friend pair that has the highest score [((40090, 132961), 361)]
# Non-friend pair that has the highest score [((1251, 106819), 376)]