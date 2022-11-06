import csv
import datetime as dt
from itertools import combinations
from collections import Counter


loc_dict = dict()

with open('loc-gowalla_totalCheckins.txt') as f:
    for line in f:
        line = line.strip().split('\t')

        user_id = int(line[0])
        user_dt = dt.datetime.strptime(line[1], '%Y-%m-%dT%H:%M:%SZ')
        loc_id = int(line[4])

        # if first time
        if not (loc_id in loc_dict.keys()):

            # add with the first user visited it
            loc_dict[loc_id] = {user_id: user_dt}

        # else it is already in loc_dict
        else:
            # check the user whether visited there
            # and update dt if neccesary
            if user_id in loc_dict[loc_id].keys():
                if loc_dict[loc_id][user_id] < user_dt:
                    # update the data as the earliest time
                    loc_dict[loc_id][user_id] = user_dt
            else:
                # add to dict
                loc_dict[loc_id][user_id] = user_dt

# friends set
friends = set()
with open('loc-gowalla_edges.txt' , newline='\n') as f:
    f_reader = csv.reader(f, delimiter='\t')
    for line in f_reader:
        a = int(line[0])
        b = int(line[1])
        friends.add((a,b))
        friends.add((b,a))

friends_counter = Counter()
non_friends_counter = Counter()

for loc in loc_dict.keys():
    # sort the visiter in time order
    loc_dict[loc] = sorted(loc_dict[loc], key=loc_dict[loc].get)
    
    # form pair with combination(,2)
    for couple in combinations(loc_dict[loc], 2):
        if couple in friends:
            friends_counter[couple] +=1 
        else:
            non_friends_counter[couple] +=1 

print(f"Friend pair that has the highest score {friends_counter.most_common(1)}")

print(f"Non-friend pair that has the highest score {non_friends_counter.most_common(1)}")
