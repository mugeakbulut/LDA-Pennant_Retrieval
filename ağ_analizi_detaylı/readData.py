import pandas as pd
import os
import glob
import networkx as nx
import matplotlib.pyplot as plt
import networkMeasures

path_to_csv = 'datasets/' 

csv_pattern = os.path.join(path_to_csv,'*.csv')
file_list = glob.glob(csv_pattern)
#print(file_list)


for file in file_list:
    data = pd.read_csv(file) # read data frame from json file
    networkMeasures.computecentralities(data) # append the data frame to the list
