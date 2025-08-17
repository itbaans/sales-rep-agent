""" 
Pricing Model Document Generator for Systems Ltd
Creates realistic commercial documents with pricing complexities and hidden details
"""

import os
import json
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
import uuid
from agent.services.llm_service import get_llm

class PricingDocumentGenerator:
    """Generates realistic pricing and commercial documents"""
    
    def __init__(self, output_dir: str = "pricing_docs"):
        self.output_dir = output_dir
        self.llm = get_llm("gemini-2.5-flash-lite")
        os.makedirs(output_dir, exist_ok=True)
        
        # Systems Ltd commercial data
        self.regional_tax_rates = {
            "Pakistan": "16% Sales Tax + 2% Withholding Tax",
            "UAE": "0% VAT for international services",
            "KSA": "15% VAT",
            "Qatar": "5% VAT",
            "Oman": "5% VAT"
        }
        self.contract_terms = [
            "30-day payment terms", "45-day payment with discount", 
            "15% penalty for late payment", "Quarterly price reviews",
            "Annual escalation clause", "Currency fluctuation adjustment"
        ]
        self.systems_employees = [
            ("Ahmed Raza", "Commercial Director"), ("Fatima Khan", "Pricing Specialist"),
            ("Bilal Siddiqui", "Legal Counsel"), ("Sana Mahmood", "Deal Architect"),
            ("Omar Farooq", "Tax Consultant")
        ]
        
    def _get_systems_employee(self) -> str:
        """Get random Systems Ltd commercial expert"""
        name, role = random.choice(self.systems_employees)
        return f"{name} ({role})"
    
    def generate_pricing_guide(self, model_name: str, model: Dict) -> Dict[str, Any]:
        """Generate ambiguous pricing guide with hidden complexities"""
        prompt = f"""Create a pricing guide document for Systems Ltd's "{model_name}" commercial model.

Model Description:
{model['description']}
Rate Structure: {model.get('rate_structure', 'Variable')}
Suitable For: {', '.join(model['suitable_for'])}
Notes: {model['notes']}

Make this guide realistic by including:
- Intentionally vague rate ranges
- Footnotes with important exceptions
- Regional tax implications not fully explained
- "Standard" terms that are always negotiated
- Hidden cost components in examples
- Case studies with selective metrics
- Implementation fees buried in details
- Discount structures with unclear eligibility

Structure with problematic sections:
1. Overview (overly optimistic benefits)
2. Rate Structure (ambiguous ranges)
3. Suitable Use Cases (overly broad)
4. Contractual Considerations (hidden traps)
5. Regional Variations (incomplete coverage)
6. FAQ (answers that create more questions)"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "pricing_guide",
            "pricing_model": model_name,
            "applicable_regions": random.sample(list(self.regional_tax_rates.keys()), 2),
            "created_date": datetime.now().isoformat(),
            "author": self._get_systems_employee(),
            "status": random.choice(["Draft", "Confidential", "Internal Use Only"])
        }
        
        return {
            "content": self._add_pricing_noise(content, model),
            "metadata": metadata
        }
    
    def generate_client_proposal(self, model_name: str, model: Dict) -> Dict[str, Any]:
        """Generate client proposal with advantageous framing"""
        client = random.choice(["Habib Bank", "PTCL", "Dubai Islamic Bank", "Saudi Telecom"])
        duration = random.choice(["6-month", "1-year", "2-year"])
        
        prompt = f"""Create a client pricing proposal for {client} using Systems Ltd's "{model_name}" model.

Model Details:
{model['description']}
Notes: {model['notes']}

Make this proposal realistic by including:
- Strategic omission of unfavorable terms
- Buried implementation costs
- "Standard" clauses that aren't standard
- Optimistic savings projections
- Flexible interpretations of scope
- Payment terms favoring Systems Ltd
- Tax treatment ambiguities
- Auto-renewal clauses in fine print

Structure with advantageous framing:
1. Executive Summary (overstated benefits)
2. Proposed Pricing Model (selective disclosure)
3. Implementation Plan (underestimated effort)
4. Terms & Conditions (vendor-favorable)
5. Next Steps (pressure to sign quickly)"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "client_proposal",
            "pricing_model": model_name,
            "client": client,
            "duration": duration,
            "value": f"${random.randint(50,500)}K",
            "prepared_date": datetime.now().isoformat(),
            "author": self._get_systems_employee()
        }
        
        return {
            "content": self._add_proposal_noise(content, model),
            "metadata": metadata
        }
    
    def generate_contract_framework(self, model_name: str, model: Dict) -> Dict[str, Any]:
        """Generate contract framework with problematic clauses"""
        prompt = f"""Create a contract framework document for Systems Ltd's "{model_name}" pricing model.

Model Characteristics:
{model['description']}
Suitable For: {', '.join(model['suitable_for'])}
Key Notes: {model['notes']}

Make this framework realistic by including:
- Ambiguous termination clauses
- Intellectual property ownership gray areas
- Limitation of liability favoring vendor
- Audit rights with excessive access
- Change control procedures that enable scope creep
- Service credits that are hard to claim
- Data protection compliance gaps
- Dispute resolution favoring vendor location

Structure with hidden risks:
1. Definitions (broad interpretations)
2. Pricing & Payment (variable components)
3. Term & Termination (auto-renewal traps)
4. Warranties (limited and conditional)
5. Liability (cap excludes key items)
6. Governing Law (vendor-friendly jurisdiction)"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "contract_framework",
            "pricing_model": model_name,
            "version": f"{random.randint(1, 5)}.{random.randint(0, 3)}",
            "last_updated": (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat(),
            "legal_owner": self._get_systems_employee(),
            "risk_level": random.choice(["Medium", "High", "Requires Review"])
        }
        
        return {
            "content": self._add_contract_noise(content, model),
            "metadata": metadata
        }
    
    def generate_cost_analysis(self, model_name: str, model: Dict) -> Dict[str, Any]:
        """Generate cost analysis with hidden markups"""
        region = random.choice(list(self.regional_tax_rates.keys()))
        
        prompt = f"""Create an internal cost analysis for Systems Ltd's "{model_name}" pricing model in {region}.

Model Details:
{model['description']}
Rate Structure: {model.get('rate_structure', 'Not specified')}
Tax Treatment: {self.regional_tax_rates[region]}

Make this analysis realistic by including:
- Buried overhead allocations
- Unallocated R&D costs
- Regional tax optimizations
- Margin stacking opportunities
- "Standard" markups that vary
- Cost baseline inaccuracies
- Sensitivity analysis gaps
- Comparison benchmarks without sources

Structure with incomplete transparency:
1. Direct Costs (selective inclusions)
2. Indirect Costs (inflated allocations)
3. Margin Structure (tiered obscurity)
4. Tax Considerations (optimization focus)
5. Competitive Positioning (favorable comparison)
6. Risk Assessment (downplayed)"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "cost_analysis",
            "pricing_model": model_name,
            "region": region,
            "target_margin": f"{random.randint(15,35)}%",
            "prepared_date": datetime.now().isoformat(),
            "author": self._get_systems_employee(),
            "confidentiality": "Strictly Internal"
        }
        
        return {
            "content": self._add_cost_noise(content, model),
            "metadata": metadata
        }
    
    def generate_negotiation_playbook(self, model_name: str, model: Dict) -> Dict[str, Any]:
        """Generate negotiation tactics with ethical gray areas"""
        prompt = f"""Create a negotiation playbook for Systems Ltd's "{model_name}" pricing model.

Model Characteristics:
{model['description']}
Suitable For: {', '.join(model['suitable_for'])}
Key Constraints: {model['notes']}

Make this playbook realistic by including:
- Anchor pricing tactics
- Concession trading strategies
- Scope management techniques
- Tax treatment ambiguities to exploit
- Payment term pressure points
- Change control monetization
- Deal sweeteners with low cost
- Walk-away thresholds

Structure with competitive tactics:
1. Positioning (value over cost)
2. Concession Strategy (tradable items)
3. Discount Authority (artificial limits)
4. Payment Terms (cash flow advantages)
5. Contractual Flexibility (future advantage)
6. Closing Techniques (time pressure)"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "negotiation_playbook",
            "pricing_model": model_name,
            "created_date": datetime.now().isoformat(),
            "author": self._get_systems_employee(),
            "clearance": "Level 4 Commercial Team Only"
        }
        
        return {
            "content": self._add_negotiation_noise(content, model),
            "metadata": metadata
        }
    
    def _add_pricing_noise(self, content: str, model: Dict) -> str:
        """Add pricing ambiguities and hidden clauses"""
        noise_items = [
            f"\n[INTERNAL: Actual minimum rate is {random.randint(5,15)}% higher]\n",
            f"\n*Tax treatment varies by region - consult finance*\n",
            f"\n**Discounts require VP approval - not advertised**\n",
            f"\n[NOTE: {model['notes'].split('.')[0]}]\n",
            f"\n<!-- Implementation fees extra - see section 7.2 -->\n",
            f"\n[FOOTNOTE: {random.choice(list(self.regional_tax_rates.values()))} applies]\n"
        ]
        
        for _ in range(random.randint(3, 5)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(noise_items) + content[pos:]
        
        return content
    
    def _add_proposal_noise(self, content: str, model: Dict) -> str:
        """Add proposal traps and advantageous framing"""
        traps = [
            f"\n[PRICING: First-year discount reverts to +{random.randint(10,25)}% in year 2]\n",
            f"\n*Scope limitation: {random.choice(model['suitable_for'])} excluded*\n",
            f"\n**Change requests at {random.choice(['T&M', 'premium rates'])}**\n",
            f"\n[TERMS: Auto-renewal for {random.randint(1,3)} years unless cancelled]\n",
            f"\n<!-- Penalty clauses in section 8.4 -->\n",
            f"\n[CLIENT-SPECIFIC: Insert termination difficulty clauses here]\n"
        ]
        
        for _ in range(random.randint(3, 5)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(traps) + content[pos:]
        
        return content
    
    def _add_contract_noise(self, content: str, model: Dict) -> str:
        """Add contractual gray areas"""
        clauses = [
            f"\n[CLAUSE: Liability capped at fees paid, excluding IP infringement]\n",
            f"\n*Governing law: {random.choice(['Pakistan', 'Dubai International Financial Centre'])}*\n",
            f"\n**Audit rights: Quarterly with 30-day notice**\n",
            f"\n[WARNING: This termination clause requires legal review]\n",
            f"\n<!-- IP ownership remains with Systems Ltd for custom developments -->\n",
            f"\n[NOTE: {model['notes'].split('.')[0]} affects this section]\n"
        ]
        
        for _ in range(random.randint(4, 6)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(clauses) + content[pos:]
        
        return content
    
    def _add_cost_noise(self, content: str, model: Dict) -> str:
        """Add cost ambiguities and markups"""
        markups = [
            f"\n[COST: Unallocated R&D amortization +{random.randint(5,15)}%]\n",
            f"\n*Overhead allocation: {random.randint(10,30)}% of direct costs*\n",
            f"\n**Minimum margin threshold: {random.randint(20,35)}%**\n",
            f"\n[HIDDEN: Account management fee {random.randint(3,8)}%]\n",
            f"\n<!-- Regional tax optimization saves ~{random.randint(5,12)}% -->\n",
            f"\n[INTERNAL: Benchmark data from {random.randint(2020,2022)} - outdated]\n"
        ]
        
        for _ in range(random.randint(4, 6)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(markups) + content[pos:]
        
        return content
    
    def _add_negotiation_noise(self, content: str, model: Dict) -> str:
        """Add negotiation tactics and gray areas"""
        tactics = [
            f"\n[TACTIC: Anchor at +{random.randint(15,30)}% of target price]\n",
            f"\n*Concession: Offer extended payment to preserve rate*\n",
            f"\n**Pressure point: Implementation timeline flexibility**\n",
            f"\n[PLAY: Introduce scope change during final negotiation]\n",
            f"\n<!-- BATNA: Walk away below {random.randint(18,25)}% margin -->\n",
            f"\n[NOTE: Use tax treatment ambiguity as concession]\n"
        ]
        
        for _ in range(random.randint(4, 6)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(tactics) + content[pos:]
        
        return content
    
    def generate_pricing_documents(self, model_name: str, model: Dict) -> List[Dict]:
        """Generate full document set for a pricing model"""
        print(f"Generating documents for: {model_name}")
        
        documents = []
        documents.append(self.generate_pricing_guide(model_name, model))
        documents.append(self.generate_contract_framework(model_name, model))
        documents.append(self.generate_cost_analysis(model_name, model))

        return documents
    
    def generate_all_pricing_docs(self, pricing_data: Dict[str, Dict]) -> List[Dict]:
        """Generate documents for all pricing models"""
        print(f"Generating documents for {len(pricing_data)} pricing models...")
        
        all_documents = []
        
        for model_name, model_data in pricing_data.items():
            try:
                model_docs = self.generate_pricing_documents(model_name, model_data)
                all_documents.extend(model_docs)
                
                # Save documents immediately
                for doc in model_docs:
                    doc_id = f"SL-PRICE-{doc['metadata']['document_type']}-{uuid.uuid4().hex[:6]}"
                    filename = f"{doc_id}.txt"
                    filepath = os.path.join(self.output_dir, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(f"=== SYSTEMS LTD COMMERCIAL DOCUMENT ===\n")
                        f.write(f"Pricing Model: {model_name}\n")
                        f.write(f"=== METADATA ===\n{json.dumps(doc['metadata'], indent=2)}\n\n")
                        f.write(f"=== CONTENT ===\n{doc['content']}")
                    
                    # Add filename to doc for indexing
                    doc["filename"] = filename
            except Exception as e:
                print(f"Error generating documents for {model_name}: {str(e)}")
        
        # Save master index
        index_path = os.path.join(self.output_dir, "pricing_document_index.json")
        with open(index_path, 'w') as f:
            json.dump([{
                "pricing_model": model_name,
                "filename": doc["filename"],
                "type": doc["metadata"]["document_type"],
                "suitable_for": model_data.get("suitable_for", [])[0] if model_data.get("suitable_for") else ""
            } for model_name, model_data in pricing_data.items() for doc in all_documents if doc["metadata"]["pricing_model"] == model_name], f, indent=2)
        
        print(f"\nGenerated {len(all_documents)} documents across {len(pricing_data)} pricing models")
        print(f"Documents saved to: {self.output_dir}")
        return all_documents

# Pricing model data from your input


if __name__ == "__main__":
    # Initialize generator
    generator = PricingDocumentGenerator(output_dir="pricing_docs")
    data=None
    with open("data/company_docs/company_price_models.json", "r") as f:
        data = json.load(f)
    # Generate documents for all pricing models
    generator.generate_all_pricing_docs(data)