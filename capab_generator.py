""" 
Capability Document Generator for Systems Ltd
Creates specialized documents for company capability areas with realistic imperfections
"""

import os
import json
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
import uuid
from agent.services.llm_service import get_llm

class CapabilityDocumentGenerator:
    """Generates realistic capability documents for Systems Ltd service areas"""
    
    def __init__(self, output_dir: str = "capability_docs"):
        self.output_dir = output_dir
        self.llm = get_llm("gemini-2.5-flash-lite")
        os.makedirs(output_dir, exist_ok=True)
        
        # Systems Ltd-specific data
        self.systems_employees = [
            ("Asif Akram", "Solutions Architect"), ("Fatima Khan", "Practice Lead"),
            ("Bilal Ahmed", "Technical Director"), ("Sana Mahmood", "Capability Manager"),
            ("Omar Farooq", "Data Science Head"), ("Zainab Raza", "Quality Assurance"),
            ("Tariq Nadeem", "Cloud Architect"), ("Ayesha Siddiqui", "UX Principal"),
            ("Kamran Ali", "Security Officer"), ("Hina Sheikh", "Delivery Head")
        ]
        self.systems_offices = ["Karachi HQ", "Lahore Center", "Dubai Office", "Riyadh Center"]
        self.tech_partners = ["Temenos", "Microsoft", "Automation Anywhere", "SAP", "Oracle", "AWS"]
        
    def _get_systems_employee(self) -> str:
        """Get random Systems Ltd expert with role"""
        name, role = random.choice(self.systems_employees)
        return f"{name} ({role})"
    
    def generate_capability_overview(self, capability_name: str, capability: Dict) -> Dict[str, Any]:
        """Generate capability overview with marketing spin and reality gaps"""
        prompt = f"""Create a capability overview document for Systems Ltd's "{capability_name}" service offering.

Key Details:
{capability['details']}
Industry Focus: {', '.join(capability['industry_focus'])}
Strength Level: {capability['strength_level']}
Notes: {capability['notes']}

Make this document realistic by including:
- Overstated marketing claims mixed with actual limitations
- "Strategic advantages" that are vaguely defined
- References to partner technologies without concrete details
- Selective success metrics that ignore challenges
- Contradictions between claimed expertise and implementation notes
- Buzzword-heavy descriptions of capabilities
- Unverified client testimonials

Structure:
1. Executive Summary (overly optimistic)
2. Market Positioning (with competitive gaps)
3. Technical Capabilities (with unclear specifics)
4. Client Success Stories (partial truths)
5. Implementation Approach (vague methodology)
6. Differentiators (some questionable)"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "capability_overview",
            "capability": capability_name,
            "industry_focus": capability['industry_focus'],
            "strength_level": capability['strength_level'],
            "created_date": datetime.now().isoformat(),
            "author": self._get_systems_employee(),
            "office": random.choice(self.systems_offices),
            "status": random.choice(["Draft", "Internal Use Only", "Client Facing"])
        }
        
        return {
            "content": self._add_marketing_noise(content, capability),
            "metadata": metadata
        }
    
    def generate_implementation_playbook(self, capability_name: str, capability: Dict) -> Dict[str, Any]:
        """Generate incomplete implementation guide with tribal knowledge"""
        prompt = f"""Create a technical implementation playbook for Systems Ltd's "{capability_name}" capability.

Key Details:
{capability['details']}
Industry Focus: {', '.join(capability['industry_focus'])}
Implementation Notes: {capability['notes']}

Make this document realistic by including:
- Incomplete step-by-step instructions
- Environment-specific configurations that don't generalize
- "Ask [Expert Name]" instead of proper documentation
- Hardcoded values from sample implementations
- Deprecated approaches still listed as options
- Missing diagrams where they'd be most useful
- Security considerations as afterthoughts
- Performance tuning "secrets" known only to veterans

Structure erratically with:
1. Architecture Overview (with missing components)
2. Setup Guide (with environment-specific gotchas)
3. Configuration Reference (with hardcoded examples)
4. Troubleshooting (with "contact support" as first option)
5. Best Practices (contradicted by actual implementations)"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "implementation_playbook",
            "capability": capability_name,
            "version": f"{random.randint(1, 3)}.{random.randint(0, 2)}",
            "last_updated": (datetime.now() - timedelta(days=random.randint(90, 730))).isoformat(),
            "author": self._get_systems_employee(),
            "review_status": random.choice(["Incomplete", "Partially Validated", "Needs Update"])
        }
        
        return {
            "content": self._add_technical_noise(content, capability),
            "metadata": metadata
        }
    
    def generate_client_proposal_template(self, capability_name: str, capability: Dict) -> Dict[str, Any]:
        """Generate proposal template with placeholder traps"""
        prompt = f"""Create a client proposal template for Systems Ltd's "{capability_name}" service.

Key Details:
{capability['details']}
Strength Level: {capability['strength_level']}
Notes: {capability['notes']}

Make this template realistic by including:
- Overpromised timelines and deliverables
- Placeholders never replaced in actual proposals
- Pricing tables with hidden cost traps
- Scope ambiguities that lead to change requests
- "Standard" terms that clients always negotiate
- Case studies missing critical context
- Technical assumptions that often prove wrong
- Team composition that never matches reality

Structure with problematic sections:
1. Executive Summary (generic value propositions)
2. Technical Approach (vague on customizations)
3. Timeline (optimistic phases with undefined dependencies)
4. Team Structure (roles that get reassigned)
5. Pricing (ambiguous line items)
6. Terms & Conditions (unfavorable clauses hidden)"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "proposal_template",
            "capability": capability_name,
            "created_date": datetime.now().isoformat(),
            "last_used": (datetime.now() - timedelta(days=random.randint(7, 120))).isoformat(),
            "win_rate": f"{random.randint(20, 60)}%",
            "author": self._get_systems_employee()
        }
        
        return {
            "content": self._add_proposal_noise(content, capability),
            "metadata": metadata
        }
    
    def generate_competitive_analysis(self, capability_name: str, capability: Dict) -> Dict[str, Any]:
        """Generate biased competitive analysis with dated information"""
        competitors = random.sample(["TCS", "Infosys", "Tech Mahindra", "IBM", "Accenture", "Local Rivals"], 3)
        
        prompt = f"""Create a competitive analysis document for Systems Ltd's "{capability_name}" offering.

Key Details:
{capability['details']}
Strength Level: {capability['strength_level']}
Notes: {capability['notes']}

Competitors: {', '.join(competitors)}

Make this analysis realistic by including:
- Outdated competitor information
- Biased strength/weakness assessments
- Questionable differentiators
- "Confidential" intelligence without sources
- Overstated market share claims
- Ignored competitive threats
- Regional focus gaps not acknowledged
- Pricing comparisons with hidden assumptions

Structure with blind spots:
1. Market Landscape (incomplete player mapping)
2. Competitor Profiles (outdated capabilities)
3. SWOT Analysis (internal bias evident)
4. Differentiators (some unverified)
5. Strategic Recommendations (ignoring internal limitations)"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "competitive_analysis",
            "capability": capability_name,
            "competitors": competitors,
            "created_date": (datetime.now() - timedelta(days=random.randint(180, 730))).isoformat(),
            "author": self._get_systems_employee(),
            "confidence": random.choice(["Low", "Medium", "High", "Unverified"])
        }
        
        return {
            "content": self._add_analysis_noise(content, capability),
            "metadata": metadata
        }
    
    def generate_roadmap_document(self, capability_name: str, capability: Dict) -> Dict[str, Any]:
        """Generate aspirational roadmap with unrealistic timelines"""
        prompt = f"""Create a capability roadmap document for Systems Ltd's "{capability_name}" service.

Current State:
Strength Level: {capability['strength_level']}
Notes: {capability['notes']}

Make this roadmap realistic by including:
- Overambitious timelines
- Unresolved dependencies
- Resource commitments that don't exist
- Market assumptions not validated
- Technical milestones without clear owners
- Partner commitments not confirmed
- "Future state" visions disconnected from reality

Structure with wishful thinking:
1. Current State Assessment (downplaying weaknesses)
2. 12-Month Roadmap (aggressive timelines)
3. Investment Requirements (underestimated)
4. Key Initiatives (some without clear ROI)
5. Growth Metrics (optimistic projections)
6. Risks (minimized or vague)"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "capability_roadmap",
            "capability": capability_name,
            "timeframe": f"{datetime.now().year}-{datetime.now().year+2}",
            "created_date": datetime.now().isoformat(),
            "author": self._get_systems_employee(),
            "approval_status": random.choice(["Draft", "Leadership Review", "Conditionally Approved"])
        }
        
        return {
            "content": self._add_roadmap_noise(content, capability),
            "metadata": metadata
        }
    
    def _add_marketing_noise(self, content: str, capability: Dict) -> str:
        """Add marketing hype and reality gaps"""
        noise_items = [
            f"\n[INTERNAL: Actual capabilities more limited than described]\n",
            f"\n*{random.choice(self.tech_partners)} partnership status uncertain*\n",
            f"\n**Client case study exaggerated - verify before reuse**\n",
            f"\n[NOTE: {capability['notes'].split('.')[0]}]\n",
            f"\n<!-- Market share numbers need verification -->\n",
            f"\n[Differentiator: Contradicted by implementation experience]\n"
        ]
        
        for _ in range(random.randint(3, 5)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(noise_items) + content[pos:]
        
        return content
    
    def _add_technical_noise(self, content: str, capability: Dict) -> str:
        """Add technical documentation gaps"""
        tech_gaps = [
            f"\n[CONFIGURATION: Environment-specific values not parameterized]\n",
            f"\n**TODO: Add {random.choice(['diagram', 'screenshot', 'architecture'])} here**\n",
            f"\n[WARNING: Deprecated approach - remove before production use]\n",
            f"\n<!-- Actual implementation differs for {random.choice(capability['industry_focus'])} clients -->\n",
            f"\n[PERFORMANCE: Known bottlenecks in {random.choice(['scaling', 'data processing', 'integration'])}]\n",
            f"\n**Contact {self._get_systems_employee()} for production settings**\n"
        ]
        
        for _ in range(random.randint(4, 6)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(tech_gaps) + content[pos:]
        
        return content
    
    def _add_proposal_noise(self, content: str, capability: Dict) -> str:
        """Add proposal traps and placeholders"""
        traps = [
            f"\n[PRICING: Marginally profitable at this rate]\n",
            f"\n*Scope gap: {random.choice(['integration', 'data migration', 'training'])} not included*\n",
            f"\n**Resource allocation optimistic by {random.randint(15,40)}%**\n",
            f"\n[CLIENT-SPECIFIC: Replace all {{bracketed}} placeholders]\n",
            f"\n<!-- Template last updated before {capability['strength_level']} capability changes -->\n",
            f"\n[RISK: {capability['notes'].split('.')[0]}]\n"
        ]
        
        for _ in range(random.randint(3, 5)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(traps) + content[pos:]
        
        return content
    
    def _add_analysis_noise(self, content: str, capability: Dict) -> str:
        """Add competitive analysis flaws"""
        flaws = [
            f"\n[INTEL: Dated {random.randint(6,24)} months - verify]\n",
            f"\n*Bias: Overstates {random.choice(['differentiators', 'win rates', 'capabilities'])}*\n",
            f"\n**Missing competitor: {random.choice(['TCS', 'Infosys', 'Local Firm'])} not analyzed**\n",
            f"\n[ASSUMPTION: {capability['strength_level']} rating questionable]\n",
            f"\n<!-- Partner capability changes not reflected -->\n"
        ]
        
        for _ in range(random.randint(3, 4)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(flaws) + content[pos:]
        
        return content
    
    def _add_roadmap_noise(self, content: str, capability: Dict) -> str:
        """Add roadmap unrealistic elements"""
        realities = [
            f"\n[RESOURCE: No budget approved for this initiative]\n",
            f"\n*Timeline: Aggressive by {random.randint(2,6)} quarters*\n",
            f"\n**Dependency: {random.choice(self.tech_partners)} roadmap not aligned**\n",
            f"\n[RISK: {capability['notes'].split('.')[0]} not addressed]\n",
            f"\n<!-- Market assumption unvalidated -->\n"
        ]
        
        for _ in range(random.randint(3, 5)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(realities) + content[pos:]
        
        return content
    
    def generate_capability_documents(self, capability_name: str, capability: Dict) -> List[Dict]:
        """Generate full document set for a capability area"""
        print(f"Generating documents for: {capability_name}")
        
        documents = []
        
        documents.append(self.generate_implementation_playbook(capability_name, capability))
        documents.append(self.generate_roadmap_document(capability_name, capability))
        
        return documents
    
    def generate_all_capability_docs(self, capabilities_data: Dict[str, Dict]) -> List[Dict]:
        """Generate documents for all capability areas"""
        print(f"Generating documents for {len(capabilities_data)} capabilities...")
        
        all_documents = []
        
        for capability_name, capability_data in capabilities_data.items():
            try:
                capability_docs = self.generate_capability_documents(capability_name, capability_data)
                all_documents.extend(capability_docs)
                
                # Save capability documents immediately
                for doc in capability_docs:
                    doc_id = f"SL-CAP-{doc['metadata']['document_type']}-{uuid.uuid4().hex[:6]}"
                    filename = f"{doc_id}.txt"
                    filepath = os.path.join(self.output_dir, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(f"=== SYSTEMS LTD CAPABILITY DOCUMENT ===\n")
                        f.write(f"Capability: {capability_name}\n")
                        f.write(f"=== METADATA ===\n{json.dumps(doc['metadata'], indent=2)}\n\n")
                        f.write(f"=== CONTENT ===\n{doc['content']}")
                    
                    # Add filename to doc for indexing
                    doc["filename"] = filename
            except Exception as e:
                print(f"Error generating documents for {capability_name}: {str(e)}")
        
        # Save master index
        index_path = os.path.join(self.output_dir, "capability_document_index.json")
        with open(index_path, 'w') as f:
            json.dump([{
                "capability": capability_name,
                "filename": doc["filename"],
                "type": doc["metadata"]["document_type"],
                "strength_level": doc["metadata"].get("strength_level", "")
            } for doc in all_documents], f, indent=2)
        
        print(f"\nGenerated {len(all_documents)} documents across {len(capabilities_data)} capabilities")
        print(f"Documents saved to: {self.output_dir}")
        return all_documents


if __name__ == "__main__":
    # Initialize generator
    generator = CapabilityDocumentGenerator(output_dir="capability_docs")

    data=None
    with open("data/company_docs/company_technical.json", "r") as f:
        data = json.load(f)

    # Generate documents for all capabilities
    generator.generate_all_capability_docs(data)