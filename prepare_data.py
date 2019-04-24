import glob
import os
import shutil

import xml_to_csv

test_train_directories = {}

##########################################################################
#               SPLIT TESTING AND TRAINING DATA                          #
# PLEASE PUT DATA IN RAW IMAGES FOLDER, EACH SUBFOLDER IS AN IMAGE CLASS #
##########################################################################

train_images = glob.glob("./rawImages/train/*")
test_images =  glob.glob("./rawImages/test/*")

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
#               CONVERTING DATA TO CSV    (store in data directory)      #
##########################################################################


print("gg")