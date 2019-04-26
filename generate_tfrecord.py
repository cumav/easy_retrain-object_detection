"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=data/train_labels.csv  --output_path=train.record
  # Create test data:
  python generate_tfrecord.py --csv_input=data/test_labels.csv  --output_path=test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf

from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

# TO-DO replace this with label map
def class_text_to_int(row_label):

    for cat_id, cat_name in enumerate(categories):
        if row_label == cat_name:
            # needs to be min 1
            return cat_id + 1
        else:
            None


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    for directory in ["train", "test"]:
        writer = tf.python_io.TFRecordWriter("data/{}.record".format(directory))
        path = os.path.join("images", directory)
        examples = pd.read_csv("data/{}_labels.csv".format(directory))
        grouped = split(examples, 'filename')
        for group in grouped:
            tf_example = create_tf_example(group, path)
            writer.write(tf_example.SerializeToString())

        writer.close()
        output_path = os.path.join(os.getcwd(), "data/{}.record".format(directory))
        print('Successfully created the TFRecords: {}'.format(output_path))


if __name__ == '__main__':
    import glob
    import os

    import xml_to_csv

    test_train_directories = {}

    ##########################################################################
    #               SPLIT TESTING AND TRAINING DATA                          #
    # PLEASE PUT DATA IN RAW IMAGES FOLDER, EACH SUBFOLDER IS AN IMAGE CLASS #
    ##########################################################################

    train_images = glob.glob("./images/train/*")
    test_images = glob.glob("./images/test/*")

    ##########################################################################
    #               CONVERTING DATA TO CSV    (store in data directory)      #
    ##########################################################################

    # convert to csv and save in data
    store_directory = os.path.join(os.getcwd(), "data")
    # make if not existent
    if not os.path.exists(store_directory):
        os.makedirs(store_directory)

    categories = xml_to_csv.create_csv(store_directory)

    ##########################################################################
    #               CREATE LABELMAP           (store in this directory)      #
    ##########################################################################

    with open("object-detection.pbtxt", "w") as file:
        entry = ""
        for val, item in enumerate(categories):
            entry += 'item {\n name: "' + item + '"\n id: ' + str(val + 1) + '\n}\n'
        file.write(entry)


    ##########################################################################
    #               CREATING TFRECORD         (store in current directory)   #
    ##########################################################################

    tf.app.run()