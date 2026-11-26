from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

from services.llm import call_llm
from services.reseach_schema import ResearchOutput
from services.search_tool import search_web, search_market_data

BASE_DIR = Path(__file__).resolve().parent
RESEARCH_SKILL = (BASE_DIR / "skills/financial-market/research.md").read_text(encoding="utf-8")
REPORT_SKILL = (BASE_DIR / "skills/financial-market/report.md").read_text(encoding="utf-8")

INITIAL_PROMPT = """
Start today's financial markets research.
Current date and time: {current_datetime}

{today_market_data}

Identify the most important recent market developments
and determine what information needs to be investigated.
"""

LOOP_PROMPT = """
Continue the financial markets research.
Current date and time: {current_datetime}

Here are the results from your previous search requests:

{search_results}

Keep all previously verified findings, market_data, and upcoming_events from earlier rounds,
and merge the new verified evidence above into them. Review remaining information gaps,
and decide whether to request more searches ('search') or finish the research ('finish').
"""

FINISH_PROMPT = """
Generate today's financial markets report using the
research collected during this investigation.
Current date and time: {current_datetime}

Research findings:
{research_results}
"""

def run_research (max_round: int) -> ResearchOutput:
    print("Starting research")
    market_data = search_market_data()
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M')
    prompt = INITIAL_PROMPT.format(
        current_datetime=now,
        today_market_data=market_data
        )
    previous_interaction_id = None
    seen_urls = set()
    
    for round in range(1, max_round+1):
        print(f"Round {round} for research")
        
        raw_json, previous_interaction_id = call_llm(
            prompt, RESEARCH_SKILL, ResearchOutput, previous_interaction_id
        )
        
        research = ResearchOutput.model_validate_json(raw_json)
        
        if research.action == "finish" or round == max_round:
            print("research done")
            return research
        
        search_results = []
        
        for query in research.queries[:5]:
            print(f"Search quert: {query}")
            result = search_web(query=query, seen_urls=seen_urls)
            search_results.append(result)
            
        prompt = LOOP_PROMPT.format(
            current_datetime=now,
            search_results="\n\n".join(search_results)
        )
    
    raise RuntimeError("Research went wrong, nothing back")
          
        

def generate_report (reseach_data: ResearchOutput) -> str:
    print("Building the report")
    
    now = datetime.now().strftime('%Y-%m-%d_%H-%M')
    prompt = FINISH_PROMPT.format(
        current_datetime=now,
        research_results=reseach_data.model_dump_json(indent=2)
    )
    
    report_md, _ = call_llm(
        prompt, REPORT_SKILL
    )
    
    return report_md

    
    
def main():
    research_data = run_research(max_round=6)
    report = generate_report(research_data)
    
    reports_dir = BASE_DIR / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    filename = f"report_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.md"
    output_path = reports_dir / filename
    
    output_path.write_text(report, encoding="utf-8")
    
    print(f"Report of today done!: {filename}")
    
if __name__ == "__main__":
    main()