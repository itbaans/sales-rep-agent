"""
LLM-Automated Conversation Testing
- Lead LLM simulates realistic prospect behavior
- Evaluator LLM assesses agent performance
"""

from agent.AgentAPI import get_agent_api
from agent.services.llm_service import get_llm
import json
import time
from typing import Dict, List, Any

class LLMLeadSimulator:
    """LLM that acts as a realistic lead"""
    
    def __init__(self, lead_persona: Dict[str, Any]):
        self.persona = lead_persona
        self.llm = get_llm(model_name="gemini-2.0-flash-lite")
        self.conversation_history = []
    
    def get_lead_prompt(self, agent_message: str) -> str:
        history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.conversation_history])
        
        return f"""You are roleplaying as a B2B lead/prospect with the following profile:

**YOUR PERSONA:**
- Name: {self.persona['name']}
- Company: {self.persona['company']}
- Role: {self.persona['role']}
- Industry: {self.persona['industry']}
- Personality: {self.persona['personality']}
- Pain Points: {', '.join(self.persona['pain_points'])}
- Budget Range: {self.persona['budget_range']}
- Timeline: {self.persona['timeline']}
- Authority Level: {self.persona['authority_level']}
- Current Situation: {self.persona['situation']}

**BEHAVIORAL GUIDELINES:**
{self.persona['behavioral_notes']}

**CONVERSATION HISTORY:**
{history}

**LATEST AGENT MESSAGE:**
{agent_message}

**YOUR TASK:**
Respond as this lead would realistically respond. Stay in character. Be natural and conversational. 
- Ask follow-up questions based on your persona's concerns
- Reveal information gradually based on trust level
- Show skepticism or enthusiasm as appropriate
- End conversation naturally when it makes sense

**RESPONSE (keep under 100 words):**"""

    def respond(self, agent_message: str) -> str:
        self.conversation_history.append({"role": "agent", "content": agent_message})
        
        prompt = self.get_lead_prompt(agent_message)
        response = self.llm.invoke(prompt).content.strip()
        
        self.conversation_history.append({"role": "lead", "content": response})
        return response

class LLMConversationEvaluator:
    """LLM that evaluates agent performance"""
    
    def __init__(self):
        self.llm = get_llm()
    
    def evaluate_conversation(self, lead_persona: Dict, conversation_log: List, agent_state: Dict) -> Dict:
        conversation_text = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in conversation_log])
        
        eval_prompt = f"""You are an expert sales coach evaluating an AI sales agent's performance in a B2B conversation.

**LEAD PROFILE:**
- Role: {lead_persona['role']} at {lead_persona['company']}
- Industry: {lead_persona['industry']}
- Authority: {lead_persona['authority_level']}
- Pain Points: {', '.join(lead_persona['pain_points'])}
- Expected Behavior: {lead_persona['behavioral_notes']}

**CONVERSATION TRANSCRIPT:**
{conversation_text}

**AGENT'S FINAL STATE:**
- Conversation Stage: {agent_state.get('conversation_stage', 'unknown')}
- Lead Qualification Scores: {agent_state.get('lead_qualification_score', {})}
- Buying Signals Detected: {agent_state.get('buying_signals_detected', [])}
- Objections Detected: {agent_state.get('detected_objections', [])}
- Documents Retrieved: {len(agent_state.get('retrieved_docs', []))}

**EVALUATE THE AGENT ON:**

1. **Rapport Building (1-10):** Did agent establish good connection?
2. **Discovery Skills (1-10):** How well did agent uncover needs/pain points?
3. **Knowledge Application (1-10):** Did agent use relevant company knowledge effectively?
4. **Objection Handling (1-10):** How well were concerns addressed?
5. **Qualification Accuracy (1-10):** Are the qualification scores realistic?
6. **Stage Management (1-10):** Was conversation stage progression appropriate?
7. **Natural Flow (1-10):** Did conversation feel natural vs robotic?
8. **Value Communication (1-10):** How well did agent communicate value?

**PROVIDE EVALUATION AS JSON:**
{{
  "scores": {{
    "rapport_building": X,
    "discovery_skills": X,
    "knowledge_application": X,
    "objection_handling": X,
    "qualification_accuracy": X,
    "stage_management": X,
    "natural_flow": X,
    "value_communication": X
  }},
  "overall_score": X,
  "strengths": ["strength1", "strength2"],
  "weaknesses": ["weakness1", "weakness2"],
  "missed_opportunities": ["opportunity1", "opportunity2"],
  "realistic_outcome": "Would this lead likely move forward? Why?",
  "improvement_suggestions": ["suggestion1", "suggestion2"]
}}"""

        try:
            response = self.llm.invoke(eval_prompt).content
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
        except Exception as e:
            print(f"Evaluation parsing error: {e}")
        
        return {"error": "Failed to parse evaluation"}

class AutomatedTestCase:
    """Complete automated test case with LLM lead and evaluator"""
    
    def __init__(self, name: str, lead_persona: Dict[str, Any], max_turns: int = 10):
        self.name = name
        self.lead_persona = lead_persona
        self.max_turns = max_turns
        self.lead_simulator = LLMLeadSimulator(lead_persona)
        self.evaluator = LLMConversationEvaluator()
    
    def run_test(self) -> Dict[str, Any]:
        print(f"\n{'='*60}")
        print(f"RUNNING AUTOMATED TEST: {self.name}")
        print(f"Lead: {self.lead_persona['name']} ({self.lead_persona['role']})")
        print(f"{'='*60}")
        
        # Initialize agent
        lead_id = f"auto_test_{self.name.lower().replace(' ', '_')}"
        agent_api = get_agent_api(lead_id)
        
        # Get opening statement
        agent_opening = agent_api.get_opening_statement(lead_id)
        print(f"AGENT: {agent_opening}")
        
        conversation_log = [{"role": "agent", "content": agent_opening}]
        
        # Run conversation
        for turn in range(self.max_turns):
            # Lead responds
            lead_response = self.lead_simulator.respond(agent_opening if turn == 0 else agent_response)
            print(f"\nLEAD: {lead_response}")
            conversation_log.append({"role": "lead", "content": lead_response})
            
            # Check for conversation end signals
            if any(phrase in lead_response.lower() for phrase in ["goodbye", "thanks for your time", "not interested", "end call"]):
                print("\n[Lead ended conversation]")
                break
            
            # Agent responds
            try:
                agent_response = agent_api.process_message(lead_id, lead_response)
                print(f"AGENT: {agent_response}")
                conversation_log.append({"role": "agent", "content": agent_response})
                
                # Check if agent ended conversation
                if agent_api.state.get('is_end', False):
                    print("\n[Agent ended conversation]")
                    break
                    
            except Exception as e:
                print(f"ERROR: {e}")
                break
        
        # Evaluate conversation
        print(f"\n{'='*40}")
        print("EVALUATING CONVERSATION...")
        print(f"{'='*40}")
        
        evaluation = self.evaluator.evaluate_conversation(
            self.lead_persona, 
            conversation_log, 
            agent_api.state
        )
        
        if "error" not in evaluation:
            print(f"\nOVERALL SCORE: {evaluation['overall_score']}/10")
            print(f"STRENGTHS: {', '.join(evaluation['strengths'])}")
            print(f"WEAKNESSES: {', '.join(evaluation['weaknesses'])}")
            print(f"OUTCOME: {evaluation['realistic_outcome']}")
        
        return {
            "test_name": self.name,
            "conversation_log": conversation_log,
            "agent_final_state": agent_api.state,
            "evaluation": evaluation
        }

# Test persona definitions
TEST_PERSONAS = {
    "eager_startup_cto": {
        "name": "Alex Chen",
        "company": "TechStart AI",
        "role": "CTO",
        "industry": "AI/ML Startup",
        "personality": "Enthusiastic but budget-conscious",
        "pain_points": ["scaling infrastructure", "need ML expertise", "tight deadlines"],
        "budget_range": "$100K-300K",
        "timeline": "3-6 months",
        "authority_level": "High (technical decisions)",
        "situation": "Series A funded, building MVP, needs technical partner",
        "behavioral_notes": "Ask lots of technical questions, mention budget constraints, show urgency but need proof of expertise. Reference competitors casually."
    },
    
    "skeptical_bank_executive": {
        "name": "Margaret Thompson",
        "company": "Regional Community Bank",
        "role": "SVP Operations",
        "industry": "Regional Banking",
        "personality": "Cautious, risk-averse, data-driven",
        "pain_points": ["regulatory compliance", "legacy system modernization", "cost control"],
        "budget_range": "$1M-5M",
        "timeline": "12-18 months",
        "authority_level": "High (budget approval)",
        "situation": "Pressured by board to modernize, but burned by previous vendor",
        "behavioral_notes": "Ask for references, challenge ROI claims, mention compliance requirements, express concern about implementation risks. Need lots of proof."
    },
    
    "overwhelmed_hospital_admin": {
        "name": "Dr. Sarah Rodriguez",
        "company": "Metro General Hospital",
        "role": "VP of Operations",
        "industry": "Healthcare",
        "personality": "Busy, stressed, needs simple solutions",
        "pain_points": ["staff efficiency", "patient flow", "cost reduction", "compliance"],
        "budget_range": "$500K-1M",
        "timeline": "ASAP",
        "authority_level": "Medium (needs board approval)",
        "situation": "Post-COVID recovery, understaffed, looking for tech solutions",
        "behavioral_notes": "Mention time constraints, ask about ease of implementation, concerned about staff training, need quick wins."
    },
    
    "comparison_shopping_manufacturer": {
        "name": "James Wilson",
        "company": "MidSize Manufacturing",
        "role": "IT Director", 
        "industry": "Manufacturing",
        "personality": "Methodical, thorough, price-sensitive",
        "pain_points": ["ERP modernization", "supply chain visibility", "integration challenges"],
        "budget_range": "$750K-2M",
        "timeline": "6-12 months",
        "authority_level": "Medium (influences decision)",
        "situation": "Evaluating 4 vendors, detailed comparison process",
        "behavioral_notes": "Ask same questions to all vendors, request detailed proposals, mention competitors by name, focus on specific requirements."
    },
    
    "tire_kicker_consultant": {
        "name": "Mike Davis",
        "company": "Small Business Consulting",
        "role": "Principal",
        "industry": "Consulting",
        "personality": "Curious but non-committal",
        "pain_points": ["client delivery", "scaling capabilities"],
        "budget_range": "$50K-100K",
        "timeline": "Someday",
        "authority_level": "High (but no real project)",
        "situation": "Fishing for information, no immediate need",
        "behavioral_notes": "Ask general questions, avoid specifics about budget/timeline, mention 'exploring options', show mild interest but no urgency."
    }
}

def create_test_cases():
    """Create automated test cases from personas"""
    return [
        AutomatedTestCase("Eager Startup CTO", TEST_PERSONAS["eager_startup_cto"], max_turns=8),
        AutomatedTestCase("Skeptical Bank Executive", TEST_PERSONAS["skeptical_bank_executive"], max_turns=10),
        AutomatedTestCase("Overwhelmed Hospital Admin", TEST_PERSONAS["overwhelmed_hospital_admin"], max_turns=6),
        AutomatedTestCase("Comparison Shopping Manufacturer", TEST_PERSONAS["comparison_shopping_manufacturer"], max_turns=12),
        AutomatedTestCase("Tire Kicker Consultant", TEST_PERSONAS["tire_kicker_consultant"], max_turns=8)
    ]

def run_automated_tests():
    """Run all automated test cases"""
    print("Starting LLM-Automated Test Suite")
    
    # Initialize knowledge bases once
    temp_agent = get_agent_api("temp_init")
    temp_agent.initialize_knowledge()
    
    test_cases = create_test_cases()
    results = []
    
    for test_case in test_cases:
        try:
            result = test_case.run_test()
            results.append(result)
            time.sleep(2)  # Brief pause between tests
        except Exception as e:
            print(f"ERROR in {test_case.name}: {e}")
            results.append({"test_name": test_case.name, "error": str(e)})
    
    # Summary report
    print(f"\n{'='*60}")
    print("AUTOMATED TEST SUMMARY")
    print(f"{'='*60}")
    
    for result in results:
        if "error" in result:
            print(f"❌ {result['test_name']}: ERROR")
        elif "evaluation" in result and "overall_score" in result["evaluation"]:
            score = result["evaluation"]["overall_score"]
            status = "✅" if score >= 7 else "⚠️" if score >= 5 else "❌"
            print(f"{status} {result['test_name']}: {score}/10")
        else:
            print(f"⚠️ {result['test_name']}: Evaluation failed")
    
    return results

def run_single_automated_test(persona_name: str):
    """Run single automated test"""
    if persona_name not in TEST_PERSONAS:
        print(f"Persona '{persona_name}' not found. Available: {list(TEST_PERSONAS.keys())}")
        return
    
    # Initialize knowledge
    temp_agent = get_agent_api("temp_init")
    temp_agent.initialize_knowledge()
    
    test_case = AutomatedTestCase(f"Test {persona_name}", TEST_PERSONAS[persona_name])
    return test_case.run_test()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        run_single_automated_test(sys.argv[1])
    else:
        run_automated_tests()