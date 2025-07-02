from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

# Omogući CORS za Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Promijeni na domen ako deployaš na prod
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/oglasi")
async def oglasi():
    SCRAPER_API_KEY = "568f532b77acf94aa5e40033d880fd15"
    target_url = (
        "https://www.willhaben.at/iad/gebrauchtwagen/auto/gebrauchtwagenboerse"
        "?PRICE_TO=15000&YEAR_MODEL_FROM=1990&YEAR_MODEL_TO=2025&DEALER=1"
    )
    scraperapi_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&render=true&url={target_url}"

    async with httpx.AsyncClient() as client:
        response = await client.get(scraperapi_url)

    soup = BeautifulSoup(response.text, "lxml")
    oglasi = []

    for ad in soup.select('article[data-testid="search-result-entry"]'):
        title_elem = ad.select_one("h2")
        price_elem = ad.select_one('span.Text-sc-1cyh90m-0.jKxjzO')
        link_elem = ad.select_one("a[href]")
        desc_elem = ad.select_one("p")

        title = title_elem.text.strip() if title_elem else None
        price = price_elem.text.strip() if price_elem else None
        link = f"https://www.willhaben.at{link_elem['href']}" if link_elem else None
        opis = desc_elem.text.strip() if desc_elem else ""

        if title and price:
            oglasi.append({
                "naslov": title,
                "cijena": price,
                "link": link,
                "opis": opis,
            })

    return oglasi
