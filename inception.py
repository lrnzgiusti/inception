# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 22:31:12 2018

@author: ince, Lorenzo Giusti
"""

import os
import sys
import multiprocessing
from time import time


""" Inserisco le variabili d'ambiente e faccio partire un timer per calcolare il tempo d'esecuzione  """
start = time()
first = "export PYTHONPATH=/facenet/src/"
os.system(first)
os.environ['PYTHONPATH'] = '/facenet/src/'

""" Divido le persone da cercare in singoli e lancio le eseguzioni in concorrenza  """
second = 'python3 google-images-download.py -k "'
seconds = []
for i in range(1,len(sys.argv)-1):
    seconds.append(second + sys.argv[i] + str('" -l ' + sys.argv[len(sys.argv)-1])  + " -t face -s medium -o datasets")

def e(s):
    os.system(s)

pool = multiprocessing.Pool(len(seconds))
pool.map(e, seconds) 
# 6.576474905014038

""" Avvio l' allineamento di train e test in concorrenza  """
third = "python facenet/src/align/align_dataset_mtcnn.py /datasets/train /datasets/trainX --image_size 160 --margin 32 --random_order --gpu_memory_fraction 0.25"
fourth = "python facenet/src/align/align_dataset_mtcnn.py /datasets/test /datasets/testX --image_size 160 --margin 32 --random_order --gpu_memory_fraction 0.25"
algn = [third, fourth]
pool = multiprocessing.Pool(2)
pool.map(e, algn)
#14.860678911209106


""" imposto il prcoesso di train e di classificazione """
fifth = "python facenet/src/classifier.py TRAIN /datasets/trainX /models/facenet/20170512-110547/20170512-110547.pb /models/facenet/model.pkl --batch_size 1000"
sixth = "python facenet/src/classifier.py CLASSIFY /datasets/testX /models/facenet/20170512-110547/20170512-110547.pb /models/facenet/model.pkl --batch_size 1000"
os.system(fifth) #36.60079789161682

os.system(sixth)
os.system("rm datasets/trainX/*.txt")
os.system("rm datasets/testX/*.txt")
print(time()-start) #54.48339486122131