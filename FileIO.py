import numpy as np
import csv


#read ground-truth
def read_shots_from_csv(filename):
    data = []
    with open('groundtruths/' + filename, 'r') as f:                  #open file for reading
        reader = csv.reader(f, delimiter=';')       #create reader
        header = reader.next()
        for line in reader:
            #part1 case: with true/false for ground_truth
            if len(line) == 3:
                data.append( (int(line[0]), int(line[1]), int(line[2])) )
            #part2 case: only start and end frame for every shot
            elif len(line) == 2:
                data.append( (int(line[0]), int(line[1])) )
    return data


#write histogram csvs with numpy
def save_histograms_to_file(filename, mdh_all):
    np.savetxt('motionDirectionHistograms/' + filename, mdh_all, delimiter=',', fmt='%4.4f')


#read histogram csvs with numpy
def read_histograms_from_file(filename):
    mdh_all = np.genfromtxt('motionDirectionHistograms/' + filename, dtype=float, delimiter=',')
    return mdh_all


#get first and last frame of every shot
def read_shot_boundaries(filename):
    ground_truth_data = read_shots_from_csv(filename)
    ground_truth_start = {}
    ground_truth_end = {}
    for data in ground_truth_data:
        #part1 case: with true/false for ground_truth
        if len(data) == 3:
            a,b,c = data
        #part2 case: only start and end frame for every shot
        elif len(data) == 2:
            a,b = data
        ground_truth_start[a] = data
        ground_truth_end[b] = data

    return ground_truth_start, ground_truth_end
