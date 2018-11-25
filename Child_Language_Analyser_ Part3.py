
# This module utilises the statistics computed in module2 to calculate the mean for each statistic in a child group
# across the 10 children's transcripts, and displays the result in the form of a bar graph. It utilizes numpy to compute
# the mean of the statistics, stored in lists corresponding to dictionary keys, pandas to convert the statistics of the
# 2 groups to dataframe and matplotlib.pyplot to plot the statistics into a graph.
# The data_analysis class from the task2 module is imported for obtaining the statistics. The compute_averages method of
# visualiser class computes the average of the 10 values for each statistics. The get_avg_stats,
# get_name function are used by the SLI object to get the contents of TD for printing and graph creation in
# visualise_statistics method.

# os module is used to extract the absolute path of the current python file.
import os
# pandas module is used for presentation and graph plotting
import pandas as pd
# numpy module is used for calculating the average of 10 values for each statistics
import numpy as np
# matplotlib.pyplot module is used for plotting the graph comparing the 2 child groups
import matplotlib.pyplot as plt
from Child_Language_Analyser_Part2 import data_analysis, main

# This class calculates the average and displays the graph comparing the 2 child groups
class visualiser:
    def __init__(self, data, name):
        # name holds the name of the child group
        # dataFrame holds the pandas dataframe of the statistics dictionary for the child group setting the child index
        # as the index for the data frame
        # statistics_avg is a dictionary with its keys as the statistics and the corresponding average value is computed
        # and assigned by the compute_averages method
        # graph_DF is an empty dictionary which will be used by the visualise_statistics method to create a pandas
        # dataframe of the 2 childgroups mean statistics for plotting.
        self.name = name
        self.dataFrame = pd.DataFrame(data)
        self.dataFrame.set_index('Child_Index', inplace=True)
        self.statistics_avg = {'lot': 0, 'sov': 0, 'rep': 0, 'ret': 0, 'ger': 0, 'pause': 0}
        self.graph_DF ={}

    # Function to compute the average of each statistic for the 10 children in each group
    def compute_averages(self):
        # for each statistics the average is computed and stored in statistics_avg dictionary
        for each in self.dataFrame.keys():
            self.statistics_avg[each] = np.average(self.dataFrame[each])
        
    # Function to return the DataFrame corresponding to the 6 statistics for this child group
    def get_dataframe(self):
        return self.dataFrame
    
    # Function to return the average of each statistic for the 10children in each group
    def get_avg_stats(self):
        return self.statistics_avg
    
    # Function to return the name of the object - SLI or TD
    def get_name(self):
        return self.name

    # Function to print out the dataframes, mean values and display the graphical representation of the 2 groups, it
    # takes the other object of same class to compare and plot the graph, by calling, its functions to retrieve data.
    def visualise_statistics(self, compare_object):
        # Printing the  mean values of SLI and TD
        print(self.name,": \n",self.dataFrame,"\nMean Values:\n")
        for key,value in self.statistics_avg.items():
            print(key,":",value,"\n")
        other_dataFrame = compare_object.get_avg_stats()
        print(compare_object.get_name(),": \n",compare_object.get_dataframe(),"\nMean Values:\n")
        for key,value in other_dataFrame.items():
            print(key,":",value,"\n")

        # GER value is too small to be represented on the same graph, hence it is scaled by a factor of 100 to make it visible
        self.statistics_avg['ger'] *= 100
        other_dataFrame['ger'] *= 100
                
        # Create a dictionary of statistics list, and corresponding values for each group, make a dataframe out of it for plotting
        values = {'Statistics':['Length of Transcript','Size of Vocabulary','Number of repetitions','Number of retracing'
                                ,'Number of grammatical errors*100','Number of pauses made'],
                'SLI':list(self.statistics_avg.values()),
                'TD':list(other_dataFrame.values())}
        self.graph_DF = pd.DataFrame(values)
        self.graph_DF.set_index('Statistics', inplace =True)
        # Plotting a bar graph of size 10x7 of the mean values of the 2 groups stored in graph_DF dataframe
        self.graph_DF.plot(kind = 'bar', figsize = (10,7) )
        # Creates a layout with padding 2 pts showing all contents on all 4 sides
        plt.tight_layout(pad = 2.0)
        # incorporates a legend in the plot
        plt.legend()
        # sets the title as SLI vs TD
        plt.title('SLI VS TD')
        # sets the x axis label as Statistics, indicating it represents the 6 statistics
        plt.xlabel('Statistics')
        # sets the y axis label as Values, indicating it represent the values for the statistics
        plt.ylabel('Values')
        # Displays the plot
        plt.show()

# Call the main function of task 2 with argument as 1 to indicate the function is called from task 3, since multiple
# values are returned, the output returned is in the form of a tuple and it is accessed by indexing.
dataFrames_returned = main(0)
# Get the dataframe and make an object of visualiser class using it.
data_SLI = dataFrames_returned[0]
data_TD = dataFrames_returned[1]

# Create objects of visualiser class for SLI and TD groups and call their compute_averages function to compute their
# averages
SLI_Visualise = visualiser(data_SLI,"SLI")
SLI_Visualise.compute_averages()

TD_Visualise = visualiser(data_TD,"TD")
TD_Visualise.compute_averages()
# Pass the TD object to the visualise_statistics method of SLI object to print the mean values and plot the graph
# comparing the 2 groups
SLI_Visualise.visualise_statistics(TD_Visualise)
