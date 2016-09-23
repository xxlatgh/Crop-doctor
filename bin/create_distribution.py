#!/use/bin/env Python

# Note: this script needs to be present at
# /home/cngan/plantvillage/create_distribution.py
# and executed from within the
# /home/cngan/plantvillage/
# directory

import glob
import os
import sys
import random
import shutil

def parsename(filepath, _image):
    '''
    return the parsed formatted new file name, file path, class name
    Some filenames contain spaces, which creates some incompatibility with a preprocessing script shipped with Caffe
    Hence we replace all spaces in the filename with _
    '''
    className = _image.split("/")[-2]
    newFileName = _image.split("/")[-1]
    newFileName = newFileName.replace(" ", "_")
    newFilePath = filepath + className+ "/" + newFileName
    shutil.move(_image, newFilePath)
    newClassName = className.split("_")[-1]
    return newFileName, newFilePath, newClassName

def getTrainTestSet(filepath):
    '''
    return training sets and test sets
    '''
    TRAIN_PERCENTAGE = 70
    TRAIN_SET = []
    VAL_SET = []
    for _image in glob.glob(filepath+"*/*"):
        newFileName,newFilePath, newClassName = parsename(filepath, _image)
        if random.randint(0, 100) < TRAIN_PERCENTAGE:
            TRAIN_SET.append((newFilePath, newClassName))
        else:
            VAL_SET.append((newFilePath, newClassName))
    return TRAIN_SET, VAL_SET

def writefile(filename, dataset):
    '''Write the distribution into a text filename'''
    with open (filename, "w") as f:
        for _entry in dataset:
            f.write(_entry[0] + " " +_entry[-1] + "\n")
    return

def main(filepath):
    TRAIN_SET, VAL_SET = getTrainTestSet(filepath)
    try:
        os.mkdir("lmdb")
    except:
        pass
    writefile("lmdb/train.txt", TRAIN_SET)
    writefile("lmdb/val.txt", VAL_SET)
    return

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print "Error, no filepath provided"
        exit()

#    filepath = '../data/crowdai/'
