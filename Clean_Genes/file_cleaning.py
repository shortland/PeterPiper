import os
"""Grabs .fasta files from folder this script is currently in, gets the sequence name by
finding the letters after the > character, gets the sequence by finding the letters after
the next | character, then strips any unknown bases (denoted by a -).

Code then appends to a list of lists titled dna, with each inner list composed in the format
[sequence_name, sequence]. Then, for each list in dna, changes * characters to &,
and changes / characters to % (* and / can't be used to name a file).

Creates a file with the new sequence name as sequence_name.txt, and puts the sequence inside
said file as one string."""

#Below looks for files ending in .fasta, then reads, cleans, and converts them.
for filename in os.listdir(os.getcwd()):
    if filename.endswith('.fasta'):
        contents = open(filename, "r").readlines()

#Looks for the lines starting with >, then grabs the title, and gets the cleaned sequence.
dna = []
for line in contents:
    
    if line[0] is '>':
        if 'sequence' in locals():#Checks if sequence exists, then adds title and sequence
                                  #to array.
            dna.append([title, sequence])
        title = ''
        sequence = ''

        #variable to see if we found the section containing the title yet
        begin = False
        for index, letter in enumerate(line[1:]):
            if not begin:
                if letter is '|':
                    #title section found, on next iteration it will jump to the next if statement
                    begin = True
                    continue
            if begin:
                if letter is '|':
                    #title complete, jump to the next line.
                    begin = False
                    break
                else:
                    title += letter
        continue
    
    for letter in line.strip():
        if letter is not '-':
            sequence += letter

#This append gets the final line that was skipped over.
dna.append([title, sequence])
for pair in dna:
    sequence_name = pair[0]
    for letter in sequence_name:
        if letter is '*':
            sequence_name = sequence_name.replace('*', '_')
        if letter is '/':
            sequence_name = sequence_name.replace('/', '__')
        # if letter is '-':
        #     sequence_name = sequence_name.replace('-', 'A')
    sequence = pair[1]
    with open("{}.txt".format(sequence_name), 'w') as file:
        file.write(sequence.upper())
file.close()
