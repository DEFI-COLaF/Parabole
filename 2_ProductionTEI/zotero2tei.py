from lxml import etree
import re

import os


ns={'tei':"http://www.tei-c.org/ns/1.0"}
root_xml = etree.Element("TEI", xmlns="http://www.tei-c.org/ns/1.0")
text_xml = etree.SubElement(root_xml, "text")
body_xml = etree.SubElement(text_xml, "body")
n_parabole = 0
for file in os.listdir('zotero_export/'):
    n_parabole+=1
    tree = etree.parse('zotero_export/'+file)
    root = tree.getroot()
    div_xml = etree.SubElement(body_xml, 'div',type="parabole", n=str(n_parabole))
    
    
    note = root.findall('.//tei:note', namespaces=ns)[1]
    lines = note.text.strip()
    paragraphs = lines.split('\n')
    for par in paragraphs:
        if re.match(r"\d{2}", par):
            p =  etree.SubElement(body_xml, "p")
            num = etree.SubElement(p,'num')
            num.text = re.match(r'^\d{2}', par).group(0)
            num.tail = re.sub(r'^\d{2}', '', par)
        elif par.startswith("Traduction"):
            head = etree.SubElement(body_xml, "head")
            head.text=par

print(etree.tostring(root_xml))
with open('test.xml', 'w') as f:
    f.write(etree.tostring(root_xml).decode('utf-8'))