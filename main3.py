import csv
import datetime as dt
from itertools import repeat
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

        # else it already exists in loc_dict
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


for loc in loc_dict.keys():
    # sort the visiter in time order for each location
    # for each location user sorted as visitor to latest visitor
    # loc_dict = {loc_1: {user_92, user_21, ...},
    #             loc_2: {user_21, user32,...}}
    loc_dict[loc] = sorted(loc_dict[loc], key=loc_dict[loc].get)


# keep the unique location for each user
# "transpose" of loc_dict
user_dict = dict()

for loc in loc_dict:
    for user in loc_dict[loc]:
        if not (user in user_dict.keys()):
            user_dict[user] = {loc}
        else:
            user_dict[user].add(loc) 

# sorting the user_dict
# users sorted by highest unique locations to lowest
user_dict = {k: v for k, v in sorted(user_dict.items(), key=lambda x: len(x[1]), reverse=True)}


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

# book keeping for max values
stalker_score = {"friends": {"couple":None, "score":0},
                "non_friends": {"couple":None, "score":0}}

# iterate over user and its unique locations
for user, locs in user_dict.items():
    
    # initiate counter for the user
    user_stalker = {"friends":Counter(), "non_friends":Counter()}
    user_friend_stalkers = 0
    user_non_friend_stalkers = 0

    # iterate over unique locations for the user
    for loc in locs:
        # since the loc_dict[loc] is sorted list
        # user_index: number of stalker that visited before the user
        # thus, user_index is total number of stalkers for the user
        user_index = loc_dict[loc].index(user)

        # get list of stalkers
        stalkers = loc_dict[loc][:user_index]
        
        # iterate over (stalker, user)
        for couple in zip(stalkers, repeat(user)):

            if (couple in friends):
                user_stalker["friends"][couple] += 1
                
                # number of "total" friend stalker score
                user_friend_stalkers += 1
            else:
                user_stalker["non_friends"][couple] += 1

                # number of "total" non-friend stalker score
                user_non_friend_stalkers += 1
    
    # counting is the major source of computation time
    # thus, check for each user to whether it is worth to count

    if user_friend_stalkers > stalker_score["friends"]["score"]:
        # count and get the friend stalker with highest score
        friend_couple, friend_score = user_stalker["friends"].most_common(1)[0]
        # compare with global max
        if friend_score > stalker_score["friends"]["score"]:
            stalker_score["friends"]["couple"] = friend_couple
            stalker_score["friends"]["score"] = friend_score
    
    if user_non_friend_stalkers > stalker_score["non_friends"]["score"]:
        # count and get the non-friend stalker with highest score
        non_friend_couple, non_friend_score = user_stalker["non_friends"].most_common(1)[0]
        # compare with global max
        if non_friend_score > stalker_score["non_friends"]["score"]:
            stalker_score["non_friends"]["couple"] = non_friend_couple
            stalker_score["non_friends"]["score"] = non_friend_score

print(stalker_score)

# {
#   'friends': {'couple': (40090, 132961), 'score': 361},
#   'non_friends': {'couple': (1251, 106819), 'score': 376}
# }