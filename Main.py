import pandas as pd
import datetime
import nltk
from nltk import sent_tokenize, WhitespaceTokenizer
# nltk.download('punkt')
import os


# Returns the index of the array where the 1st occurrence of the substring is located
def getIndex(st, arr):
    for i, s in enumerate(arr):
        if st in s:
            return i


# Location of folder which contains the files to extract production data out of
loc = r'V:\APLA\jobs\AP\Deloitte\024104 - Deloitte 2020MY METI\01 Data\01 Organized\03 ' \
      r'Production\Thailand\Erawan\Production'

# Create empty mother_df
mother_df = pd.DataFrame(columns=['Field', 'Contract', 'Date', 'SalesGas_mmscf', 'Cond/Oil_bbl'])

# Iterate through .txt files in loc
for dir, subdir, files in os.walk(loc):

    # If files is not empty
    if files:
        # Open and read the .txt file
        for f in files:
            #print(f)
            lines = []
            with open(dir + '\\' + f, 'rt') as file:
                # Extract date from the file name
                date = datetime.datetime(int(f[0:4]), int(f[5:7]), int(f[8:10]))
                field = 'Erawan'

                for line in file:
                    lines.append(line)

            df = pd.DataFrame(columns=['Field', 'Contract', 'Date', 'SalesGas_mmscf', 'Cond/Oil_bbl'])

            # Extract just the section we need (Section 7. Platform Activities/Rema)
            startString = '7. Platform Activities/Rema'
            endString = '8. POB'
            startIndex = getIndex(startString, lines)
            endIndex = getIndex(endString, lines)

            try:
                # ERAWAN: Tranche 1, 2, 3, and Contract 4
                lines_new = lines[startIndex:endIndex]
                tranche1 = lines_new[getIndex('Tranche 1', lines_new)]
                tranche2 = lines_new[getIndex('Tranche 2', lines_new)]
                tranche3 = lines_new[getIndex('Tranche 3', lines_new)]
                contract4 = lines_new[getIndex('Contract 4', lines_new)]

                contracts = [tranche1, tranche2, tranche3, contract4]
                for contract in contracts:
                    # Tokenize the lines
                    default_st = nltk.sent_tokenize
                    sentences = default_st(text=contract)

                    for sentence in sentences:
                        # print(sentence)
                        # Tokenize sentence into words, tag words' pos
                        ws = WhitespaceTokenizer()
                        words = ws.tokenize(sentence)
                        #print(words)

                        # Read contents into df
                        df['Field'] = [field]
                        df['Contract'] = [words[0] + ' ' + words[1]]
                        df['Date'] = [date]
                        df['SalesGas_mmscf'] = [words[3]]
                        df['Cond/Oil_bbl'] = [words[4]]

                        mother_df = mother_df.append(other=df, ignore_index=True)

            except TypeError:
                print('error: ' + f)


print(mother_df)

# Write mother_df out to excel file
mother_df.to_csv(
    r'V:\APLA\jobs\AP\Deloitte\024104 - Deloitte 2020MY METI\06 PHDWin\prod work\Thailand\Erawan_output.csv')
