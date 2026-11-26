from typing import Literal
from pydantic import BaseModel, Field


class Evidence(BaseModel):
    id: str = Field(description="Identificador único corto, ej: 'ev_1', 'ev_2'")
    title: str = Field(description="Titular de la noticia o fuente")
    url: str = Field(description="URL exacta devuelta por la búsqueda")
    published_date: str | None = Field(default=None, description="Fecha de publicación si aparece")
    snippet: str = Field(description="Dato o fragmento clave extraído de la fuente")


class Finding(BaseModel):
    claim: str = Field(description="Afirmación factual concreta sobre el mercado")
    evidence_ids: list[str] = Field(
        default_factory=list,
        description="Lista de IDs de Evidence que respaldan o contradicen esta afirmación, ej: ['ev_1']"
    )
    status: Literal["supported", "contradicted", "unsupported"] = Field(
        description="supported si la evidencia lo confirma; contradicted si hay fuentes opuestas; unsupported si falta respaldo"
    )


class MarketData(BaseModel):
    asset: str = Field(description="Nombre o ticker del activo, ej: 'S&P 500', 'NVDA', 'EUR/USD'")
    value: str = Field(description="Precio o nivel actual encontrado, ej: '5,980.50'")
    change: str | None = Field(default=None, description="Variación porcentual o en puntos, ej: '-0.85%'")
    as_of: str | None = Field(default=None, description="Fecha u hora del dato")
    evidence_id: str | None = Field(default=None, description="ID de la Evidence de donde salió este dato")


class UpcomingEvent(BaseModel):
    date: str = Field(description="Fecha del evento, ej: '2026-11-27'")
    event: str = Field(description="Descripción del evento macro o empresarial")
    expected_impact: str | None = Field(default=None, description="Por qué es relevante para el mercado")


class ResearchOutput(BaseModel):
    action: Literal["search", "finish"] = Field(
        description="'search' si faltan datos importantes; 'finish' si ya hay suficiente evidencia para el reporte"
    )
    queries: list[str] = Field(
        default_factory=list,
        description="Lista de 2 a 4 búsquedas concretas si action='search'. Vacía si action='finish'."
    )
    evidences: list[Evidence] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
    market_data: list[MarketData] = Field(default_factory=list)
    upcoming_events: list[UpcomingEvent] = Field(default_factory=list)
    research_summary: str | None = Field(
        default=None,
        description="Síntesis ejecutiva completa cuando action='finish'"
    )