import xml.etree.ElementTree as ET
import csv

collation_file = "./2_xml/collation_11.xml"
tei_file = "../TEI_parabole.xml"
geonames_file = "allCountries.txt" 
output_file = "./3_import_qgis/avoir.csv"

tei_ns = {"tei": "http://www.tei-c.org/ns/1.0"}
tei_tree = ET.parse(tei_file)
tei_root = tei_tree.getroot()

id_map = {}  # ex: {"parabole_id": "geonames_id"}
for parabole in tei_root.findall(".//tei:div[@type='parabole']", tei_ns):
    parabole_id = parabole.attrib.get("{http://www.w3.org/XML/1998/namespace}id")
    corresp_place = parabole.attrib.get("corresp")
    if corresp_place is not None:
        place_id = corresp_place.replace("#", "")
        place_list = tei_root.findall(".//tei:listPlace/tei:place", tei_ns)
        for place_el in place_list:
            place_el_id = place_el.attrib.get("{http://www.w3.org/XML/1998/namespace}id")
            if place_el_id == place_id:
                if place_el.find("./tei:settlement", tei_ns):
                    place_geonamesId = place_el.find("./tei:settlement/tei:idno[@type='geonames']", tei_ns)
                    id_map[parabole_id] = (place_geonamesId.text, 'settlement')
                else:
                    place_geonamesId = place_el.find("./tei:region/tei:idno[@type='geonames']", tei_ns)
                    id_map[parabole_id] = (place_geonamesId.text, 'region')
                
                
coll_tree = ET.parse(collation_file)
coll_root = coll_tree.getroot()

pairs = []  # (geonameId, type_place, mot)
app= coll_root.find(".//app[@type='avait']")
for rdg in app.findall("./rdg"):
    wits = rdg.attrib.get("wit", "").split()
    mot = (rdg.text or "").strip()
    for wit in wits:
        wit = wit.lstrip("#")
        same_wit = "-".join(wit.split("-")[1:] + [wit.split("-")[0]])
        if same_wit in id_map:
            wit_dict, place_type = id_map[same_wit]
            pairs.append((wit_dict, place_type, mot))

geonames_dict = {}
with open(geonames_file, "r", encoding="utf-8") as f:
    for line in f:
        cols = line.strip().split("\t")
        if len(cols) > 5:
            geonameid = cols[0]
            name = cols[1]
            lat = cols[4]
            lon = cols[5]
            geonames_dict[geonameid] = (lon, lat)

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["geonames", "place_type", "mot", "longitude", "latitude"])
    for geoname_id, place_type, mot in pairs:
        lon, lat = geonames_dict.get(geoname_id, (None, None))
        writer.writerow([geoname_id, place_type, mot, lon, lat])

print(f"CSV écrit dans {output_file}")
