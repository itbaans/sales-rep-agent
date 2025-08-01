import json
from pathlib import Path

MEMORY_FILE = Path("data/long_term_memory.json")

def save_memory(lead_id: str, detailed_memory: dict, summary: str):

    all_memory = {}
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, 'r') as f:
                content = f.read()
                if content:
                    all_memory = json.loads(content)
        except json.JSONDecodeError:
            all_memory = {}

    # The new memory object now has a dedicated key for the summary.
    all_memory[lead_id] = {
        "summary": summary,
        "detailed_memory": detailed_memory
    }
    
    with open(MEMORY_FILE, 'w') as f:
        json.dump(all_memory, f, indent=2)
        
    print(f"---SERVICE: Long-term memory with in-context summary saved for {lead_id}---")

# The load_memory function does not need to be changed. It already loads the full object.

def load_memory(lead_id: str) -> dict:
    if not MEMORY_FILE.exists():
        return {}
    try:
        with open(MEMORY_FILE, 'r') as f:
            content = f.read()
            if not content:
                return {}
            all_memory = json.loads(content)
        # Return the entire object stored under the lead's ID, or an empty dict if not found.
        return all_memory.get(lead_id, {})
    except (json.JSONDecodeError, FileNotFoundError):
        return {}