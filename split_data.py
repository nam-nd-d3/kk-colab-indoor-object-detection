# coding:utf-8
"""
Name : split_data.py
Author : Nam Nguyen
Contact : nam.nd.d3@gmail.com
Time    : 7/22/2021 1:47 PM
Desc:
"""
import logging
import os
import shutil

from numpy import random
from tqdm import tqdm


def split_two_folds(paths):
    random.shuffle(paths)

    rating = int(round(0.5 * len(paths)))
    fold1 = paths[:rating]
    fold2 = paths[rating:]

    return fold1, fold2


def copy_file(input_path, f, fold_path):
    f_current_path = os.path.join(input_path, f)
    f_des_path = os.path.join(fold_path, f)
    shutil.copy(f_current_path, f_des_path)


def get_name(file):
    return str(file).split(".")[0]


def get_ext(file):
    return file.split["."][-1]


def attach_name_n_exts(name, ext):
    return f"{name}.{ext}"


def move_files(current_path, des_path):
    shutil.move(current_path, des_path)
    return True


if __name__ == "__main__":
    input_xml_path = "./data/annotations/pascal_voc_xmls/"
    input_img_path = "./data/images/"

    fold1_img_path = "./data/fold1/images"
    fold1_xml_path = "./data/fold1/annotations"

    fold2_img_path = "./data/fold2/images"
    fold2_xml_path = "./data/fold2/annotations"

    if not os.path.exists(fold1_img_path):
        os.makedirs(fold1_img_path)
    if not os.path.exists(fold1_xml_path):
        os.makedirs(fold1_xml_path)
    if not os.path.exists(fold2_img_path):
        os.makedirs(fold2_img_path)
    if not os.path.exists(fold2_xml_path):
        os.makedirs(fold2_xml_path)

    xml_files = os.listdir(input_xml_path)
    img_files = os.listdir(input_img_path)

    xml_ext = ".xml"
    img_ext = ".jpg"

    xml_name_files = [get_name(f) for f in xml_files]
    img_name_files = [get_name(f) for f in img_files]

    print("Number of XML files: ", len(xml_name_files))
    print("Number of image files: ", len(img_name_files))

    if len(xml_name_files) != len(img_name_files):
        logging.error("Number of xml files should be equal number of image files!")
    fold1_dirs, fold2_dirs = split_two_folds(xml_name_files)

    with tqdm(total=len(fold1_dirs)) as progressbar:
        progressbar.set_description("Copying images")
        for f1 in fold1_dirs:
            f1_xml = f1 + xml_ext
            f1_img = f1 + img_ext
            copy_file(input_xml_path, f1_xml, fold1_xml_path)
            copy_file(input_img_path, f1_img, fold1_img_path)

            progressbar.update(1)

    with tqdm(total=len(fold2_dirs)) as progressbar:
        progressbar.set_description("Copying images")
        for f2 in fold2_dirs:
            f2_img = f2 + img_ext
            f2_xml = f2 + xml_ext
            copy_file(input_xml_path, f2_xml, fold2_xml_path)
            copy_file(input_img_path, f2_img, fold2_img_path)

            progressbar.update(1)
