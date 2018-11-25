# This module computes the following six statistics , from the cleaned files written in the
# previous module.
# Length of the transcript — indicated by the number of statements
# Size of the vocabulary — indicated by the number of unique words
# Number of repetition for certain words or phrases — indicated by the CHAT symbol [/]
# Number of retracing for certain words or phrases — indicated by the CHAT symbol [//]
# Number of grammatical errors detected — indicated by the CHAT symbol [*]
# Number of pauses made — indicated by the CHAT symbol (.)
# This uses the OS module to extract the absolute path of the current file, and reads the cleaned files relative to this
# path one after the other. The data_analysis class contains modules that each compute one of the statistics, taking the
# file contents as input and returns the count as output. Each of these functions is called by analyse_script function.
# the list_of_words() function converts the list of lines into a list of words by replacing '\n' character with space
# character and joining it based on no spaces, and later splitting it based on space character. This function is called
# by the functions computing the statistics. The __str__ functions returns the feature list contents in a well formatted
# manner.

# os module is used to extract the absolute path of the current python file.
import os

# Stores the absolute path of the current python file
dirname = os.path.dirname(__file__)

# This class performs all statistics calculation for a given child group, one child after another in the group.
class data_analysis:
    def __init__(self, name):
        # feature_list : A dictionary having keys holding a list of each of the 6 statistics, each list will contain 10
        # entries for each of the 10 files in SLI and TD for the 10 children
        # Child Index - holds the child number
        # LOT - Length of the transcript
        # SOV - Size of the vocabulary
        # REP - Number of repetition for certain words or phrases
        # RET - Number of retracing for certain words or phrases
        # GE - Number of grammatical errors detected
        # PAUSE - Number of pauses made
        # name - will hold the name of the child group (SLI, TD)
        # instance - will hold the number of the transcript being read in the child group, initially set to 0.
        self.size_of_file = 10
        self.feature_list = {'Child_Index': [], 'lot': [], 'sov': [], 'rep': [], 'ret': [], 'ger': [], 'pause': []}
        self.name = name
        self.instance = 0

    # This function returns the feature_list for task3
    def get_feature_list(self):
        return self.feature_list

    # This function returns a formatted string containing the 6 statistics for the given child group
    def __str__(self):
        str1 = self.name+"\n"
        # key_list is used to sort the keys of the list, for better presentation and to avoid randomness while printing
        key_list = list(self.feature_list.keys())
        key_list.sort()
        # Append each of the keys in the statistics to the string
        for each in key_list:
            str1 += str(each)+" \t"
        # i goes from 0 to 9 (size_of_file = 10), iterating for one file after the other
        for i in range(self.size_of_file):
            str1 += "\n"
            # iterating through each of the statistics
            for each in key_list:
                str1 += str(self.feature_list[each][i])+"\t\t"
                # Extra tab space for Child_Index, for better presentation
                if each == 'Child_Index':
                    str1+=" \t\t"
        # returns the formatted string
        return str1

    # Task2a
    # Calculates the length of transcript by iterating through each of the line in the file stored in file_contents list
    #  passed as an argument to the function, to check if it contains ',', '.', '!' and if it exists in the line, it
    # increments the counter by 1. The counter is returned.
    def lot(self, file_contents):
        # List of characters to search of, the ' \n ' character ensures the punctuation mark is at the end of the line,
        # and does not calculate the punctuations in the middle of statements. Counter is set to 0 at first.
        punctuations = [' .\n', ' ?\n', ' !\n']
        counter = 0
        # iterates through the lines in file_contents
        for each in file_contents:
            for x in punctuations:
                if x in each:
                    counter += 1
                    break

        return counter


    # Function to convert a list of individual characters into a list of words
    def list_of_words(self, file_contents):
        index = 0
        words = []
        # for each of the characters in the file_contents list
        for each in file_contents:
            # Replace the '\n' character with space character
            if '\n' in each:
                file_contents[index] = each.replace('\n', ' ')
            # join the list into a string on basis of adjacent character to later split on basis of space
            str_joined = ''.join(each)
            # This is to group the sentences into a list of words, marked by the space character
            words.append(str_joined.split(' '))
            # holds the current index of the character being iterated through file_contents in the loop incremented here
            #  for the next cycle
            index += 1
        return words

    # Tak2b
    # Function to return the number of unique words
    def sov(self, file_contents):
        set_of_words = set()
        # A list containing the characters that must not be added into the set. Contains the parameters used for
        # measuring statistics, the *CHI indicating child transcript line and punctuation marks.
        skip_chars = ['[/]', '[//]', '[*]', '(.)', '*CHI:', '.', '!', '?']
        # Convert the file contents into a list of words using the above defined function
        words = self.list_of_words(file_contents)
        # For each word in the newly created list, add it to a set, excluding the contents in skip_chars . Set maintains
        # only unique words and ignores the add operation if the word already exists.
        for each in words:
            for each1 in each:
                if each1 not in skip_chars:
                    set_of_words.add(each1)
        # Removes the empty character that gets added unnecessarily.
        set_of_words.remove('')
        # length of the set determins the number of unique words.
        return len(set_of_words)

    # Task 2c
    # Function to calculate the number of repetitons in the file identified by the number of occurrences of [/].
    def rep(self, file_contents):
        # Counter is set to 0 in the beginning
        counter = 0
        # Convert the file_contents into a list of words using the above defined function.
        words = self.list_of_words(file_contents)
        # iterate through each line in the file and each word in each line, and increment the counter if '[/]' is
        # encountered.
        for each_line in words:
            for each_word in each_line:
                if each_word == '[/]':
                    counter += 1
        # Returns the counter holding number of repetitions
        return counter

    # Task 2d
    # Function to calculate the number of retraces in the file identified by the number of occurrences of [//].
    def ret(self, file_contents):
        # Convert the file_contents into a list of words using the above defined function.
        words = self.list_of_words(file_contents)
        # Counter is set to 0 in the beginning
        counter = 0
        # iterate through each line in the file and each word in each line, and increment the counter if '[//]' is
        # encountered.
        for each_line in words:
            for each_word in each_line:
                if each_word == '[//]':
                    counter += 1
        # Returns the counter holding number of retraces
        return counter

    # Task 2e
    # Function to calculate the number of grammatical errors in the file identified by the number of occurrences of [*].
    def ger(self, file_contents):
        # Convert the file_contents into a list of words using the above defined function.
        words = self.list_of_words(file_contents)
        # Counter is set to 0 in the beginning
        counter = 0
        # iterate through each line in the file and each word in each line, and increment the counter if '[*]' is
        # encountered.
        for each_line in words:
            for each_word in each_line:
                if each_word == '[*]':
                    counter += 1
        # Returns the counter holding number of grammatical errors
        return counter

    # Task 2e
    # Function to calculate the number of pauses in the file identified by the number of occurrences of (.).
    def pause(self, file_contents):
        # Counter is set to 0 in the beginning
        counter = 0
        # Convert the file_contents into a list of words using the above defined function.
        words = self.list_of_words(file_contents)
        # iterate through each line in the file and each word in each line, and increment the counter if '(.)' is
        # encountered.
        for each_line in words:
            for each_word in each_line:
                if each_word == '(.)':
                    counter += 1
        # Returns the counter holding number of pauses
        return counter

    # This function recieves the file path for the cleaned transcript, reads the contents and calls the 6 statistics
    # functions one by one. the value returned to it is appended to the list associated with the dictionary key in
    # feature_list
    def analyse_script(self, file):
        # Open the file using the path provided by file variable in the argument, in read mode.
        f = open(file, 'r')
        # Read its contents into a list using the readlines() method
        lines_in_file = f.readlines()
        # Increment the instance counter each time the file is read
        self.instance += 1
        # Append the instance number into the child_index key associated list
        self.feature_list['Child_Index'].append(self.instance)
        # Call the lot function and append its value into the list associated with lot key
        self.feature_list['lot'].append(self.lot(lines_in_file))
        # Call the sov function and append its value into the list associated with sov key
        self.feature_list['sov'].append(self.sov(lines_in_file))
        # Call the rep function and append its value into the list associated with rep key
        self.feature_list['rep'].append(self.rep(lines_in_file))
        # Call the ret function and append its value into the list associated with ret key
        self.feature_list['ret'].append(self.ret(lines_in_file))
        # Call the ger function and append its value into the list associated with ger key
        self.feature_list['ger'].append(self.ger(lines_in_file))
        # Call the pause function and append its value into the list associated with pause key
        self.feature_list['pause'].append(self.pause(lines_in_file))
        # Close the file that was opened
        f.close()

# objects for data_analysis class is created for SLI and TD, the file path of cleaned files is passed to analyse script
# method. Flag indicates which module calls it, if 1, it is called from task2, if 0 it is called from task3
def main(flag):
    # Create 2 objects for the class data_analysis, one for SLI and one for TD
    SLI_DA = data_analysis("SLI")
    TD_DA = data_analysis("TD")

    # Iterate through the 10 files int SLI_cleaned folder and pass the path to the analyse_script method od the SLI_DA
    # object to calculate the statstics for the group.
    for p in range(1, 11):
        file_path_SLI = dirname + '/ENNI Dataset/SLI_cleaned/SLI-' + str(p) + '.txt'
        SLI_DA.analyse_script(file_path_SLI)

    # Iterate through the 10 files int STD_cleaned folder and pass the path to the analyse_script method od the TD_DA
    # object to calculate the statstics for the group.
    for p in range(1, 11):
        file_path_TD = dirname + '/ENNI Dataset/TD_cleaned/TD-' + str(p) + '.txt'
        TD_DA.analyse_script(file_path_TD)
    # if flag is 1, print the objects
    if flag:
        print(SLI_DA)
        print(TD_DA)
    # if flag is 0 return the values to the calling module, i.e module 3
    else:
        return SLI_DA.get_feature_list(), TD_DA.get_feature_list()
# If this is the main script, it calls main with argument to indicat task2 is calling the function
if __name__ == "__main__":
    main(1)