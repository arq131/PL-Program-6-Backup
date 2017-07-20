# Program 5 by Danny Nguyen (Python)
#
# Purpose:
#   This program will read in commands from an input file and store the values into
#   variables. It will also print out information when requested.

# Imports.
import re
from p6At import setVariables, setFormat, formatText, printText

# Declaring Variables
varInfo = {}
formatInfo = {'FLOW' : 'YES', 'LM' : '80', 'RM' : '80', 'JUST' : 'LEFT', 'BULLET' : 'o' }
inputLine = input()
fLine = 1
outputLine = ""
# Main while loop to read through input file until EOF and parse the data. 
while inputLine != None:
    try: # Search the input line for a certain command.
        regEx = re.compile(r'(@\.) (VAR|FORMAT|PRINT) ([A-Za-z0-9 =@".-]*)')
        match = regEx.search(inputLine)
        if (match == None): # the there is no match to the pattern, then the line is not a command. 
            formatText(inputLine, formatInfo, varInfo)
            inputLine = input()
            continue

    # Check to make sure that the line is a command line
        if match.group(1) == "@.":
            if match.group(2) == "VAR": # IF the command is "@. VAR ---"
                setVariables(match.group(3), varInfo)
            elif match.group(2) == "FORMAT": # If the command is "@. FORMAT ---"
                setFormat(match.group(3), formatInfo)
            elif match.group(2) == "PRINT": # IF the command is "@. PRINT ---"
                if match.group(3) == "VARS": # If printing out varInfo
                    print(varInfo)
                elif match.group(3) == "FORMAT": # if printing out formatInfo
                    print(formatInfo)
                else: # else error with printing.
                    print("Error: Unable to print. Found:", match.group(3))
            else: # Else the command is invalid.
                print("Error: Invalid Command. Found: " + match.group(2))
        else: # Error with command line missing @.
            print("Error: Line is not a command. Found: " + inputLine)

        inputLine = input() # go to next line
    except(EOFError): # reached end of file. break out. 
        break


