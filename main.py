from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Flutter može da zove
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/oglasi")
async def get_oglasi():
    url = "https://api.scraperapi.com?api_key=OVDE_STAVI_TVOJ_API_KEY&url=https://www.willhaben.at/iad/gebrauchtwagen/auto/gebrauchtwagenboerse?PRICE_TO=15000&YEAR_MODEL_FROM=1990&YEAR_MODEL_TO=2025"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    soup = BeautifulSoup(response.text, "lxml")
    oglasi = []

    for ad in soup.select("article[data-testid='search-result-entry']"):
        naslov = ad.select_one("h2")
        cijena = ad.select_one("span.Text-sc-1cyh90m-0.jKxjzO")
        link = ad.select_one("a[href]")
        opis = ad.select_one("p")

        oglasi.append({
            "naslov": naslov.text.strip() if naslov else "N/A",
            "cijena": cijena.text.strip() if cijena else "N/A",
            "link": f"https://www.willhaben.at{link['href']}" if link else "",
            "opis": opis.text.strip() if opis else "",
            "slika": None
        })

    return oglasi
