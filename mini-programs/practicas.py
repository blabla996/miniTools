import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

base_url = "https://borsapractiques.fib.upc.edu/ca/ofertes?combine=&sector_id=&candidate_type_id=1&"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36"}

FIB_SESSION = os.getenv("FIB_SESSION")
FIB_SESSION_COOKIE = os.getenv("FIB_SESSION_COOKIE")

cookies = {
    FIB_SESSION: FIB_SESSION_COOKIE
}

with open("ofertas.txt", "w", encoding="utf-8") as file:

    for page in range(0, 8):

        url = f"{base_url}page={page}"

        response = requests.get(
            url,
            headers=headers,
            cookies=cookies,
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Todas las filas de la tabla
        rows = soup.select("table.views-view-table tbody tr")

        print(f"Página {page}: {len(rows)} ofertas")

        for row in rows:

            practice = row.select_one(".views-field-name a")
            company = row.select_one(".views-field-employer-alias a")

            if practice and company:

                practice_text = practice.get_text(" ", strip=True)
                company_text = company.get_text(" ", strip=True)

                file.write(f"Práctica: {practice_text}\n")
                file.write(f"Empresa: {company_text}\n\n")

print("Terminado")