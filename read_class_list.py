import pickle


master_list = {}

''' Input File formatted as user,section '''
classList = open('class_list.txt', 'r')
for line in classList.readlines():
    line = line.strip().split(',')
    master_list[line[0]] = line[1]

with open('class_list.pickle', 'wb') as output:
    pickle.dump(master_list, output, protocol=pickle.HIGHEST_PROTOCOL)
