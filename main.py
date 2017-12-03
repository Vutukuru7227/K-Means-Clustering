import numpy as np
import pandas as pd
from random import uniform
import sys
import os


def find_closest_centroid():
    cluster.clear()
    cluster_id.clear()

    for j in range(0, k):
        cluster[j] =[]
        cluster_id[j] =[]

    for i in range(len(input_data)):
        b = np.array((input_data['x'][i], input_data['y'][i]))
        Id = input_data['id'][i]
        minimum = sys.float_info.max
        for j in range(0, k):
            a = np.array(centroid_list[j])
            dist = np.linalg.norm(a - b)
            if dist < minimum:
                cluster_pt = j
                minimum = dist
        cluster[cluster_pt].append((input_data['x'][i], input_data['y'][i]))
        cluster_id[cluster_pt].append(Id)


def update_centroid():

    for i in range(0, k):
        x = 0
        y = 0
        for each_point in cluster[i]:
            x += each_point[0]
            y += each_point[1]
            try:
                centroid_list[i] = ((x/len(cluster[i])), (y/len(cluster[i])))
            except Exception:
                continue


def calculate_SSE():
    SSE = 0
    for i in range(0, k):
        c = np.array(centroid_list[i])
        for pt in cluster[i]:
            p = np.array(pt)
            dist = np.linalg.norm(c - p)
            SSE = SSE + dist*dist
    return SSE


k = int(sys.argv[1])
input_file = sys.argv[2]
input_data = pd.read_csv(input_file, sep = '\t')
output_file = sys.argv[3]
centroid_list = []
for i in range(k):
    centroid_list.append((uniform(0, 1), uniform(0, 1)))
cluster = {}
cluster_id = {}

# Loop to find the best possible clusters.
for i in range(0, 25):
    flag = True
    previous_centroids = centroid_list[:]
    find_closest_centroid()
    update_centroid()

    for j in range(0,k):
        if (centroid_list[j][0] != previous_centroids[j][0]) or (centroid_list[j][1] != previous_centroids[j][1]):
            flag = False
            break
    if flag:
        break

# Calling the method to calculate the Sum of Squared Means error.
err = calculate_SSE()

for i in range(0, k):
    print('CLUSTER = ', i )
    print('\tPoints -->\t', end="")
    for Id in cluster_id[i]:
        print(Id, ',', end="")
    print()
print()

print('The final SSE is =', err)
print("-------------------------------------------")
print('Output printed to '+str(output_file)+'file')
print("-------------------------------------------")


# Printing to the output file.
file = open(output_file, 'w')
file.write("Cluster No\t List of point ids separated by commas\n")
for i in range(0, k):
    file.write(str(i) + '\t')
    for Id in cluster_id[i]:
        file.write(str(Id) + ", ")
    file.write("\n")
    file.write("\n")
file.write('The SSE is =' + str(err))