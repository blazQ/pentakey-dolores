import os
import xml.etree.ElementTree as ET

xml_file_path = os.path.join("/home/musimathicslab/Scrivania/CacciaNegriRapa/pentakey/src/results", "TestScore.musicxml")

tree = ET.parse(xml_file_path)
root = tree.getroot()

def convert_note_to_uppercase(note):
    if note.text is not None:
        note.text = note.text.upper()

for note in root.findall(".//note"):
    if note.find(".//step") is not None:
        convert_note_to_uppercase(note.find(".//step"))

modified_xml_file_path = os.path.join("/home/musimathicslab/Scrivania/CacciaNegriRapa/pentakey/src/results", "TestScore.musicxml")
tree.write(modified_xml_file_path)

print("New file saved in:", modified_xml_file_path)