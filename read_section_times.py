import pickle

master_times = {}

section_times = open('section_times.txt', 'r')
for line in section_times.readlines():
    line = line.strip().split(',')
    master_times[line[0]] = {'day' : line[1],
                             'start' : line[2],
                             'end' : line[3],
                             'pm' : True if line[4] == 'P' else False}

with open('section_times.pickle', 'wb') as output:
    pickle.dump(master_times, output, protocol=pickle.HIGHEST_PROTOCOL)
