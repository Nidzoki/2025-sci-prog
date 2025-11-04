Steam Topsellers Scraper
Sve podatke dohvaćamo sa službene stranice Steama:
https://store.steampowered.com/search/?filter=topsellers
Ova stranica prikazuje trenutno najprodavanije igre na Steamu. HTML sadržaj stranice se dohvaća pomoću Steel API i parsira u Pythonu.

Korištene tehnologije:
Marimo za kreiranje interaktivnih ćelija i UI elemenata
BeautifulSoup za parsiranje HTML sadržaja
Steel API za dohvat web stranica
Google Generative AI za analizu i generiranje sažetaka

KAKO POKRENITI:
1. Instalirati sve potrebne pakete pip install marimo requests beautifulsoup4 google-generativeai
2. Nabaviti Steel API i Google AI API kljuceve(Marimo trenutno ne želi učitati API ključeve iz .env datoteke, zbog čega je potrebno staviti STEEL_API_KEY i GOOGLE_API_KEY direktno u kod u funkciji get_api_keys. Bez toga aplikacija neće raditi.)
3. Pokreni aplikaciju: marimo run scraper.py