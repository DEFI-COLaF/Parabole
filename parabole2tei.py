import os
from lxml import etree as ET
import re
import spacy

def apply_xslt(xml_file):
    """
    Parses an XML file and applies an XSLT transformation.
    
    :param xml_file: Path to the input XML file.
    :type xml_file: str
    :return: Transformed XML tree or None in case of error.
    :rtype: ElementTree
    """
    xslt_file = "alto2XMLsimple.xsl"
    try:
        xml_tree = ET.parse(xml_file)
        xslt_tree = ET.parse(xslt_file)
        transform = ET.XSLT(xslt_tree)
        return transform(xml_tree)
    except Exception as e:
        print(f"Error: {e}")
        return None

def add_tei_line(line,parent):
    """
    Add the textual content of the blocks to the corresponding ElementTree.
    """
    lb = ET.Element('lb')
    parent.append(lb)
    if re.match(r"^\d{2}", line.text):
        num = ET.SubElement(parent,'num')
        num.text = re.match(r'^\d{2}', line.text).group(0)
        num.tail = re.sub(r'^\d{2}', '', line.text)
    else:
        lb.tail = line.text
    

def add_p_head(liste_line, parent):
    last_el=None
    for line in liste_line:
        if line.text.startswith("Traduction"):
            last_el = ET.SubElement(parent, "head")
            add_tei_line(line, last_el)
        elif re.match(r"^\d{2}", line.text):
            last_el = ET.SubElement(parent, "p")
            add_tei_line(line, last_el)
        elif last_el:
            add_tei_line(line, last_el)
        else:
            with open('erreur.txt', 'w') as f:
                f.write(line.text)

def get_metadata(liste_line):
    liste_str_line = []
    for el in liste_line:
        liste_str_line.append(ET.tostring(el, encoding="unicode"))
    nlp=spacy.load("fr_core_news_sm")
    clean_text =  re.sub(r"<.*?>","", "".join(liste_str_line[:1]))
    doc = nlp(clean_text)
    person = [ent.text for ent in doc.ents if ent.label_=="PER"]
    location = [ent.text for ent in doc.ents if ent.label_=="LOC"]
    print(f"Person: {person}, Location:{location}")




root_xml = ET.Element("TEI", xmlns="http://www.tei-c.org/ns/1.0")
text_xml = ET.SubElement(root_xml, "text")
body_xml = ET.SubElement(text_xml, "body")
n_parabole = 0
n_pb = 0
for alto in sorted(os.listdir('alto_auto/')):
    n_pb+=1
    xml_simple = apply_xslt('alto_auto/'+alto)
    root = xml_simple.getroot()
    liste_zone = root.findall('region')
    pb = ET.SubElement(body_xml, "pb", n=str(n_pb))
    for zone in liste_zone:
        liste_line = zone.findall("line")
        liste_1_text = liste_line[0].text
        if 'Traduction' in liste_1_text:
            #nouvelle parabole
            n_parabole+=1
            div_nv_parabole = ET.SubElement(body_xml, "div", type="parabole", n=str(n_parabole))
            add_p_head(liste_line, div_nv_parabole)
            get_metadata(liste_line)
                    
        elif re.match(r"^\d{2}", liste_1_text):
            # fin de parabole avec début de paragraphe
            add_p_head(liste_line, div_nv_parabole)
        elif '—' in liste_1_text:
            pass
            #NumberingZone
            # traiter les régions qui contiennent number et parabole - erreurs
        else:
            bool_parabole = False
            n_index_par = 0
            for line in liste_line:
                n_index_par+=1
                if re.match(r"\d{2}", line.text):
                    bool_parabole = True
                    break
            if bool_parabole:
                last_p = div_nv_parabole.xpath('//p')[-1]
                for line in liste_line[:n_index_par]:
                    add_tei_line(line, last_p)
                add_p_head(liste_line[n_index_par:], div_nv_parabole)
            else:
                pass
                #paragraphes du front et table des matières (à encoder manuellement?)

with open(f'test.xml', "w") as f:
    f.write(ET.tostring(root_xml, encoding='unicode', pretty_print=True))