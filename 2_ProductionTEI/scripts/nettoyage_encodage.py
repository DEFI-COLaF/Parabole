import html

# 1. Lire le XML original
with open("./2_ProductionTEI/test.xml", "r", encoding="utf-8") as f:
    xml_data = f.read()

# 2. Décoder les entités HTML (comme &#233; → é)
decoded_xml = html.unescape(xml_data)

# 3. Écrire le XML décodé en UTF-8
with open("output2.xml", "w", encoding="utf-8") as f:
    f.write(decoded_xml)

print("Conversion terminée : output.xml encodé en UTF-8")
