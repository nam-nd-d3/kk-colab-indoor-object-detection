# coding:utf-8
"""
Name : convert_to_pascal_voc_xml.py
Author : Nam Nguyen
Contact : nam.nd.d3@gmail.com
Time    : 7/22/2021 8:11 AM
Desc:
"""
import logging
import os
import cv2

import xml.etree.ElementTree as ET
from PIL import Image
from tqdm import tqdm

BEGIN_ANNOTATION = '<annotation verified="no">'
END_ANNOTATION = '</annotation>'
INFORM_FORMAT = '''
  <folder>{}</folder>
  <filename>{}</filename>
  <path>{}</path>
  <source>
    <database>Unknown</database>
  </source>
  <size>
    <width>{}</width>
    <height>{}</height>
    <depth>{}</depth>
  </size>
  <segmented>0</segmented>
'''

OBJECT_FORMAT = '''<object>
<name>{}</name>
<pose>Unspecified</pose>
<truncated>0</truncated>
<Difficult>0</Difficult>
<bndbox>
  <xmin>{}</xmin>
  <ymin>{}</ymin>
  <xmax>{}</xmax>
  <ymax>{}</ymax>
</bndbox>
</object>
'''


def is_img_file(img_path):
    exts = [".jpg", ".png", ".jpeg"]
    is_exts = [lambda x: [x.endswith(y) for y in exts]]
    if any(is_exts):
        try:
            img = Image.open(img_path)
            img.verify()
            return True
        except (IOError, SyntaxError) as e:
            logging.error('Not image file:', img_path)
    return None


def get_img_file(img_path):
    return img_path.split(os.sep)[-1] if is_img_file(img_path) else None


def get_img_size(img_path):
    img_checked = is_img_file(img_path)
    if img_checked:
        try:
            img = cv2.imread(img_path)
            return img.shape
        except (IOError, SyntaxError) as e:
            logging.error("Can't reading image file:", img_path)
    return None


def get_img_info(img_path):
    # path: /root/project_name/data/images/fold_1/train_set/image.jpg
    train_set = img_path.split(os.sep)[-2]
    img_file = get_img_file(img_path)
    width_img, height_img, depth_img = get_img_size(img_path)

    return train_set, img_file, (width_img, height_img, depth_img)


def get_files_list(dir_path):
    return [os.path.join(dir_path, img_f) for img_f in os.listdir(dir_path)]


def get_boxes_n_labels(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    objs = []
    for child in root:
        label = child.find('label').text
        top, left, width, height = child.attrib['top'], \
                                   child.attrib['left'], \
                                   child.attrib['width'], \
                                   child.attrib['height']
        xmin = int(left)
        ymin = int(top)
        xmax = int(left) + int(width)
        ymax = int(top) + int(height)
        box = (xmin, ymin, xmax, ymax)
        obj = (box, label)
        objs.append(obj)

    return objs


def generate_pascal_voc_xml(img_path, xml_path):
    img_info = get_img_info(img_path)
    train_set = img_info[0]
    img_name = img_info[1]
    width_img, height_img, depth_img = img_info[2]

    str_output = BEGIN_ANNOTATION
    inform_xml = INFORM_FORMAT.format(train_set,
                                      img_name,
                                      img_path,
                                      width_img,
                                      height_img,
                                      depth_img)
    str_output += inform_xml

    xml_info = get_boxes_n_labels(xml_path)
    for objs in xml_info:
        (xmin, ymin, xmax, ymax), label_name = objs
        obj_xml = OBJECT_FORMAT.format(label_name,
                                       xmin,
                                       ymin,
                                       xmax,
                                       ymax)
        str_output += obj_xml

    str_output += END_ANNOTATION
    xml_output = ET.fromstring(str_output)

    return xml_output


def get_name(path):
    return path.split(os.sep)[-1]


def get_name_no_ext(path):
    return get_name(path).split(".")[0]


def main():
    imgs_dir_path = "./data/images"
    xmls_dir_path = "./data/annotations/xmls"
    output_dir_path = "./data/annotations/pascal_voc_xmls"
    if not os.path.exists(output_dir_path):
        os.mkdir(output_dir_path)

    imgs_path_list = get_files_list(imgs_dir_path)
    xmls_path_list = get_files_list(xmls_dir_path)

    print("[INFO] Number of images: ", len(imgs_path_list))
    print("[INFO] Number of xmls: ", len(xmls_path_list))
    count = 0
    with tqdm(total=len(imgs_path_list)) as progressbar:
        progressbar.set_description("[INFO] Processing:")
        for img, xml in zip(imgs_path_list, xmls_path_list):
            name_img = get_name_no_ext(img)
            name_xml = get_name_no_ext(xml)

            if name_img == name_xml:
                try:
                    xml_ot = generate_pascal_voc_xml(img, xml)
                    xml_output_path = os.path.join(output_dir_path, get_name(xml))
                    with open(xml_output_path, "wb") as file:
                        file.write(ET.tostring(xml_ot))
                    count += 1
                except IOError as e:
                    logging.error("Can't write xml!")
            else:
                continue
            progressbar.update(1)

    print("[INFO] Processed: ", count)


if __name__ == "__main__":
    main()
