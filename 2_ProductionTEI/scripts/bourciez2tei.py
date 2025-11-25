from lxml import etree
import re
import glob
import unicodedata
from pathlib import Path
import os
import pandas as pd
from math import radians, cos, sin, asin, sqrt


# Load GPS coordinates from CSV
gps_df = pd.read_csv('../1_source/transcrib_Bourciez/gps_bourciez.csv', sep=';')
print(f"Loaded {len(gps_df)} GPS records")
print(f"GPS columns: {gps_df.columns.tolist()}")

# Load geonames data (France only, ADMIN4 level only)
cols_geonames = [
    "geonameid", "name", "asciiname", "alternatenames", "latitude", "longitude",
    "feature_class", "feature_code", "country_code", "cc2", "admin1_code",
    "admin2_code", "admin3_code", "admin4_code", "population", "elevation",
    "dem", "timezone", "modification_date"
]
geonames_full_df = pd.read_csv('allCountries.txt', sep='\t', header=None, names=cols_geonames, dtype=str, na_filter=False)
# Filter for France AND ADMIN4 level (non-empty admin4_code) AND feature code P (city/town/commune)
geonames_df = geonames_full_df[
    (geonames_full_df['country_code'] == 'FR') & 
    (geonames_full_df['admin4_code'] != '') &
    (geonames_full_df['admin4_code'].notna()) &
    (geonames_full_df['feature_class'] == 'P')  # Only populated places
].copy()
print(f"Filtered to {len(geonames_df)} ADMIN4 level populated place entries for France")

# Convert coordinates to float
geonames_df['latitude'] = pd.to_numeric(geonames_df['latitude'], errors='coerce')
geonames_df['longitude'] = pd.to_numeric(geonames_df['longitude'], errors='coerce')
gps_df['y'] = pd.to_numeric(gps_df['y'], errors='coerce')
gps_df['x'] = pd.to_numeric(gps_df['x'], errors='coerce')

# Build legacy geonames_dict for fallback
geonames_dict = {}
with open('allCountries.txt', "r", encoding="utf-8") as f:
    for line in f:
        cols = line.strip().split("\t")
        geonameid = cols[0]
        name = cols[1]
        geonames_dict[name] = geonameid

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in km between two GPS coordinates"""
    if pd.isna(lat1) or pd.isna(lon1) or pd.isna(lat2) or pd.isna(lon2):
        return float('inf')
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km

def find_geonames_by_coordinates(place_name, latitude, longitude, max_distance=2):
    """Find geonames entry closest to GPS coordinates within max_distance km"""
    if pd.isna(latitude) or pd.isna(longitude):
        return None, None, None
    
    # Calculate distance to all geonames entries
    distances = geonames_df.apply(
        lambda row: haversine_distance(latitude, longitude, row['latitude'], row['longitude']),
        axis=1
    )
    
    # Filter by distance
    valid_matches = distances[distances <= max_distance]
    
    if valid_matches.empty:
        return None, None, None
    
    # Sort by distance only (ascending - closest first)
    candidates_idx = valid_matches.index
    candidates = geonames_df.loc[candidates_idx].copy()
    candidates['distance'] = distances[candidates_idx]
    
    candidates = candidates.sort_values(['distance'], ascending=[True])
    
    best_match = candidates.iloc[0]
    return best_match['geonameid'], best_match['name'], best_match['distance']

dict_geonames_region = {"Gironde": "3015948","Gers":"3016194", "Dordogne":"3021042", "Haute-Garonne":"3013767", "Hautes-Pyrénées":"3013726", "Landes":"3007866", "Lot-et-Garonne":"2997523", "Pyrénées-Atlantiques":"2984887", "Tarn-et-Garonne":"2973357"}


ns={'tei':"http://www.tei-c.org/ns/1.0"}
root_xml = etree.Element("TEI", xmlns="http://www.tei-c.org/ns/1.0")
Teiheader_xml = etree.SubElement(root_xml, "TEIHeader")
profiledesc_xml = etree.SubElement(Teiheader_xml, "profileDesc")
settingdesc_xml = etree.SubElement(profiledesc_xml, "settingDesc")
listplace_xml = etree.SubElement(settingdesc_xml, "listPlace")
text_xml = etree.SubElement(root_xml, "text")
body_xml = etree.SubElement(text_xml, "body")
n_parabole = 0
dict_localisation={}
dict_geonames_place={}  # Map geonames ID to place element
n_localisation=0
n_person = 0
list_file = []
for file in glob.glob('../1_source/transcrib_Bourciez/*/*/*/*'):
    if file.endswith('.txt'):
        list_file.append(file)
for file in glob.glob('../1_source/transcrib_Bourciez/*/*/*'):
    if 'txt' in file:
        list_file.append(file)

for file in list_file:
    n_parabole+=1
    div_xml = etree.SubElement(body_xml, 'div',type="parabole", n=str(n_parabole))
    with open(file, "r") as f:
        plain_text = f.read()
    list_par = plain_text.split('\n')
    head_xml = etree.SubElement(div_xml, 'head')
    div_xml.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "bourciez-gasc-1240-"+str(n_parabole)
    div_xml.attrib["{http://www.w3.org/XML/1998/namespace}lang"] = "gasc-1240"
    auteur = list_par[2]
    n_person +=1
    person_xml = etree.SubElement(profiledesc_xml, "person")
    person_id = "person_"+str(n_person)
    person_xml.attrib["{http://www.w3.org/XML/1998/namespace}id"] = person_id
    p_xml = etree.SubElement(person_xml, "p")
    p_xml.text = auteur
    div_xml.attrib["hand"] = "#" + person_id
    
    list_file_path = file.split('/')
    localisation = list_file_path[-1].replace(".txt", "")
    
    # Try to find geonames ID using GPS coordinates first
    gps_row = gps_df[gps_df['comuna'] == localisation]
    geonames_id = None
    geonames_name = None
    
    if gps_row.empty:
        # Try alternative column names in GPS CSV
        for col in gps_df.columns:
            if 'place' in col.lower() or 'id' in col.lower():
                gps_row = gps_df[gps_df[col] == localisation]
                if not gps_row.empty:
                    break
    
    if not gps_row.empty:
        lat = gps_row.iloc[0]['y']
        lon = gps_row.iloc[0]['x']
        geonames_id, geonames_name, distance = find_geonames_by_coordinates(localisation, lat, lon, max_distance=2)
        
        # If no match within 2km, try with larger distance threshold (5km)
        if geonames_id is None:
            print(f"  ⚠️  No match found for {localisation} within 2km, trying 5km...")
            geonames_id, geonames_name, distance = find_geonames_by_coordinates(localisation, lat, lon, max_distance=5)
        if geonames_id is not None:
            print(f"  ✓ Matched {localisation} at {distance:.2f}km")
        else:
            print(f"  ✗ NO MATCH FOUND for {localisation} - no geonames entry within 5km")
    else:
        print(f"  ✗ NO GPS COORDINATES found for {localisation}")
    
    # Check if we already have a place element with this geonames ID
    if geonames_id and geonames_id in dict_geonames_place:
        localisation_id = dict_geonames_place[geonames_id]
        print(f"Reusing existing place {localisation_id} for {localisation} (geonames: {geonames_id})")
        
        # If the location name is different, add it as alternative name
        if localisation != geonames_name and localisation not in [elem.text for elem in listplace_xml.findall(f".//tei:place[@{{http://www.w3.org/XML/1998/namespace}}id='{localisation_id}']/tei:settlement/tei:name[@type='alternative']", namespaces=ns)]:
            place_xml = listplace_xml.find(f".//tei:place[@{{http://www.w3.org/XML/1998/namespace}}id='{localisation_id}']", namespaces=ns)
            if place_xml is not None:
                settlement_xml = place_xml.find('tei:settlement', namespaces=ns)
                if settlement_xml is not None:
                    alt_name_xml = etree.SubElement(settlement_xml, "name", type="alternative")
                    alt_name_xml.text = localisation
                    print(f"  Added alternative name: {localisation}")
    else:
        # Create new place element
        n_localisation+=1
        localisation_id = "place_"+str(n_localisation)
        dict_localisation[localisation] = localisation_id
        if geonames_id:
            dict_geonames_place[geonames_id] = localisation_id
        
        place_xml = etree.SubElement(listplace_xml, "place")
        place_xml.attrib["{http://www.w3.org/XML/1998/namespace}id"] = localisation_id
        place_settlement_xml = etree.SubElement(place_xml, "settlement")
        place_settlement_name_xml = etree.SubElement(place_settlement_xml, "name")
        place_settlement_name_xml.text = localisation
        
        # Add geonames name if different from bourciez name
        if geonames_name and geonames_name != localisation:
            geonames_name_xml = etree.SubElement(place_settlement_xml, "name", type="geonames")
            geonames_name_xml.text = geonames_name
            print(f"  Added geonames name: {geonames_name}")
        
        place_settlement_geonames_xml = etree.SubElement(place_settlement_xml, "idno", type="geonames")
        place_settlement_geonames_xml.text = geonames_id
        place_canton_xml = etree.SubElement(place_xml, "region", type="canton")
        place_canton_name_xml = etree.SubElement(place_canton_xml, "name")
        place_canton_name_xml.text = list_file_path[-2]
        place_region_xml = etree.SubElement(place_xml, "region", type="departement")
        place_region_name_xml = etree.SubElement(place_region_xml, "name")
        place_region_name_xml.text = list_file_path[3]
        place_region_geonames_xml = etree.SubElement(place_region_xml, "idno", type="geonames")
        place_region_geonames_xml.text = dict_geonames_region.get(list_file_path[3], None)
    
    div_xml.attrib["corresp"] = "#"+ localisation_id


    head_xml.text = list_par[4]
    for par in list_par[6:min(15, len(list_par))]:
        if re.match(r"^\d{1}\.", par):
            p =  etree.SubElement(div_xml, "p")
            num = etree.SubElement(p,'num')
            num.text = re.match(r'^\d{1}\.', par).group(0)
            #nettoyage du text et tag des notes
            text = re.sub(r'^\d{1}\.', '', par)
            num.tail = text

    if len(list_par)>16:
        note_xml = etree.SubElement(div_xml, 'note')
        for par in list_par[16:]:
            if par and par != "":
                note_p_xml = etree.SubElement(note_xml, 'p')
                note_p_xml.text = par

with open('test.xml', 'w', encoding='utf-8') as f:
    f.write(etree.tostring(root_xml).decode('utf-8'))
