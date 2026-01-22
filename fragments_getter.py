import os
import requests
from bs4 import BeautifulSoup
import re

output_dir = "./Literatura - original"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

books_map = {
    "https://wolnelektury.pl/katalog/lektura/chlopi-czesc-pierwsza-jesien.html": "reymont_jesien.txt",
    "https://wolnelektury.pl/katalog/lektura/reymont-chlopi-zima.html": "reymont_zima.txt",
    "https://wolnelektury.pl/katalog/lektura/chlopi-czesc-trzecia-wiosna.html": "reymont_wiosna.txt",
    "https://wolnelektury.pl/katalog/lektura/chlopi-czesc-czwarta-lato.html": "reymont_lato.txt",
    
    "https://wolnelektury.pl/katalog/lektura/ogniem-i-mieczem-tom-pierwszy.html": "sienkiewicz_ogniem.txt",
    "https://wolnelektury.pl/katalog/lektura/potop-tom-pierwszy.html": "sienkiewicz_potop.txt",
    "https://wolnelektury.pl/katalog/lektura/pan-wolodyjowski.html": "sienkiewicz_wolodyjowski.txt",
    
    "https://wolnelektury.pl/katalog/lektura/czerwony-kapturek.html": "basnie_kapturek.txt",
    "https://wolnelektury.pl/katalog/lektura/jas-i-malgosia.html": "basnie_jas_malgosia.txt",
    "https://wolnelektury.pl/katalog/lektura/mali-czarodzieje.html": "basnie_czarodzieje.txt",
    "https://wolnelektury.pl/katalog/lektura/roszpunka.html": "basnie_roszpunka.txt",
    "https://wolnelektury.pl/katalog/lektura/sniezka.html": "basnie_sniezka.txt",
    
    "https://wolnelektury.pl/katalog/lektura/doyle-dolina-trwogi.html": "doyle_dolina.txt",
    "https://wolnelektury.pl/katalog/lektura/doyle-znak-czterech.html": "doyle_znak.txt",
    "https://wolnelektury.pl/katalog/lektura/pies-baskervilleow.html": "doyle_pies.txt",
    "https://wolnelektury.pl/katalog/lektura/doyle-studium-w-szkarlacie.html": "doyle_studium.txt",

    "https://wolnelektury.pl/katalog/lektura/wagner-banda-z-norrtull.html": "wagner_banda.txt",
    "https://wolnelektury.pl/katalog/lektura/arystoteles-poetyka.html": "arystoteles_poetyka.txt",
    "https://wolnelektury.pl/katalog/lektura/grabinski-ksiega-ognia-zielone-swiatki.html": "grabinski_ksiega.txt",
}

def download_and_process_book(url, filename, char_limit=45000):
    try:
        print(f"Downloading: {filename}...")
        response = requests.get(url)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        book_container = soup.find('div', id='book-text')
        
        if book_container:
            themes_div = book_container.find('div', id='themes')
            if themes_div:
                themes_div.decompose() 

            paragraphs = book_container.find_all('p')
            
            full_text = " ".join([p.get_text() for p in paragraphs])
            
            clean_text = re.sub(r'\s+', ' ', full_text).strip()
            
            limit = min(len(clean_text), char_limit)
            final_text = clean_text[:limit]
            
            file_path = os.path.join(output_dir, filename)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(final_text)
                
            print(f" -> Saved {limit} characters to {file_path}")
        else:
            print(f" -> WARNING: Div 'book-text' not found in {filename}")
        
    except Exception as e:
        print(f" -> ERROR with {filename}: {e}")

for url, fname in books_map.items():
    download_and_process_book(url, fname)

print("\nDone! All files are located in the 'Literatura - original' folder.")