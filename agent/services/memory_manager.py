import json
from pathlib import Path

MEMORY_FILE = Path("data/long_term_memory.json")

def load_memory(lead_id: str) -> dict:
    """Loads long-term memory for a specific lead."""
    if not MEMORY_FILE.exists():
        return {}
    with open(MEMORY_FILE, 'r') as f:
        all_memory = json.load(f)
    return all_memory.get(lead_id, {})

def save_memory(lead_id: str, new_summary: str, insights: dict):
    """Saves updated long-term memory for a lead."""
    all_memory = {}
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, 'r') as f:
            all_memory = json.load(f)
            
    # Update the lead's memory (this could be more sophisticated)
    lead_memory = all_memory.get(lead_id, {})
    lead_memory['last_interaction_summary'] = new_summary
    # In a real app, you would merge insights, not just overwrite
    lead_memory.update(insights) 
    
    all_memory[lead_id] = lead_memory
    
    with open(MEMORY_FILE, 'w') as f:
        json.dump(all_memory, f, indent=2)
    print(f"---SERVICE: Long-term memory saved for {lead_id}---")