import os, json
from glob import glob
import numpy as np
np.set_printoptions(precision=4, linewidth=100)
from matplotlib import pyplot as plt
from PIL import Image as Image

import utils; reload(utils)
from utils import plots

import vgg16
from vgg16 import Vgg16
from vgg16bn import Vgg16BN

def top5(preds):
    top5_idxs_acending = np.argsort(preds, axis=1)[:, -5:]
    top5_idxs=[]
    for i in top5_idxs_acending:
        newi =i [::-1]
#        newi = sorted(i, reverse=True)
        top5_idxs.append(newi)
    return top5_idxs
top5_idxs_acending = np.argsort(preds, axis=1)[:, -5:]

def pred_batch(preds, filenames):
#    preds = model.predict(imgs)
    idxs = np.argmax(preds, axis=1)
    top5_idxs = top5(preds)
    print('Shape: {}'.format(preds.shape))
    print('First (unsorted) 5 classes: {}'.format(imgclasses[:5]))
    print('First (unsorted) 5 probabilities : {}\n'.format(preds[0, :5]))
    print('Predictions prob/class: ')

    for i in range(len(idxs)):
        top_idx = idxs[i]
        top5_idx = top5_idxs[i]
        if preds[i, idx]>0.80:
            print ('  {}/{}'.format(preds[i, idx], imgclasses[idx]))
            print (filenames[i])

def pred_single(preds, filenames, idx):
    idxs = np.argmax(preds, axis=1)
    top5_idxs = top5(preds)
    print('Predictions prob/class: ')

    top_idx = idxs[idx]
    top5_idx = top5_idxs[idx]

    print idx, top5_idx
    for j in range(5):
        print ('  {}/{}'.format(preds[idx, top5_idx[j]], imgclasses[top5_idx[j]]))
    print (filenames[idx])

batch_size =64

path = "data/labeldata/sample/"
test_path = path+ 'test/'

'''
load data
'''
batches = get_batches(path+'train', batch_size=batch_size)
val_batches = get_batches(path+'valid', batch_size=batch_size*2, shuffle=False)

(val_classes, trn_classes, val_labels, trn_labels,
    val_filenames, filenames, test_filenames) = get_classes(path)

trn = get_data(path+'train')
val = get_data(path+'valid')

test = get_data(path+'test')
save_array(path+'results/trn.dat', trn)
save_array(path+'results/val.dat', val)
save_array(path+'results/test.dat', test)
trn = load_array(path+'results/trn.dat')
val = load_array(path+'results/val.dat')

results_path = path+'results/'
test = load_array(path+'results/test.dat')

'''
create model
'''
gen = image.ImageDataGenerator()
model = vgg_ft_bn(54)
model.compile(optimizer=Adam(1e-3),
       loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(trn, trn_labels, batch_size=batch_size, nb_epoch=20, validation_data=(val, val_labels))
model.save_weights(path+'results/vgg_bn_ft20.h5')


'''
predict outcome
'''
preds = model.predict(test, batch_size=batch_size*2 )
imgclasses = []
train_path = path +'train'
for item in os.listdir(train_path):
    if os.path.isdir(os.path.join(train_path, item)):
        if item not in imgclasses:
            imgclasses.append(item)
print imgclasses[0], imgclasses[len(imgclasses)-1], len(imgclasses)

for i in range(len(idxs)):
    idx = idxs[i]
    out='{:.4f}/{}'.format(preds[i, idx], imgclasses[idx])
    print idx
    print (''.join(out))

for i in range(len(test_filenames)):
    pred_single(preds, test_filenames, i)
    Image.open(test_path + test_filenames[i])
