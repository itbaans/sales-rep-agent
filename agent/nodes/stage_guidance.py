import json
from agent.services.llm_service import get_llm
from agent.state import ConversationState
from agent.prompts import get_stage_guidance_prompt

def stage_guidance_node(state: ConversationState) -> ConversationState:
    print("---NODE: STAGE_GUIDANCE---")

    llm = get_llm()

    prompt = get_stage_guidance_prompt(state)

    response_str = llm.invoke(prompt).content
    
    try:
        parsed = json.loads(response_str)
    except:
        # fallback: retry or sanitize
        parsed = {"stage_guidance": response_str, "lead_qualification_score": {}, "detected_objections": [], "buying_signals_detected": []}

    state['stage_guidance'] = parsed.get('stage_guidance', "")
    state['lead_qualification_score'] = parsed.get('lead_qualification_score', {})
    state['detected_objections'] = parsed.get('detected_objections', [])
    state['buying_signals_detected'] = parsed.get('buying_signals_detected', [])

    return state