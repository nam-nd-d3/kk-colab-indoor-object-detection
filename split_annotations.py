import os
import xml.etree.ElementTree as ET

path = os.getcwd()
header = b"<?xml version='1.0' encoding='ISO-8859-1'?>\n"

for xml_file in os.listdir(path):
    if "xml" in xml_file:
        xml_folder = xml_file.split(".xml")[0]
        xml_folder_path = os.path.join(path, xml_folder)
        if not os.path.exists(xml_folder_path):
            os.mkdir(xml_folder_path)
        xml_path = os.path.join(path, xml_file)

        context = ET.iterparse(xml_path, events=('end',))
        for event, elem in context:
            if elem.tag == 'image':
                title = elem.get("file")
                title = title.split(".jpg")[0]
                print(title)
                filename = format(title + ".xml")
                with open(os.path.join(xml_folder_path, filename), 'wb') as f:
                    f.write(header)
                    f.write(ET.tostring(elem))
