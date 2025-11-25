from lxml import etree
import re
import os



def extract_page(filename):
    match = re.search(r'_p(\d{3})', filename)
    return int(match.group(1)) if match else float('inf')



ns={'tei':"http://www.tei-c.org/ns/1.0"}
root_xml = etree.Element("TEI", xmlns="http://www.tei-c.org/ns/1.0")
text_xml = etree.SubElement(root_xml, "text")
body_xml = etree.SubElement(text_xml, "body")
n_parabole = 0
list_file = []
for file in os.listdir('../1_source/transcrib_1831/'):
    list_file.append(file)
sorted_list = sorted(list_file, key=extract_page)

for file in sorted_list:
    n_parabole+=1
    tree = etree.parse('../1_source/transcrib_1831/'+file)
    root = tree.getroot()
    div_xml = etree.SubElement(body_xml, 'div',type="parabole", n=str(n_parabole))
    pb_xml = etree.SubElement(div_xml, 'pb', n=str(extract_page(file)))
    note = root.findall('.//tei:note', namespaces=ns)[1]
    lines = note.text.strip()
    paragraphs = lines.split('\n')
    for par in paragraphs:
        if re.match(r"\d{2}", par):
            p =  etree.SubElement(div_xml, "p")
            num = etree.SubElement(p,'num')
            num.text = re.match(r'^\d{2}', par).group(0)
            num.tail = re.sub(r'^\d{2}', '', par)
        elif par.startswith("Traduction"):
            head = etree.SubElement(div_xml, "head")
            head.text=par

with open('test.xml', 'w') as f:
    f.write(etree.tostring(root_xml).decode('utf-8'))
