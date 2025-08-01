from agent.state import ConversationState
from agent.services.llm_service import get_llm
from agent.prompts import get_system_persona

def generate_opening_statement(state: ConversationState) -> ConversationState:
    """
    Generates the agent's opening message by inspecting lead data, company data,
    and any long-term memory. Invokes Gemini LLM to decide tone and content
    for either initial outreach or a follow-up.
    """
    print("---NODE: GENERATE_OPENING_STATEMENT---")

    # Retrieve data from state
    lead = state.get('lead_data', {})
    memory = state.get('long_term_memory', {})
    company = state.get('company_data', {})

    # Construct a clear instruction for the LLM
    base_instruction = (
        "Using the provided data, craft an opening statement. "
        "Decide if it's an initial outreach or follow-up, reference past interaction if any. "
        "Important: respond ONLY with the opening statement itself—do NOT include any lead-in text such as 'Okay, here's...' or additional commentary."
    )

    # Assemble context sections
    company_section = f"## COMPANY DATA ##\n{company!r}"
    lead_section = f"## LEAD DATA ##\n{lead!r}"
    memory_section = f"## PAST MEMORY ##\n{memory!r}" if memory else "## PAST MEMORY ##\nNone"

    # Build message list for Gemini LLM
    prompt = [
        f"##SYSTEM: {get_system_persona()}",
        f"{base_instruction}\n{company_section}\n{lead_section}\n{memory_section}"
    ]

    # Initialize and invoke Gemini
    llm = get_llm()
    response = llm.invoke(prompt).content

    # Safely extract generated text
    try:
        llm_output = response.generations[0][0].text.strip()
    except Exception:
        llm_output = str(response)

    # Append the LLM's reply to conversation history
    state.setdefault('messages', []).append({
        'role': 'agent',
        'content': llm_output
    })

    print(f"\nAgent: {llm_output}\n")
    return state


def process_user_input(state: ConversationState) -> ConversationState:

    user_input = input("Your response: ")
    state['user_input'] = user_input
    state['messages'].append({"role": "user", "content": user_input})
    return state

