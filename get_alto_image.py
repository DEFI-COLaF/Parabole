import requests
import time
import os 
import click
import shutil
import xml.etree.ElementTree as ET

def get_response(requete_url):
    response = requests.get(requete_url, stream=True)
    if response.status_code!=200:
        time.sleep(60)
        response = requests.get(requete_url, stream=True)
    return response


def get_pagination(pagination_response):
    root = ET.fromstring(pagination_response.text)
    pagination_number = root.find(".//structure/nbVueImages")
    return pagination_number.text


@click.command()
@click.argument('ark_id', type=str)
@click.option('-i', '--image', 'getimage', is_flag=True, default=False)
@click.option('-a', '--alto', 'getalto', is_flag=True, default=False)
def main(ark_id, getimage, getalto):
    """
    Script qui permet de récupérer les fichiers alto et/ou image d'un document Gallica à partir de son ark id.
    :param ark_id: identifiant ark du document à récupérer
    :type ark_id: str
    :param getimage: option à indiquer si l'on souhaite la récupération des images du document
    :type getimage: bool
    :param getalto: option à indiquer si l'on souhaite la récupération des altos du document
    :type getalto: bool
    """
    pagination_doc = f'https://gallica.bnf.fr/services/Pagination?ark={ark_id}'
    pagination_response = get_response(pagination_doc)
    pagination_number = get_pagination(pagination_response)
    for page_number in range(0,int(pagination_number)):
        if getimage:
            page_url = f'https://gallica.bnf.fr/iiif/ark:/12148/{ark_id}/f{page_number}/full/full/0/native.jpg'
            response = get_response(page_url)
            save_path = os.path.join(f'./image/{ark_id}_{page_number:03d}.jpg')
            with open(save_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
        if getalto:
            page_url = f"https://gallica.bnf.fr/RequestDigitalElement?O={ark_id}&E=ALTO&Deb={page_number}"
            response = get_response(page_url)
            save_path = os.path.join(f'./alto/{ark_id}_{page_number:03d}.xml')
            with open(save_path, 'w') as out_file:
                out_file.write(response.text)
        
        
        

        
if __name__ == "__main__":
    main()               