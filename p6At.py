# p6At Created by Danny Nguyen

import re
import math
# Global Variables
firstLine = 0
outputLine = ""

##### setVariables #####
# Purpose: 
# 		setVariables will search the (atString) and add the variables into
# 		varInfo.
# Parameters:
# 		atString : String to search.
# 		varInfo : Dictionary to store the information parsed.
# Example Usage:
# 		atString : "@first=name" ... "@last=name" ... "@street="123 san antonio""
def setVariables(atString, varInfo):
    varRegEx = re.compile(r'@(.*?)="?([^"]*\.?)"?')
    searchVar = varRegEx.search(atString)
    if searchVar == None:
        print("Error: Unable to match string. Found: " + atString)
    varInfo[searchVar.group(1)] = searchVar.group(2)

##### setFormat #####
# Purpose:
#		setFormat will search he (atString) and add the variables into
# 		formatInfo.
# Parameters:
# 		atString : String to search
# 		formatInfo : Dictionary to store the information parsed.
# Notes:
#       We are assuming values for RM/LM, and FLOW are correct input. 
# Example Usage:
# 		atString : " JUST=BULLET BULLET=o RM=70 FLOW=YES"
# # # # # # # # # # # #
def setFormat(atString, formatInfo):
    formatRegEx = re.compile(r'(.*?)=(.*)')
    varChange = atString.split();
    justCheck = {"LEFT", "RIGHT", "BULLET", "CENTER"}
    for var in varChange:
        tokens = formatRegEx.search(var)
        key = tokens.group(1)
        value = tokens.group(2)
        if key in formatInfo:
            if key == "JUST": # make sure the values of JUST are correct.
                if value not in justCheck: # if the values being assign to JUST is invalid, continue
                    print("Error: Assign wrong value into JUST. Found: " + var)
                    continue
            formatInfo[key] = value
        else:
            print("Error: Key value is bad. Found: " + var)

##### reset #####
# Purpose:
#   Initializes the current working formatted output line to an empty string
# Parameters:
#   N/A
# Notes/Examples:
#   Not sure if this is really too helpful, but i'll just roll with it. 
# # # # # # # # # # # #
def reset():
    global outputLine
    outputLine = ""     # Resets output line to empty

##### formatText #####
# Purpose:
#   Format the text that is being passed in.
# Parameters:
#   inputLine - The line of text that needs to be formatted.
#   formatInfo - info for formatting
#   varInfo - info for variables
# Notes:
#    * Determine the formatted text width (different from bullets)
#       o formatWidth = int(formatInfo["RM"]) - int(formatInfo["LM"]) + 1
#    * If the line is empty/blank:
#       o If flow is yes: [Print current working formatted line]
#       o Initialize for new paragraph (i.e. recognize that you are on the first line of a paragraph)
#       o print a blank line.
#    * Else it is a line that needs to be formatted.
#       o Expand the input line by substituting variables.
#           - For each word in the expanded line:
#               // See if it can be added to the current working formatted output line.
#               // If so, add it. 
#               // Else, Invoke a function to print the text.
#       o Otherwise, FLOW == "NO"
#           - Truncate the expanded input line of necessary.
#           - Invoke a function to print the text.
# # # # # # # # # # # #
def formatText(inputText, formatInfo, varInfo):
    # Substition for @values
    global firstLine
    global outputLine
    subRegEx = re.compile(r'@([A-Za-z]*)([\.,\?]?[ ]?)')    # regex for reading variables.
    inputText = inputText.strip()
    strings = inputText.split(" ")                         # variable containing all words in a sentence.

    # Check if the line is a blank/empty line.
    if inputText.strip() in ['', '\n', '\r\n']:
        outputLine = outputLine.strip()
        if formatInfo["FLOW"] == "YES":         # check to see if there is flow.
            printText(formatInfo)               # print remaining info.
        firstLine = 0                           # reset to beginning of paragraph.
        reset()                                 # reset text line.
        print(' ')                                 # print blank line
        return                                  # don't need to go further.

    # if flow is turned of and output line is not empty, print out current message before reading.    
    if (formatInfo["FLOW"] == "NO") and (outputLine != ""):
        printText(formatInfo)

    # Go through a line of text, word by word. 
    for text in strings:
       
        # Search the word to see if it needs to be replaced. If so, add the text using info in varInfo.
        subMatch = subRegEx.search(text)
        if subMatch != None: # if it matched
            key = subMatch.group(1)
            if key in varInfo: # check if the key is in varInfo
                if subMatch.group(2) != None: # if there is puncuation after the variable
                    text = varInfo[key] + subMatch.group(2)
                else: # otherwise replace text with value
                    text = varInfo[key] 
        text = text.strip()

        # Determine length of output+text+indention.    
        if formatInfo["JUST"] == "BULLET": 
            totalLen = len(outputLine) + len(text) + int(formatInfo["LM"]) + 1
        else:
            totalLen = len(outputLine) + len(text) + int(formatInfo["LM"]) - 1

        # Check if flow is turn on. Do something special if it is.
        if formatInfo["FLOW"] == "YES":
            if (totalLen > int(formatInfo["RM"])): # If the length of the sentence is greater than RM
                outputLine = outputLine.strip()
                printText(formatInfo)              # Print out current line.
                reset()                            # Reset text.
                outputLine += text + " "           # Add current word to next line.
            else: # otherwise just add word onto line.
                outputLine += text + " "
        elif formatInfo["FLOW"] == "NO": # else if flow is turned off
            if totalLen > int(formatInfo["RM"]):   # If the length exceeds RM
                printText(formatInfo)              # Print out current line
                reset()                            # Reset text
                return                             # Finish reading sentence (truncate)
            else: # Otherwise just keep reading.
                outputLine += text + " "

    
    # If there is text that hasn't been printed with flow on, leave output line alone and don't print anything.
    if (formatInfo["FLOW"] == "YES") and (outputLine != ""):
        return

    outputLine = outputLine.strip()
    
    # Print out the output line after all the text on the line has been read. 
    printText(formatInfo)

##### addSpaces #####
# addSpaces(formatInfo, ifBullet)
# Purpose: 
#   Adds the required amount of spaces before each sentence. (Length depends on LM value)
# Parameter:
#   formatInfo - dictionary contains formatting info.
# # # # # # # # # # #
def addSpaces(formatInfo):
    global outputLine
    global firstLine
    RM = int(formatInfo["RM"])
    LM = int(formatInfo["LM"])
    outputLine = outputLine.strip()

    # Handle right justification.
    if formatInfo["JUST"] == "RIGHT":
        while len(outputLine) <= (RM-1): # while the line is not at RM
            outputLine = " " + outputLine               # add spaces until it reaches RM.
        return 

    # Handle center justification.
    if formatInfo["JUST"] == "CENTER":       
        Rcenter = RM - len(outputLine)
        Lcenter = LM + len(outputLine)
        avgCenter = math.floor((RM + LM)/2)
        spaceNeeded = (avgCenter - math.floor(len(outputLine)/2))
        print(spaceNeeded)
        for i in range(1, spaceNeeded): # 
            outputLine = " " + outputLine
        return

    # check if its the first line in a paragraph and if it requires a bullet.
    if (firstLine == 0) and (formatInfo["JUST"] == "BULLET"):
        outputLine = formatInfo["BULLET"] + " " + outputLine    # insert bullet
        for i in range(1, LM):               # insert require spaces
            outputLine = " " + outputLine
        firstLine = 1
        return

    # if its not the first line in the paragraph
    if formatInfo["JUST"] == "BULLET":  # check to see if it require spaces for bullets 
        for i in range(1, LM+2):
            outputLine = " " + outputLine
    else: # else add spaces w/o bullet format.
        for i in range (1, LM):
            outputLine = " " + outputLine

##### printText #####
# Purpose:
#   Function for printing the text.
# Parameters:
#   formatInfo - info for formating.
# Notes:
#   * If FLOW == "YES" && (current working formatted output line) is empty, There is nothing to print.
#   * Determine the format text width, which is different for bullets.
#   * Determine the number of spaces for left margin.
#   * Depending on the value of JUST, print appropriately.
#       o Note that the bulleted paragraphs only print bullets for the first line in the paragraph.
# # # # # # # # # # # #
def printText(formatInfo):
    global outputLine

    # if the output line is empty and flow is on, don't do anything. (formatter handles this)
    if (outputLine == "") and (formatInfo["FLOW"] == "YES"):
        return

    addSpaces(formatInfo) # format the spacing for printing.
    print(outputLine)     # print out the formatted line.
    reset()               # reset the line after printing. 
    









