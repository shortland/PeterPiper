#!/usr/bin/env python3
import subprocess

# Run QGRS
# Input: Single Sequence File
qgrs_command = "./qgrs -i qgrs_input.txt -o qgrs_output.txt"
res = subprocess.check_output(qgrs_command.split())
for line in res.splitlines():
    print(line)
# Nothing should be printed to STDOUT. Output is placed into qgrs_output.txt

with open("vienna_input.txt", "rb") as infile, open("vienna_output.out", "wb") as outfile:
    subprocess.check_call(["/Users/ilankleiman/Desktop/Serve/viennacmd"], stdin=infile, stdout=outfile)

# try:
#     res = subprocess.check_output(vienna_command.split())
# except:
#     print('An error occured')
# for line in res.splitlines():
#     print(line)