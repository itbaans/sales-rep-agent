import datetime
import json

from agent.prompts import get_ops_agent_prompt
from agent.services.llm_service import get_llm

# --- OPs agent's Tools Implementations ---

def schedule_meeting(attendees: list[str], duration_minutes: int, topic: str, time_preference: str) -> dict:

    if not all([attendees, duration_minutes, topic, time_preference]):
        return {
            "status": "error",
            "message": "Missing one or more required parameters: attendees, duration_minutes, topic, time_preference."
        }

    print("---")
    print(f"[ACTION LOG] Executing schedule_meeting:")
    print(f"  - Topic: {topic}")
    print(f"  - Duration: {duration_minutes} minutes")
    print(f"  - Attendees: {', '.join(attendees)}")
    print(f"  - Time Preference: {time_preference}")
    print("  - SIMULATION: Successfully created calendar event and sent invites.")
    print("---\n")

    return {
        "status": "success",
        "message": f"A {duration_minutes}-minute meeting about '{topic}' has been successfully scheduled with {', '.join(attendees)}."
    }

def send_email(recipient_email: str, subject: str, body: str) -> dict:

    if not all([recipient_email, subject, body]):
        return {
            "status": "error",
            "message": "Missing one or more required parameters: recipient_email, subject, body."
        }

    print("---")
    print(f"[ACTION LOG] Executing send_email:")
    print(f"  - To: {recipient_email}")
    print(f"  - Subject: {subject}")
    print(f"  - Body:\n---\n{body}\n---")
    print("  - SIMULATION: Email has been successfully queued for sending.")
    print("---\n")

    return {
        "status": "success",
        "message": f"Email with subject '{subject}' has been sent to {recipient_email}."
    }

def web_search(query: str) -> dict:

    if not query:
        return {"status": "error", "message": "Query parameter cannot be empty."}

    print("---")
    print(f"[ACTION LOG] Executing web_search:")
    print(f"  - Query: '{query}'")
    print("  - SIMULATION: Executing web search and finding top 3 results.")
    print("---\n")

    # In a real scenario, you would return actual search results.
    # For now, we return a summary string.
    return {
        "status": "success",
        "message": f"Web search completed for '{query}'.",
        "result": f"Placeholder result: Research on '{query}' shows it is a key industry trend with major players like TechCorp and Innovate Inc. leading the market."
    }

def create_document(document_type: str, content: str) -> dict:

    if not all([document_type, content]):
        return {
            "status": "error",
            "message": "Missing one or more required parameters: document_type, content."
        }
        
    filename = f"{document_type}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    print("---")
    print(f"[ACTION LOG] Executing create_document:")
    print(f"  - Document Type: {document_type}")
    print(f"  - Filename: {filename}")
    print(f"  - Content Preview: '{content[:100]}...'")
    print(f"  - SIMULATION: Document '{filename}' has been created and saved to the system.")
    print("---\n")

    return {
        "status": "success",
        "message": f"Document '{filename}' of type '{document_type}' has been successfully created."
    }

def report_task_unactionable(reason):
    return{
        "status": "not actionable",
        "message": {reason}
    }

OPS_AGENT_TOOLS = {
    "schedule_meeting": schedule_meeting,
    "send_email": send_email,
    "web_search": web_search,
    "create_document": create_document,
    "report_task_unactionable": report_task_unactionable,
    # The 'clarify_and_request_info' tool would be added here when implemented.
}

def delegate_to_ops_agent(task_description: str) -> dict:

    print("---")
    print(f"[DELEGATION LOG] Sales Agent initiated delegation.")
    print(f"  - Task: '{task_description}'")

    # 1. Generate the specific prompt for the OpsAgent
    ops_agent_prompt = get_ops_agent_prompt(delegated_task=task_description)

    # 2. Invoke the LLM with the OpsAgent prompt
    print("[DELEGATION LOG] Invoking LLM for OpsAgent decision...")
    try:
        llm = get_llm(model_name="gemini-2.0-flash-lite")
        # In a real application, consider adding a timeout.
        llm_response_str = llm.invoke(ops_agent_prompt).content
    except Exception as e:
        error_message = f"LLM invocation failed for OpsAgent. Error: {e}"
        print(f"[DELEGATION ERROR] {error_message}")
        return {"status": "error", "message": error_message}
        
    print(f"[DELEGATION LOG] OpsAgent raw response received: {llm_response_str}")

    # 3. Parse the LLM's JSON response robustly
    try:
        # LLMs sometimes wrap their JSON in markdown code blocks. This removes them.
        if llm_response_str.strip().startswith("```json"):
            clean_json_str = llm_response_str.strip()[7:-3].strip()
        else:
            clean_json_str = llm_response_str.strip()
        
        parsed_action = json.loads(clean_json_str)
        thought = parsed_action.get("thought", "No thought provided.")
        action = parsed_action.get("action")

        if not action or not isinstance(action, dict):
             raise ValueError("Parsed JSON is missing a valid 'action' object.")

        print(f"[DELEGATION LOG] OpsAgent Thought: {thought}")

    except (json.JSONDecodeError, AttributeError, ValueError) as e:
        error_message = f"Failed to decode or validate OpsAgent's JSON response. Error: {e}. Raw response: '{llm_response_str}'"
        print(f"[DELEGATION ERROR] {error_message}")
        return {"status": "error", "message": error_message, "details": "The OpsAgent returned a malformed response."}

    # 4. Extract tool name and parameters
    tool_name = action.get("tool")
    tool_params = {k: v for k, v in action.items() if k != 'tool'}

    # 5. Execute the chosen tool
    if tool_name in OPS_AGENT_TOOLS:
        print(f"[DELEGATION LOG] OpsAgent chose tool: '{tool_name}' with params: {tool_params}")
        selected_tool_func = OPS_AGENT_TOOLS[tool_name]
        try:
            # Execute the function and return its result directly
            execution_result = selected_tool_func(**tool_params)
            print("---")
            return execution_result
        except TypeError as e:
            # This error is crucial: it means the LLM hallucinated parameters that the function doesn't accept.
            error_message = f"Error calling tool '{tool_name}': Mismatched or invalid parameters provided by LLM. Error: {e}"
            print(f"[DELEGATION ERROR] {error_message}")
            return {"status": "error", "message": error_message}
    else:
        error_message = f"OpsAgent selected an unknown or unsupported tool: '{tool_name}'"
        print(f"[DELEGATION ERROR] {error_message}")
        return {"status": "error", "message": error_message}
    