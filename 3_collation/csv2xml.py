import pandas as pd
import xml.etree.ElementTree as ET
from collections import defaultdict

input_file = "./collation_csv/collation_verset_1_dordogne_corrige.csv"
output_file = "./collation_xml/collation_bourciez_dordogne_verset_1.xml"

df = pd.read_csv(input_file, sep=",", header=None)
print(df)


root = ET.Element("root")

for col in range(1, len(df.columns)):
    french_version = df[col][0]
    if french_version:
        app_elem = ET.SubElement(root, "app", type=str(french_version))
    else:
        app_elem = ET.SubElement(root, "app")
    dict_content = defaultdict(str)
    for row in range(0, len(df)):
        version = str(df[col][row]).strip()
        code_version = str(df[0][row]).strip()
        if not version or version.lower() == "nan":
            continue
        if version in dict_content:
            dict_content[version]=dict_content[version] + " #" + code_version
        else:
            dict_content[version] = "#"+code_version
    for key in dict_content:
        rdg_elem = ET.SubElement(app_elem, "rdg", wit=dict_content[key])
        rdg_elem.text = key

tree = ET.ElementTree(root)
tree.write(output_file, encoding="utf-8")
