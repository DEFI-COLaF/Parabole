import xml.etree.ElementTree as ET
import csv

tei_file = "Bourciez.xml"
geonames_file = "./2_ProductionTEI/allCountries.txt" 

tei_ns = {"tei": "http://www.tei-c.org/ns/1.0"}
tei_tree = ET.parse(tei_file)
tei_root = tei_tree.getroot()

id_map = []
for place in tei_root.findall(".//tei:listPlace/tei:place", tei_ns):
   place_el_id = place.attrib.get("{http://www.w3.org/XML/1998/namespace}id")
   if place.find("./tei:settlement", tei_ns):
      place_geonamesId = place.find("./tei:settlement/tei:idno[@type='geonames']", tei_ns)
      id_map.append((place_el_id, place_geonamesId.text))
   else:
      place_geonamesId = place.find("./tei:region/tei:idno[@type='geonames']", tei_ns)
      id_map.append((place_el_id, place_geonamesId.text))
                
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

with open("output_qgis.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(['par_id', "geonames","longitude", "latitude"])
    for (place_id, geoname_id) in id_map:
        lon, lat = geonames_dict.get(geoname_id, (None, None))
        writer.writerow([place_id, geoname_id, lon, lat])

print(f"CSV écrit dans {output_file}")
