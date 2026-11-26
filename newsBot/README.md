# NewsBot

NewsBot genera un informe diario en español sobre mercados financieros. Combina cotizaciones de Yahoo Finance mediante `yfinance`, búsqueda de noticias con Tavily e investigación y redacción con Google Gemini. Está pensado como herramienta personal e informativa; no ofrece recomendaciones de compra o venta.

## Requisitos

- Python 3
- Claves de API para Google Gemini y Tavily

## Instalación

Desde la carpeta del proyecto:

```bash
cd newsBot
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

En Windows PowerShell, activa el entorno con:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Configuración

Crea un archivo `.env` en la carpeta `newsBot` con tus propias claves:

```dotenv
GEMINI_API_KEY=tu_clave_de_gemini
TAVILY_API_KEY=tu_clave_de_tavily
```

No compartas ni subas `.env` a GitHub. El repositorio ignora ese archivo; usa claves propias y mantenlas privadas.

## Ejecución

Con el entorno virtual activado y `.env` configurado:

```bash
python main.py
```

El programa consulta datos de mercado, realiza hasta seis rondas de investigación y guarda el informe en `newsBot/reports/`. Las llamadas a proveedores externos pueden estar sujetas a cuotas o costes según sus cuentas y planes.

## Personalización del modelo y nivel de razonamiento

Puedes cambiar el modelo de Gemini y el nivel de razonamiento (`thinking_level`) en `services/llm.py`. Usa un modelo y un nivel admitidos por tu cuenta y por la versión del SDK instalada. Por ejemplo:

```python
config = {
    "model": "gemini-4-hydrogen",
    "input": prompt,
    "system_instruction": skill,
    "generation_config": {
        "thinking_level": "xhigh",
    }
}
```

## Fuentes y limitaciones

Las cotizaciones se obtienen mediante `yfinance` desde Yahoo Finance y las noticias mediante Tavily. La disponibilidad, puntualidad y exactitud de fuentes externas pueden variar. El informe es informativo y educativo; verifica los datos importantes con sus fuentes originales y no lo uses como asesoramiento financiero.
