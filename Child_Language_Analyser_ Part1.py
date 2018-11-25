
# The following module reads in the SLI and TD files from the ENNI DATASET folder, one by one as a list of strings.
# It then identifies the string containing '*CHI:' and extracts and appends them into a list until it encounters any
# other symbols like %mor, %gra, @ID: etc. Once the the *CHI statements have been extracted, the list is cleaned of any
# unnecessary symbols like anything enclosed in '[]' except [/],[//],[*m:+ed], anything between '()' is retained and '(',')'
# is removed, except '(.)', '<','>' is removed, words starting with '&' and  '+' is removed.
# Finally the cleaned out script is written to seperate text files in append mode, one line after the other in SLI-Cleaned
# and TD-Cleaned folders inside ENNI Dataset. To read and write files, which are stored relative to this module, the OS
# module has been used, and os.path.dirname is used to extract the directory name of the current python file, the rest of
# the path is concatenated in the respective read and write commands.


# Modules for pattern matching (re) and file read write(os)
import re
import os

#Stores the absolute path of the current python file
dirname = os.path.dirname(__file__)

# Following loop runs 20 times, 10 times for 10 text files in both SLI and TD folders
for x in ['SLI', 'TD']:
    # Text files are named SLI-1 to SLI-10 and TD-1 to TD-10
    for f in range(1, 11):
        # The absolute path of the python file extracted above is appended  with the relative path of the text files stored
        # as a folder in the same location of this python file. Variable 'x' will hold either 'SLI' or 'TD' at any given time
        # and 'f' will hold a value between 1 and 10 at any given time. For ex: for SLI-1.txt, the path below would convert
        # to "C:/Users/USER1/Desktop/Python/ENNI Dataset/SLI/SLI-1.txt"

        filename = dirname+'/ENNI Dataset/'+str(x)+'/'+str(x)+"-" + str(f) + '.txt'
        print(f, filename)

        # Open the file in read mode
        f1 = open(filename, 'r')
        # Read the file contents into a list of strings, split based on "\n"
        f_str = f1.readlines()

        # Two empty lists, one to hold the indices where  '*CHI:' is present and another to hold the filtered out strings.
        chi_index = []
        filtered_list = []

        # task1a
        # Iterate through each string in the list to find the occurrence of '*CHI:' at the start of the string, if
        # present, append that index to chi_index list.
        for i in range(len(f_str)):
            if f_str[i].find("*CHI") == 0:
                chi_index.append(i)

        i = -1
        # Iterate through chi_index, to obtain the index where *CHI is present and append those lines to the
        # filtered_list. Check if the next line starts with any other symbols like %gra, @ID, etc. if so go to the next
        # index in chi_index, else append the next line to the filtered_list. This ensures that if the *CHI statement
        # extends to multiple lines, those are correctly captured into the filtered list
        for each in chi_index:

            filtered_list.append(f_str[each])  # chi_index[i]=each
            i += 1 # counter for filtered_list
            j = each + 1 # holds one more than the current index provided by chi_index

            # to check if 2 consecutive *CHI: appear, if so skip processing the remaining loop. Checks if j value is the
            # same as the next index held in chi_index, as long as i is not the last index.
            if i != len(chi_index) - 1 and chi_index[i + 1] == j:
                continue
            # re. match checks for anything in between '@'and':' and '%' and ':' and '*EXA:' , if it returns some value,
            # it breaks out of the loop else it will append the line to filtered_list, j is incremented at the end of
            # each loop.
            while True:
                if (re.match('@.*:', f_str[j]) is not None) or (re.match('%.*:', f_str[j])) is not None or (
                        re.match('\*EXA:', f_str[j]) is not None):
                    break
                else:
                    filtered_list[i] += f_str[j]
                j += 1


        # task1b
        # All '\t' characters are expanded into whitespaces to avoid confusion
        for j in range(len(filtered_list)):
            filtered_list[j] = filtered_list[j].expandtabs()

        # '[* m:+ed]' and [* m] is replaced with '[*]' to make the proceesing more easier, this '[*]' will be counted in the next task.
        for j in range(len(filtered_list)):
            if '[* m:+ed]' in filtered_list[j]:
                filtered_list[j] = filtered_list[j].replace('[* m:+ed]', '[*]')
            if '[* m]' in filtered_list[j]:
                filtered_list[j] = filtered_list[j].replace('[* m]', '[*]')

            # If'[' is encountered, it checks for '[/], '[//]', '[*] symbols, if it is encountered, it skips the remaining
            # loop and proceed with the next i value, if it is not encountered, re.match is used to find the index of '['
            # and ']' and the string is replaced with the concatenation of substring without it.
            # 'j' represents the index of each string in filtered_list and 'i' represents index of each character in the string
            if '[' in filtered_list[j]:
                for i in range(len(filtered_list[j])):

                    if filtered_list[j][i] == '[':
                        if filtered_list[j][i:i + 4] == '[//]' or filtered_list[j][i:i + 3] == '[/]' or filtered_list[j][i:i + 3] == '[*]':
                            continue
                        else:
                            m, n = re.match('\[.*\]', filtered_list[j][i:]).span()
                            # Incase 2 consecutive pairs of square brackets have been taken into consideration the
                            # following code will reassign it to the right value
                            n = filtered_list[j][i + m:].find(']')
                            filtered_list[j] = filtered_list[j][0:i + m] + filtered_list[j][i + n + 1:]
                    if i == len(filtered_list[j]) - 1 or i == len(filtered_list[j]):
                        break

            # if '<' or '>' symbol is encountered, the string is reassigned to the concatenation of substring without it.
            if '<' in filtered_list[j] or '>' in filtered_list[j]:
                for i in range(len(filtered_list[j])):
                    if filtered_list[j][i] == '<' or filtered_list[j][i] == '>':
                        filtered_list[j] = filtered_list[j][0:i] + filtered_list[j][i + 1:]
                    if i == len(filtered_list[j]) - 1 or i == len(filtered_list[j]):
                        break

            # if '(' or ')' is encountered, '(.)' is checked for, if present, the remaining loop is skipped and i is
            # incremented to the next value, else '(' and ')' symbols are excluded and the substrings are concatenated
            # and stored as the new string. the flag ensures that ')' symbol is not removed if it is a part of '(.)'.
            if '(' in filtered_list[j]:
                flag = 0  # to ensure not to delete ')' of '(.)'
                for i in range(len(filtered_list[j])):
                    if filtered_list[j][i] == '(':
                        if filtered_list[j][i:i + 3] == '(.)':
                            flag = 1
                            continue
                        else:
                            filtered_list[j] = filtered_list[j][0:i] + filtered_list[j][i + 1:]
                            flag = 0
                    if filtered_list[j][i] == ')' and not flag:
                        filtered_list[j] = filtered_list[j][0:i] + filtered_list[j][i + 1:]
                    if i == len(filtered_list[j]) - 1 or i == len(filtered_list[j]):
                        break

            # if '&' or '+' symbol is encountered, the string is reassigned to the concatenation of substring without
            # the symbol and the word following it. \S represent non-whitespace character and \s represents whitespace

            # if i is equal to or one ess than the length of string, due to removal of symbols, quit the loop to prevent
            # list index out of range error
            if '&' in filtered_list[j] or '+' in filtered_list[j]:
                for i in range(len(filtered_list[j])):
                    if filtered_list[j][i] == '&' and filtered_list[j][i - 1] == ' ':
                        m, n = re.match('\&\S*\s', filtered_list[j][i:]).span()
                        filtered_list[j] = filtered_list[j][0:i + m] + filtered_list[j][i + n-1:]
                    if filtered_list[j][i] == '+' and filtered_list[j][i - 1] == ' ':
                        m, n = re.match('\+\S*\s', filtered_list[j][i:]).span()
                        filtered_list[j] = filtered_list[j][0:i + m] + filtered_list[j][i + n-1:]
                    if i == len(filtered_list[j]) - 1 or i == len(filtered_list[j]):
                        break

        # Replace '\n' with spa ce to avoid any confusion when reading the cleaned files
        for index in range(len(filtered_list)):
            if "\n" in filtered_list[index]:
                filtered_list[index] = filtered_list[index].replace("\n"," ")

        # Remove the trailing white spaces and append a '\n' at the end of each string in the filtered_list to use the
        # readlines() function in the next task to easily retrieve the contents.
        for i in range(len(filtered_list)):
            filtered_list[i] = filtered_list[i].rstrip()
            filtered_list[i] += "\n"

        # print(filtered_list)

        # Open new text file in the SLI_cleaned / TD_cleaned folder respectively in append mode and write each string
        # to the file one by one. Close all files opened.
        filename1 = dirname+'/ENNI Dataset/'+ str(x)+'_cleaned/' + str(x)+"-" + str(f) + '.txt'
        f2 = open(filename1, 'a')
        for each in filtered_list:
            f2.write(each)
        f1.close()
        f2.close()

