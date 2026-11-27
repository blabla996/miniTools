from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

from services.llm import call_llm
from services.reseach_schema import ResearchOutput, ResearchStep
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

Review remaining information gaps across US markets, macro/central banks, tech/AI, China, and Europe,
and decide whether to request more searches ('search') or conclude data gathering ('finish').
"""

CONSOLIDATE_PROMPT = """
The search phase is complete.
Current date and time: {current_datetime}

Consolidate all verified information gathered across <yahoo_market_data> and all <external_search_data>
results from previous rounds into the final structured ResearchOutput JSON (evidences, findings,
key market_data, upcoming_events, and research_summary).
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
    now = datetime.now().strftime('%Y-%m-%d_%H-%M')
    prompt = INITIAL_PROMPT.format(
        current_datetime=now,
        today_market_data=market_data
        )
    previous_interaction_id = None
    seen_urls = set()
    
    for round in range(1, max_round+1):
        print(f"Round {round} for research")
        
        raw_json, previous_interaction_id = call_llm(
            prompt, RESEARCH_SKILL, "medium", ResearchStep, previous_interaction_id
        )
        
        researchStep = ResearchStep.model_validate_json(raw_json)
        
        if researchStep.action == "finish" or round == max_round:
            print("research done")
            break
        
        search_results = []
        
        for query in researchStep.queries[:5]:
            print(f"Search query: {query}")
            result = search_web(query=query, seen_urls=seen_urls)
            search_results.append(result)
        
        if not search_results:
            search_results.append(
                "No search queries were provided in the previous step. "
                "If you need more data, provide 1–3 specific queries; otherwise, set action='finish'."
            )
            
        prompt = LOOP_PROMPT.format(
            current_datetime=now,
            search_results="\n\n".join(search_results)
        )
    
    print("Consolidating research output...")
    prompt = CONSOLIDATE_PROMPT.format(current_datetime=now)
                
    raw_json, previous_interaction_id = call_llm(
        prompt, RESEARCH_SKILL, "xhigh", ResearchOutput, previous_interaction_id
    )
            
    research = ResearchOutput.model_validate_json(raw_json)
    return research
          
        

def generate_report (reseach_data: ResearchOutput) -> str:
    print("Building the report")
    
    now = datetime.now().strftime('%Y-%m-%d_%H-%M')
    prompt = FINISH_PROMPT.format(
        current_datetime=now,
        research_results=reseach_data.model_dump_json(indent=2)
    )
    
    report_md, _ = call_llm(
        prompt, REPORT_SKILL, "high"
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