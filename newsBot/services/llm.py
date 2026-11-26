from google import genai
import time

# conection
client = genai.Client()

def call_llm(prompt: str, skill:str ,schema=None, previous_interaction_id: str | None = None) -> tuple[str, str]:
    
    config = {
        "model": "gemini-3.8-flash",
        "input": prompt,
        "system_instruction": skill,
        "generation_config": {
            "thinking_level": "low"
        }
    }
    
    if previous_interaction_id:
        config["previous_interaction_id"] = previous_interaction_id
        
    if schema:
        config["response_format"] = {
        "type": "text",
        "mime_type": "application/json",
        "schema": schema.model_json_schema()
    }

    max_retries = 3
    for attempt in range (1, max_retries+1):
        try:
            interaction = client.interactions.create(**config, timeout=120.0)
            break
        except Exception as e:
            if getattr(e, "status_code", None) in (429, 503) and attempt < max_retries:
                wait_seconds = 5 * (2 ** (attempt - 1))  # 5s, 10s, 20s
                print(f"[WARN] API ocupada ({e.code}). Reintentando en {wait_seconds}s (intento {attempt}/{max_retries})...")
                time.sleep(wait_seconds)
            else:
                raise
    
    if not interaction.output_text:
        raise RuntimeError(f"Gemini no answer. Status: {interaction.status}")
    
    # .output_text ya filtra el pensamiento y devuelve solo el str final
    return interaction.output_text, interaction.id
