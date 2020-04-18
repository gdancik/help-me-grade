#!/usr/bin/env python 

import sys


if len(sys.argv) != 3 :
    print('Usage: grade-notebooks notebookDirectory gradedDirectory')
    exit()


import re
import glob
import os

def gradeFile(fileName, gradedDirectory) :
    """ grades the given file and saves in graded directory """

    # read in file
    with open(fileName) as f :
        a = f.read()

    ### Update points per question
    qry = """ "### Question (\d+) <span style = 'font-size:80%'>\s*\[(\d+) points\]</span>\\\\n",\n """.strip()
    repl = """ "### Question \g<1> <span style = 'font-size:80%'>[\g<2> / \g<2> points]</span>\\\\n",
    "\\\\n",
    "<p style = 'color:red'> Great job! </p>",
    "\\\\n",
    """.strip()

    updated = re.sub(qry, repl, a)

    fileName = os.path.basename(fileName)
    # update total points and write to file
    fout = gradedDirectory + '/'+ fileName.replace('.ipynb', '_graded.ipynb')
    nameNum = 0
    with open(fout, 'w') as f :
        for line in updated.split('\n') :

            # look for name line
            if nameNum == 0 and "### Name:" in line :
                if line[-1] != ',' :
                    line += ','
                f.write(line + '\n')
                f.write('"\\n",\n')
                f.write('"<h2 style = \'color:red\'> 97 / 100 -- Great job! </h2>",\n')
                f.write('"\\n"')
                nameNum += 1
            else :
                # check next line, do we need to add a comma?
                if nameNum == 1 :
                    if line.strip() != ']' :
                        f.write(',\n')
                    nameNum += 1
                f.write(line + '\n')
        print(fileName, '--->', fout)


def gradeAllFiles(directory, gradedDirectory) :
    """grades all files in the given directory, then writes to gradedDirectory"""
    files = glob.glob(directory +'/*.ipynb')
    os.mkdir(gradedDirectory)
    for file in files :
        gradeFile(file, gradedDirectory)


gradeAllFiles(sys.argv[1], sys.argv[2])
