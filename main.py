import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import Fore, Style, init
import fade
import html

init(autoreset=True)

ascii_art = """
###################################################
#                                                 #
#         WEB SCRAPER - ZELIRO TOOL               #
#                                                 #
###################################################
"""
print(fade.purpleblue(ascii_art))

def download_file(url, folder):
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join(folder, os.path.basename(url))
        if filename.endswith('.css') or filename.endswith('.js'):
            try:
                content = response.text
                formatted_content = content
                if filename.endswith('.css'):
                    import cssbeautifier
                    formatted_content = cssbeautifier.beautify(content)
                elif filename.endswith('.js'):
                    import jsbeautifier
                    formatted_content = jsbeautifier.beautify(content)
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(formatted_content)
            except Exception as e:
                print(Fore.RED + f"Erreur lors de la mise en forme de {filename}: {e}")
        else:
            with open(filename, 'wb') as file:
                file.write(response.content)
        print(Fore.GREEN + f'Téléchargé : {filename}')
    else:
        print(Fore.RED + f'Échec du téléchargement : {url}')

def scrape_website(url, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    response = requests.get(url)
    if response.status_code != 200:
        print(Fore.RED + 'Impossible d\'accéder au site')
        return

    html_file = os.path.join(output_folder, 'index.html')
    soup = BeautifulSoup(response.text, 'html.parser')
    pretty_html = soup.prettify()
    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(pretty_html)
    print(Fore.CYAN + f'HTML sauvegardé et formaté : {html_file}')
    css_folder = os.path.join(output_folder, 'css')
    js_folder = os.path.join(output_folder, 'js')
    os.makedirs(css_folder, exist_ok=True)
    os.makedirs(js_folder, exist_ok=True)
    for css in soup.find_all('link', {'rel': 'stylesheet'}):
        css_url = urljoin(url, css['href'])
        download_file(css_url, css_folder)

    for js in soup.find_all('script', {'src': True}):
        js_url = urljoin(url, js['src'])
        download_file(js_url, js_folder)

    complete_art = """
########################################
#                                      #
#       TÉLÉCHARGEMENT TERMINÉ !       #
#                                      #
########################################
"""
    print(fade.purpleblue(complete_art))

url = input(Fore.YELLOW + 'Entrez l\'URL du site : ')
output_folder = 'site_extrait'
scrape_website(url, output_folder)

input(Fore.MAGENTA + '\nAppuyez sur Entrée pour fermer...')
