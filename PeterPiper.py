#!/usr/bin/env python3

import subprocess
import os
from os import listdir
from os.path import isfile, join
from random import randint

class Piper:
    def __init__(self, directory, run_all = False):
        self.directory = directory
        self.file_list = [f for f in listdir(directory) if isfile(join(directory, f))]

        if run_all:
            # meme-in-file which will contain all the sequences in FASTA format
            # returns the name/location of the file
            meme_in_file = self.create_meme_in_file("meme_data_%s" % str(randint(1000, 100000)))
            # the bash command for executing the meme-motif...
            meme_cmd = "meme meme_in/%s" % meme_in_file
            # returns the name/location of the bash executable file
            meme_exec_name = self.create_bash_file("meme_execs/meme_cmd_%s" % str(randint(1000, 100000)), meme_cmd)
            # for each file in the 'data' directory, take in their contents then append to a single file in FASTA format
            i = 0
            for file_name in self.file_list:
                if file_name[0] == ".":
                    continue
                # opens file "data/...". reads content and appends FASTA ">sequence" prefix, 
                # returns new formatted FASTA sequence
                meme_data = self.parse_meme_file("data/%s" % file_name, i)
                self.append_meme_in_file("meme_in/%s" % meme_in_file, meme_data)

                ## TODO: !!!!
                #### QGRS PORTION, MOVE OUT EVENTUALLY!!!
                qgrs_command = "./qgrs -i data/%s -t 2 -s 5 -v -o qgrs_out/%s" % (file_name, file_name)
                res = subprocess.check_output(qgrs_command.split())
                for line in res.splitlines():
                    print(line)

                # ## TODO: !!!!
                # #### VIENNA PORTION, MOVE OUT EVENTUALLY!!!
                # with open("data/%s" % file_name, "rb") as infile, open("vienna_out/%s" % file_name, "wb") as outfile:
                #     subprocess.check_call(["/Users/ilankleiman/Desktop/Serve/viennacmd"], stdin=infile, stdout=outfile)
                vienna_cmd = "sudo RNAfold -p -d2 -g --noLP -P dna_mathews2004.par --noconv < data/%s > vienna_out/%s" % (file_name, file_name)
                vienna_exec_name = self.create_bash_file("vienna_execs/vienna_cmd_%s" % str(randint(1000, 100000)), vienna_cmd)
                print(self.vienna_execute(vienna_exec_name))

                self.join_qgrs_vienna("vienna_out/%s" % file_name, "qgrs_out/%s" % file_name, "%s" % file_name)

                i += 1
            # returns the response of executing the meme executable.
            print(self.meme_motif(meme_exec_name))
        
    def create_bash_file(self, file_name, cmd):
        data = open(file_name, "w")
        data.write("#!/usr/bin/env bash\n")
        data.write(cmd)
        return file_name

    def create_meme_in_file(self, file_name):
        data = open("meme_in/%s" % file_name, "w")
        return file_name

    def append_meme_in_file(self, file_path, fasta_data):
        data = open(file_path, "a")
        data.write("%s\n" % fasta_data)
        data.close()

    def parse_meme_file(self, file_name, i):
        data = open(file_name, "r")
        file_data = ">sequence%s\n" % i
        file_data += data.read()
        return file_data

    def meme_motif(self, exec_name):
        os.chmod(exec_name, 0o755)
        return subprocess.call(exec_name, shell=True)

    def vienna_execute(self, exec_name):
        os.chmod(exec_name, 0o755)
        return subprocess.call(exec_name, shell=True)

    def join_qgrs_vienna(self, qgrs_path, vienna_path, original_naming):
        filenames = [qgrs_path, vienna_path]
        with open("vienna_qgrs_outs/%s" % original_naming, 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)
    

# Run: QGRS
# Input: [qgrs_input.txt]
# Output: [qgrs_output.txt]


# Run: Vienna
# Input: [vienna_input.txt]
# Output: [vienna_output.out]

executable = Piper('data', True)