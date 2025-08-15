"""
Conversation Test Cases for Sales Agent System
Run these to validate agent behavior across different scenarios
"""

from agent.AgentAPI import get_agent_api
import json
import time

class ConversationTestCase:
    def __init__(self, name, description, lead_profile, conversation_flow, expected_behaviors):
        self.name = name
        self.description = description
        self.lead_profile = lead_profile
        self.conversation_flow = conversation_flow
        self.expected_behaviors = expected_behaviors
        self.results = {}

    def run_test(self, agent_api):
        """Run the conversation test case"""
        print(f"\n{'='*60}")
        print(f"RUNNING TEST: {self.name}")
        print(f"Description: {self.description}")
        print(f"{'='*60}")
        
        # Get opening statement
        opening = agent_api.get_opening_statement(self.lead_profile['lead_id'])
        print(f"Agent Opening: {opening}")
        
        conversation_log = [{"role": "agent", "content": opening}]
        
        # Run conversation flow
        for i, user_message in enumerate(self.conversation_flow):
            print(f"\nTurn {i+1}")
            print(f"User: {user_message}")
            
            try:
                response = agent_api.process_message(self.lead_profile['lead_id'], user_message)
                print(f"Agent: {response}")
                conversation_log.append({"role": "user", "content": user_message})
                conversation_log.append({"role": "agent", "content": response})
                
                # Check if conversation ended
                if agent_api.state.get('is_end', False):
                    print("\n[Conversation ended by agent]")
                    break
                    
            except Exception as e:
                print(f"ERROR: {e}")
                break
        
        # Analyze results
        self.analyze_conversation(agent_api.state, conversation_log)
        return self.results

    def analyze_conversation(self, final_state, conversation_log):
        """Analyze conversation against expected behaviors"""
        self.results = {
            'final_state': final_state,
            'conversation_log': conversation_log,
            'analysis': {},
            'passed_checks': [],
            'failed_checks': []
        }
        
        # Check expected behaviors
        for check_name, check_func in self.expected_behaviors.items():
            try:
                if check_func(final_state, conversation_log):
                    self.results['passed_checks'].append(check_name)
                    print(f"✓ PASSED: {check_name}")
                else:
                    self.results['failed_checks'].append(check_name)
                    print(f"✗ FAILED: {check_name}")
            except Exception as e:
                self.results['failed_checks'].append(f"{check_name} (ERROR: {e})")
                print(f"✗ ERROR in {check_name}: {e}")

# Define test cases

TEST_CASES = {
    "interested_technical_lead": ConversationTestCase(
        name="Interested Technical Lead",
        description="Technical decision maker showing clear interest and buying signals",
        lead_profile={
            "lead_id": "test_tech_lead_001",
            "name": "Sarah Chen", 
            "company": "MedTech Solutions",
            "role": "CTO"
        },
        conversation_flow=[
            "Hi, I'm looking for a partner to help us integrate AI into our patient management system. What experience do you have with healthcare AI?",
            "That sounds interesting. Can you tell me more about the Hami project? What was the tech stack and how long did implementation take?",
            "We have a budget of around $500K for this project. What kind of timeline are we looking at?",
            "Great, can we schedule a demo next week?",
            "Alright great Bye"
        ],
        expected_behaviors={
            "searches_healthcare_ai": lambda state, log: any("hami" in msg['content'].lower() for msg in log if msg['role'] == 'agent'),
            "detects_budget_signal": lambda state, log: state.get('buying_signals_detected') and any("budget" in signal.lower() for signal in state['buying_signals_detected']),
            "progresses_to_interest_stage": lambda state, log: state.get('conversation_stage') in ['interest', 'closing'],
            "high_engagement_score": lambda state, log: state.get('lead_qualification_score', {}).get('engagement_level', 0) >= 7,
            "mentions_case_studies": lambda state, log: any("case" in msg['content'].lower() or "project" in msg['content'].lower() for msg in log if msg['role'] == 'agent')
        }
    ),

    "skeptical_cfo": ConversationTestCase(
        name="Skeptical CFO",
        description="Cost-focused executive who needs strong ROI justification",
        lead_profile={
            "lead_id": "test_cfo_002",
            "name": "Robert Kim",
            "company": "Regional Bank Corp", 
            "role": "CFO"
        },
        conversation_flow=[
            "I'm evaluating IT service providers. Our current setup costs us $2M annually. How can you justify being more expensive?",
            "That's a lot of claims. Do you have specific ROI numbers from similar banking clients?",
            "What's your typical pricing model? I need to understand the total cost structure.",
            "I'm not convinced the ROI justifies the cost. What guarantees do you offer?"
        ],
        expected_behaviors={
            "searches_pricing_info": lambda state, log: any("pricing" in doc.lower() for doc in state.get('retrieved_docs', [])),
            "searches_banking_cases": lambda state, log: any("banking" in doc.lower() or "bank" in doc.lower() for doc in state.get('retrieved_docs', [])),
            "detects_price_objection": lambda state, log: state.get('detected_objections') and any("cost" in obj.lower() or "expensive" in obj.lower() for obj in state['detected_objections']),
            "stays_in_objection_handling": lambda state, log: state.get('conversation_stage') == 'objection_handling',
            "provides_roi_evidence": lambda state, log: any("roi" in msg['content'].lower() or "return" in msg['content'].lower() for msg in log if msg['role'] == 'agent')
        }
    ),

    "tire_kicker": ConversationTestCase(
        name="Tire Kicker",
        description="Asks many questions but shows no real buying intent",
        lead_profile={
            "lead_id": "test_tire_kicker_003",
            "name": "Alex Johnson",
            "company": "Startup Inc",
            "role": "Developer"
        },
        conversation_flow=[
            "What services do you offer?",
            "Interesting. What about AI capabilities?",
            "Cool. What programming languages do you use?",
            "How many employees do you have?",
            "What's your company history?",
            "Thanks for the info. I'll think about it."
        ],
        expected_behaviors={
            "low_qualification_scores": lambda state, log: all(score <= 5 for score in state.get('lead_qualification_score', {}).values()),
            "multiple_knowledge_searches": lambda state, log: len(state.get('retrieved_docs', [])) >= 3,
            "no_buying_signals": lambda state, log: len(state.get('buying_signals_detected', [])) == 0,
            "stays_in_discovery": lambda state, log: state.get('conversation_stage') == 'discovery',
            "low_authority_detected": lambda state, log: state.get('lead_qualification_score', {}).get('authority_level', 10) <= 4
        }
    ),

    "returning_lead": ConversationTestCase(
        name="Returning Lead",
        description="Lead with existing memory/history resuming conversation",
        lead_profile={
            "lead_id": "lead_2024_0156",  # This lead has existing memory
            "name": "Jennifer Martinez",
            "company": "HealthTech Innovations", 
            "role": "VP of Engineering"
        },
        conversation_flow=[
            "Hi again, I wanted to follow up on our previous conversation about AI integration.",
            "Yes, I remember we discussed the Hami project. Can you tell me more about the implementation challenges you faced?",
            "That's helpful. What about ongoing maintenance and support?"
        ],
        expected_behaviors={
            "loads_previous_memory": lambda state, log: state.get('long_term_memory') != {},
            "references_past_conversation": lambda state, log: any("previous" in msg['content'].lower() or "remember" in msg['content'].lower() for msg in log if msg['role'] == 'agent'),
            "builds_on_past_context": lambda state, log: state.get('conversation_stage') != 'discovery',  # Should skip basic discovery
            "maintains_qualification_data": lambda state, log: state.get('lead_qualification_score', {}).get('authority_level', 0) > 5
        }
    ),

    "urgent_buyer": ConversationTestCase(
        name="Urgent Buyer",
        description="Lead with immediate need and clear timeline pressure",
        lead_profile={
            "lead_id": "test_urgent_004",
            "name": "Maria Rodriguez",
            "company": "Enterprise Corp",
            "role": "IT Director"
        },
        conversation_flow=[
            "We need to implement a new ERP system by end of Q1. Our current system is failing and we're losing money daily.",
            "We have budget approved and executive buy-in. I need to know if you can deliver in 3 months.",
            "What's your availability for an emergency meeting this week?",
            "Perfect, let's get the contract process started immediately."
        ],
        expected_behaviors={
            "detects_high_urgency": lambda state, log: state.get('lead_qualification_score', {}).get('need_urgency', 0) >= 8,
            "searches_erp_capabilities": lambda state, log: any("erp" in doc.lower() for doc in state.get('retrieved_docs', [])),
            "progresses_quickly_to_closing": lambda state, log: state.get('conversation_stage') in ['closing'],
            "detects_multiple_buying_signals": lambda state, log: len(state.get('buying_signals_detected', [])) >= 2,
            "high_overall_qualification": lambda state, log: sum(state.get('lead_qualification_score', {}).values()) >= 25
        }
    ),

    "competitor_comparison": ConversationTestCase(
        name="Competitor Comparison",
        description="Lead actively comparing multiple vendors",
        lead_profile={
            "lead_id": "test_comparison_005",
            "name": "David Park",
            "company": "Regional Healthcare",
            "role": "VP Technology"
        },
        conversation_flow=[
            "I'm evaluating several vendors for our digital transformation project. How do you compare to Accenture and IBM?",
            "What makes your approach different from the big consulting firms?",
            "Can you provide references from similar healthcare organizations?",
            "What's your win rate against these competitors?"
        ],
        expected_behaviors={
            "addresses_competition": lambda state, log: any("competitor" in msg['content'].lower() or "different" in msg['content'].lower() for msg in log if msg['role'] == 'agent'),
            "provides_differentiation": lambda state, log: any("unique" in msg['content'].lower() or "advantage" in msg['content'].lower() for msg in log if msg['role'] == 'agent'),
            "searches_healthcare_cases": lambda state, log: any("healthcare" in doc.lower() for doc in state.get('retrieved_docs', [])),
            "maintains_professional_tone": lambda state, log: not any("better than" in msg['content'].lower() or "superior" in msg['content'].lower() for msg in log if msg['role'] == 'agent')
        }
    ),

    "knowledge_tester": ConversationTestCase(
        name="Knowledge Tester",
        description="Technical lead testing agent's domain expertise",
        lead_profile={
            "lead_id": "test_knowledge_006",
            "name": "Dr. Lisa Wang",
            "company": "MedResearch Institute",
            "role": "Chief Data Scientist"
        },
        conversation_flow=[
            "What's your experience with FHIR compliance in healthcare AI systems?",
            "How do you handle PHI data security in cloud deployments?",
            "What machine learning frameworks do you typically use for clinical decision support?",
            "Can you explain your approach to model explainability in healthcare AI?"
        ],
        expected_behaviors={
            "attempts_knowledge_searches": lambda state, log: len(state.get('retrieved_docs', [])) >= 2,
            "acknowledges_knowledge_gaps": lambda state, log: any("specific" in msg['content'].lower() or "details" in msg['content'].lower() for msg in log if msg['role'] == 'agent'),
            "maintains_technical_focus": lambda state, log: state.get('communication_style_preference') == 'technical',
            "searches_healthcare_tech": lambda state, log: any("healthcare" in doc.lower() or "technical" in doc.lower() for doc in state.get('retrieved_docs', []))
        }
    )
}

def run_all_tests():
    """Run all conversation test cases"""
    print("Starting Conversation Test Suite")
    print("="*60)
    
    results = {}
    
    for test_name, test_case in TEST_CASES.items():
        try:
            # Create fresh agent for each test
            agent_api = get_agent_api(test_case.lead_profile['lead_id'])
            
            # Initialize knowledge bases (only once)
            if not hasattr(run_all_tests, 'initialized'):
                agent_api.initialize_knowledge()
                run_all_tests.initialized = True
            
            # Run test
            test_results = test_case.run_test(agent_api)
            results[test_name] = test_results
            
            # Brief summary
            passed = len(test_results['passed_checks'])
            failed = len(test_results['failed_checks'])
            print(f"\nSUMMARY: {passed} passed, {failed} failed")
            
        except Exception as e:
            print(f"ERROR running {test_name}: {e}")
            results[test_name] = {"error": str(e)}
        
        print("\n" + "-"*40 + "\n")
    
    # Overall summary
    print("OVERALL TEST RESULTS")
    print("="*60)
    for test_name, result in results.items():
        if 'error' in result:
            print(f"❌ {test_name}: ERROR - {result['error']}")
        else:
            passed = len(result['passed_checks'])
            total = passed + len(result['failed_checks'])
            print(f"{'✅' if passed == total else '⚠️ '} {test_name}: {passed}/{total} checks passed")
    
    return results

def run_single_test(test_name):
    """Run a single test case by name"""
    if test_name not in TEST_CASES:
        print(f"Test '{test_name}' not found. Available tests: {list(TEST_CASES.keys())}")
        return
    
    test_case = TEST_CASES[test_name]
    agent_api = get_agent_api(test_case.lead_profile['lead_id'])
    agent_api.initialize_knowledge()
    
    return test_case.run_test(agent_api)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        run_single_test(test_name)
    else:
        # Run all tests
        run_all_tests()