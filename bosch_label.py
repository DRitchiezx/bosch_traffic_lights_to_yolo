# by DRitchie ZJU
import xml.etree.ElementTree as ET
import pickle
import os
import yaml
from os import listdir, getcwd
from os.path import join


sets = ["train", "test"]

classes = ["Green","Red","GreenLeft","GreenRight","RedLeft","RedRight","Yellow","off","RedStraight","GreenStraight",
           "GreenStraightLeft","GreenStraightRight","RedStraightLeft","RedStraightRight"]


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return x, y, w, h

def convert_annotation(path_label, example):
    short_name = os.path.basename(example['path'])
    lable_file = path_label + short_name.replace('png','txt')
    out_file = open(lable_file, 'w')

    # Bosch
    h = 720  # Image height
    w = 1280  # Image width

    for box in example['boxes']:
        cls = box['label']
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
        b = (float(box['x_min']), float(box['x_max']), float(box['y_min']),
             float(box['y_max']))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    out_file.close()


wd = getcwd()

for image_set in sets:
    path_label = '../data/bosch_rgb/labels/%s/' % image_set

    if not os.path.exists(path_label):
        os.makedirs(path_label)


    # BOSCH
    INPUT_YAML = '../data/bosch_rgb/%s.yaml' % image_set
    examples = yaml.load(open(INPUT_YAML, 'rb').read())

    # examples = examples[:10]  # for testing
    len_examples = len(examples)
    print("Loaded ", len(examples), "examples")

    list_file = open('../data/bosch_rgb/labels/%s.txt' % image_set, 'w')
    counter = 0
    for i in range(len(examples)):
        if len(examples[i]['boxes']) == 0:
            continue
        examples[i]['path'] = os.path.abspath(os.path.join(os.path.dirname(INPUT_YAML), examples[i]['path']))
        list_file.write('%s\n' % examples[i]['path'])
        convert_annotation(path_label,  examples[i])

        if i % 10 == 0:
            print("Percent done", (i / len_examples) * 100)
        counter += 1

    list_file.close()

