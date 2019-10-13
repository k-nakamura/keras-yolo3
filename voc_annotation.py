import xml.etree.ElementTree as ET
from os import getcwd

sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ['Abyssinian', 'Bengal', 'Birman', 'Bombay', 'British_Shorthair', 'Egyptian_Mau', 'Maine_Coon', 'Persian',
           'Ragdoll', 'Russian_Blue', 'Siamese', 'Sphynx']


def convert_annotation(image_id, list_file):
    in_file = open('annotations/xmls/%s.xml' % image_id)
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = '_'.join(image_id.split('_')[:-1])
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))


wd = getcwd()


for year, image_set in sets:
    image_ids = open('annotations/trainval.txt').read().strip().split()
    list_file = open('train.txt', 'w')
    for image_id in image_ids:
        list_file.write('images/%s.jpg' % (image_id))
        convert_annotation(image_id, list_file)
        list_file.write('\n')

    list_file.close()

