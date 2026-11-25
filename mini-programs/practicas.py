import json
import os
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://borsapractiques.fib.upc.edu"
LIST_URL = f"{BASE_URL}/ca/ofertes?combine=&sector_id=&candidate_type_id=1&"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36"
})
session.cookies.update({
    os.getenv("FIB_SESSION"): os.getenv("FIB_SESSION_COOKIE")
})


def get_description(url: str) -> str:
    try:
        res = session.get(url, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        box = soup.select_one(".field--name-job-description .field__item") or soup.select_one(".field--name-job-description")
        if not box:
            return "Descripción no encontrada"

        lines = [
            f"- {el.get_text(' ', strip=True)}" if el.name == "li" else el.get_text(" ", strip=True)
            for el in box.find_all(["p", "li", "h2", "h3", "h4"])
            if el.get_text(strip=True)
        ]
        return "\n".join(lines) if lines else box.get_text("\n", strip=True)

    except requests.RequestException as e:
        return f"Error: {e}"


ofertas = []

for page in range(8):
    res = session.get(f"{LIST_URL}page={page}", timeout=15)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    rows = soup.select("table.views-view-table tbody tr")
    print(f"Página {page}: {len(rows)} ofertas")

    for row in rows:
        practice = row.select_one("td.views-field-name a")
        company = row.select_one("td.views-field-employer-alias a")

        if practice and company:
            url = urljoin(BASE_URL, practice["href"])
            ofertas.append({
                "practica": practice.get_text(" ", strip=True),
                "empresa": company.get_text(" ", strip=True),
                "descripcion": get_description(url)
            })
            time.sleep(0.5)

with open("ofertas_detalle.json", "w", encoding="utf-8") as f:
    json.dump(ofertas, f, ensure_ascii=False, indent=2)

print(f"Terminado: {len(ofertas)} ofertas guardadas.")