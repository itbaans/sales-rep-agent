""" 
Realistic Document Generator for Systems Ltd B2B Software Services
Creates messy, unstructured documents mirroring real corporate environments
with Systems Ltd-specific data
"""

import os
import json
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
import uuid
from agent.services.llm_service import get_llm

class DocumentGenerator:
    """Generates realistic, messy corporate documents for Systems Ltd"""
    
    def __init__(self, output_dir: str = "generated_docs"):
        self.output_dir = output_dir
        self.llm = get_llm("gemini-2.5-flash-lite")
        os.makedirs(output_dir, exist_ok=True)
        
        # Systems Ltd-specific data
        self.industries = ["Banking", "Telecom", "Retail", "Government", "Healthcare", "Insurance", "Manufacturing"]
        self.project_types = [
            "ERP Implementation (Oracle/SAP)",
            "Digital Transformation",
            "Cloud Migration (AWS/Azure)",
            "AI/ML Solutions",
            "Core Banking Upgrade",
            "CRM Implementation",
            "Payment Gateway Integration",
            "Data Center Modernization"
        ]
        self.companies = [
            "Habib Bank Limited", "Jazz Telecom", "National Bank of Pakistan", 
            "PTCL", "Al-Futtaim Group", "Dubai Islamic Bank", "Emirates NBD",
            "Abu Dhabi Commercial Bank", "Etisalat", "Saudi Telecom Company"
        ]
        self.systems_tech = [
            "Nexus Core Banking", "Optimus ERP", "Aurora AI Platform",
            "Stratus Cloud Framework", "Vectra Payment Hub", "Nimbus Mobile Banking",
            "OmniChannel Retail Suite", "Quantum Data Analytics"
        ]
        self.systems_employees = [
            ("Asif Akram", "Project Manager"), ("Fatima Khan", "Solutions Architect"),
            ("Bilal Ahmed", "Technical Lead"), ("Sana Mahmood", "Business Analyst"),
            ("Omar Farooq", "Data Engineer"), ("Zainab Raza", "QA Manager"),
            ("Tariq Nadeem", "DevOps Specialist"), ("Ayesha Siddiqui", "UX Designer"),
            ("Kamran Ali", "Security Consultant"), ("Hina Sheikh", "Delivery Head")
        ]
        self.systems_offices = ["Karachi HQ", "Lahore Center", "Islamabad Branch", "Dubai Office", "Riyadh Center"]
        
    def _get_systems_employee(self) -> str:
        """Get random Systems Ltd employee with role"""
        name, role = random.choice(self.systems_employees)
        return f"{name} ({role})"
    
    def generate_project_postmortem(self, success_rate: float = 0.7) -> Dict[str, Any]:
        """Generate realistic project post-mortem with inconsistencies"""
        
        is_success = random.random() < success_rate
        project_type = random.choice(self.project_types)
        client = random.choice(self.companies)
        industry = random.choice(self.industries)
        tech_used = random.sample(self.systems_tech, k=2)
        project_code = f"SL-{random.randint(1000,9999)}-{datetime.now().year}"
        
        prompt = f"""Generate a realistic project post-mortem document for Systems Ltd's {project_type} project.

Client: {client} ({industry} industry)
Project Code: {project_code}
Systems Ltd Technologies Used: {", ".join(tech_used)}
Project Outcome: {'Successful with challenges' if is_success else 'Problematic with some wins'}

Make this document realistic by including:
- References to Systems Ltd methodologies like Agile@Scale or Delivery360
- Discussion of Systems Ltd's {tech_used[0]} platform capabilities
- Challenges with client's legacy systems integration
- Budget constraints specific to Pakistan/Middle East markets
- Multiple authors with conflicting perspectives
- Corporate jargon mixed with technical details
- "TBD" items and incomplete sections
- Both positive and negative feedback about Systems Ltd team
- Action items for Systems Ltd's COE teams
- Regional implementation challenges

Structure:
- Project Overview (Scope, Duration, Budget)
- Systems Ltd Team Composition
- Technical Implementation Challenges
- Client-Specific Customizations
- Lessons Learned (What Systems Ltd did well/poorly)
- Recommendations for Future Projects

Make it authentic with:
- References to Systems Ltd's Karachi/Lahore development centers
- Realistic project timelines (6-18 months typical)
- Budget discussions in USD/PKR/AED
- Client feedback about Systems Ltd's strengths/weaknesses"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "project_postmortem",
            "vendor": "Systems Ltd",
            "client": client,
            "industry": industry,
            "project_type": project_type,
            "project_code": project_code,
            "technologies": tech_used,
            "success": is_success,
            "created_date": (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat(),
            "authors": [self._get_systems_employee() for _ in range(random.randint(2, 4))],
            "office": random.choice(self.systems_offices)
        }
        
        return {
            "content": self._add_formatting_noise(content),
            "metadata": metadata
        }
    
    def generate_client_meeting_notes(self) -> Dict[str, Any]:
        """Generate messy meeting notes with incomplete information"""
        
        client = random.choice(self.companies)
        meeting_type = random.choice(["Requirements Workshop", "Solution Review", "Project Crisis Meeting", "UAT Sign-off", "Change Request Negotiation"])
        project_code = f"SL-{random.randint(1000,9999)}-{datetime.now().year}"
        
        prompt = f"""Generate realistic meeting notes for a {meeting_type} between Systems Ltd and {client}.

Project Code: {project_code}
Systems Ltd Attendees: {self._get_systems_employee()}, {self._get_systems_employee()}
Client Attendees: [CTO Representative], [Head of Operations], [IT Manager]

Make these notes authentic:
- Discuss integration with Systems Ltd's {random.choice(self.systems_tech)} platform
- Mention specific modules like "Collections Hub" or "Loan Origination"
- Include pricing discussions in USD with Pakistan/Middle East market context
- Reference regional compliance requirements (SBP, UAE Central Bank)
- Show disagreements about customization scope
- Note action items for Systems Ltd's Karachi development team
- Highlight client concerns about timeline delays
- Include technical debt discussions
- Capture follow-ups with Systems Ltd COE teams

Format:
- Incomplete sentences and rushed notes
- Questions marked as "TBD - check with Systems Ltd architect"
- Action items with ambiguous owners
- Technical debt items requiring Systems Ltd COE involvement
- Budget constraints specific to region
- References to Systems Ltd delivery centers (Karachi/Lahore)"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "meeting_notes",
            "vendor": "Systems Ltd",
            "client": client,
            "project_code": project_code,
            "meeting_type": meeting_type,
            "date": (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat(),
            "location": random.choice(["Virtual Teams", "Client Dubai Office", "Karachi HQ"]) + " | " + random.choice(self.systems_offices),
            "duration": f"{random.randint(30, 120)} minutes"
        }
        
        return {
            "content": self._add_meeting_noise(content),
            "metadata": metadata
        }
    
    def generate_technical_runbook(self) -> Dict[str, Any]:
        """Generate technical documentation with tribal knowledge"""
        
        system = random.choice(self.systems_tech)
        client = random.choice(self.companies)
        project_code = f"SL-{random.randint(1000,9999)}-{datetime.now().year}"
        
        prompt = f"""Generate a technical runbook for Systems Ltd's {system} deployed at {client}.

Project Code: {project_code}
Environment: {random.choice(['Production UAE', 'Staging KHI', 'DR Riyadh'])}
Key Contacts: {self._get_systems_employee()} (Systems Ltd Support), {random.choice(['Client Infrastructure Team', 'Client DBA Group'])}

Make this documentation realistic:
- Include references to Systems Ltd proprietary frameworks
- Document workarounds for client-specific legacy integrations
- Mention deprecated methods still used at client site
- Include emergency contacts at Systems Ltd Karachi office
- Note configuration specifics for Middle East markets
- Document known issues with SBP/UAE Central Bank compliance features
- Include tribal knowledge like "Contact Asif in Karachi for DB issues"
- Reference client-specific customizations
- List environment details with hardcoded credentials (redact properly)
- Include troubleshooting for regional network issues

Sections to cover:
- System Overview (with outdated diagrams)
- Deployment Procedures for UAE/KSA environments
- Client-Specific Configuration
- Integration Points with Client Legacy Systems
- Known Issues and Workarounds
- Systems Ltd Support Contacts (Karachi/Lahore offices)
- Change Management Process"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "technical_runbook",
            "vendor": "Systems Ltd",
            "system": system,
            "client": client,
            "project_code": project_code,
            "environment": random.choice(['Production', 'Staging', 'DR']),
            "last_updated": (datetime.now() - timedelta(days=random.randint(15, 200))).isoformat(),
            "version": f"{random.randint(1, 5)}.{random.randint(0, 9)}",
            "support_contact": self._get_systems_employee()
        }
        
        return {
            "content": self._add_technical_noise(content),
            "metadata": metadata
        }
    
    def generate_email_thread(self) -> Dict[str, Any]:
        """Generate email thread with escalating issues"""
        
        client = random.choice(self.companies)
        issue_type = random.choice(["Performance Issue", "Integration Problem", "User Training", "Scope Change", "Budget Discussion"])
        project_code = f"SL-{random.randint(1000,9999)}-{datetime.now().year}"
        tech_involved = random.choice(self.systems_tech)
        
        prompt = f"""Generate a realistic email thread about a {issue_type} at {client} involving Systems Ltd's {tech_involved}.

Project Code: {project_code}
Participants: 
  - Systems Ltd: {self._get_systems_employee()} (Technical Lead), {self._get_systems_employee()} (Account Manager)
  - Client: [IT Director], [Operations Manager]
  - Possibly: {self._get_systems_employee()} (Delivery Head)

Create 4-6 emails showing:
- Initial problem report from client
- Systems Ltd technical team response from Karachi office
- Escalation to Systems Ltd management
- Discussions about regional support coverage
- References to SLAs and contractual obligations
- Timezone challenges (PKT vs UAE/KSA time)
- Budget implications for additional work

Include realistic elements:
- Email signatures with Systems Ltd office locations
- Urgent requests during off-hours
- Forwarded internal Systems Ltd discussions
- References to previous projects with the client
- Technical details about {tech_involved} implementation
- Contractual terms specific to Middle East engagements
- Redacted financial information
- Action items for Systems Ltd Karachi team"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "email_thread",
            "vendor": "Systems Ltd",
            "client": client,
            "project_code": project_code,
            "issue_type": issue_type,
            "technology": tech_involved,
            "thread_length": random.randint(4, 8),
            "date_range": f"{random.randint(1, 14)} days",
            "participants": random.randint(3, 6)
        }
        
        return {
            "content": self._add_email_noise(content),
            "metadata": metadata
        }
    
    def generate_proposal_document(self, win_rate: float = 0.4) -> Dict[str, Any]:
        """Generate proposal document (won or lost)"""
        
        is_won = random.random() < win_rate
        client = random.choice(self.companies)
        project_type = random.choice(self.project_types)
        tech_proposed = random.choice(self.systems_tech)
        project_code = f"SL-PROP-{random.randint(100,999)}-{datetime.now().year}"
        
        prompt = f"""Generate a business proposal from Systems Ltd to {client} for {project_type}.

Project Code: {project_code}
Core Technology: {tech_proposed}
Result: This proposal was {'WON' if is_won else 'LOST'}

Make it realistic by including:
- Systems Ltd credentials in Banking/Telecom sectors
- Case studies from similar regional clients
- Implementation approach using Systems Ltd Delivery Framework
- Team structure based in Karachi/Lahore with client-site leads
- Pricing in USD with regional payment terms
- Compliance with local regulations (SBP, UAE Central Bank)
- Support model with Dubai/Riyadh coverage
- References to Systems Ltd partnerships (Oracle, SAP, AWS)

Add authentic flaws:
- Overly optimistic timelines
- Template sections with placeholder text
- Pricing inconsistencies in different sections
- Vague risk mitigation strategies
- Limited details on client-specific customization
- Generic technical diagrams
- Unclear division of responsibilities
- References to outdated Systems Ltd capabilities"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "proposal",
            "vendor": "Systems Ltd",
            "client": client,
            "project_type": project_type,
            "project_code": project_code,
            "technology": tech_proposed,
            "status": "won" if is_won else "lost",
            "value": f"${random.randint(250, 2000)}K",
            "created_date": (datetime.now() - timedelta(days=random.randint(60, 300))).isoformat(),
            "submitted_by": self._get_systems_employee()
        }
        
        return {
            "content": self._add_proposal_noise(content),
            "metadata": metadata
        }
    
    def _add_formatting_noise(self, content: str) -> str:
        """Add realistic formatting inconsistencies"""
        noise_items = [
            "\n[INTERNAL SYSTEMS LTD: Verify with COE team before sharing]\n",
            f"\n**CONFIDENTIAL - Systems Ltd {random.choice(['Karachi', 'Lahore', 'Dubai'])} Office Only**\n",
            "\n--- Reviewed by Systems Ltd PMO on {date} ---\n".format(date=datetime.now().strftime("%d/%m/%Y")),
            "\n[REF: Systems Ltd Delivery Framework Section 4.2]\n",
            "\n[ACTION: Escalate to Systems Ltd Delivery Head]\n"
        ]
        
        for _ in range(random.randint(1, 3)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(noise_items) + content[pos:]
        
        return content
    
    def _add_meeting_noise(self, content: str) -> str:
        """Add meeting-specific noise"""
        interruptions = [
            "\n[Audio unclear - poor connection to Karachi office]\n",
            "\n[Systems Ltd architect joined late due to timezone difference]\n",
            "\n[Discussing off-topic: Ramadan working hours]\n",
            "\n[ACTION: Schedule follow-up with Systems Ltd COE team]\n",
            "\n[CLIENT SENSITIVE: Redacted competitive information]\n"
        ]
        
        for _ in range(random.randint(2, 4)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(interruptions) + content[pos:]
        
        return content
    
    def _add_technical_noise(self, content: str) -> str:
        """Add technical documentation noise"""
        tech_notes = [
            "\n<!-- TODO: Update diagram from Systems Ltd repository -->\n",
            "\n[WARNING: This method deprecated in v3.2 - use only for UAE clients]\n",
            "\n**NOTE: Contact DevOps team at Karachi HQ for production access**\n",
            "\n```\n# Configuration for National Bank Pakistan deployment\n# Last validated: 2023-11-15 by Tariq\n```\n",
            "\n[LEGACY: Required for Dubai Islamic Bank integration]\n"
        ]
        
        for _ in range(random.randint(2, 5)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(tech_notes) + content[pos:]
        
        return content
    
    def _add_email_noise(self, content: str) -> str:
        """Add email-specific noise"""
        email_artifacts = [
            "\n[Sent from my iPhone - Systems Ltd Mobile]\n",
            "\n--- Forwarded to Systems Ltd Delivery Head ---\n",
            "\n[AUTO-REPLY: Karachi office closed for Eid holiday]\n",
            "\n**Systems Ltd Confidential - Do not forward**\n",
            "\n[Urgent: Response needed before EOD PKT]\n"
        ]
        
        for _ in range(random.randint(1, 2)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(email_artifacts) + content[pos:]
        
        return content
    
    def _add_proposal_noise(self, content: str) -> str:
        """Add proposal-specific noise"""
        proposal_notes = [
            "\n[SYSTEMS LTD INTERNAL DRAFT - NOT FOR CLIENT DISTRIBUTION]\n",
            "\n*Subject to final negotiation with client legal team*\n",
            "\n**Version 3.2 - Review comments from Delivery Head pending**\n",
            "\n--- Commercial terms valid for 45 days ---\n",
            "\n[WARNING: Scope gap identified during review]\n"
        ]
        
        for _ in range(random.randint(1, 3)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(proposal_notes) + content[pos:]
        
        return content
    
    def generate_document_set(self, total_docs: int = 50):
        """Generate a complete set of realistic documents"""
        
        print(f"Generating {total_docs} Systems Ltd documents...")
        
        document_types = [
            ("project_postmortem", self.generate_project_postmortem, 0.3),
            ("meeting_notes", self.generate_client_meeting_notes, 0.3),
            ("technical_runbook", self.generate_technical_runbook, 0.2),
            ("email_thread", self.generate_email_thread, 0.1),
            ("proposal", self.generate_proposal_document, 0.1)
        ]
        
        generated_docs = []
        
        for i in range(total_docs):
            # Select document type based on weights
            rand = random.random()
            cumulative = 0
            
            for doc_type, generator_func, weight in document_types:
                cumulative += weight
                if rand <= cumulative:
                    doc = generator_func()
                    doc["metadata"]["doc_id"] = f"SL-{doc_type}-{uuid.uuid4().hex[:6]}"
                    
                    # Save to file
                    filename = f"{doc['metadata']['doc_id']}.txt"
                    filepath = os.path.join(self.output_dir, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(f"=== SYSTEMS LTD DOCUMENT ===\n")
                        f.write(f"=== METADATA ===\n{json.dumps(doc['metadata'], indent=2)}\n\n")
                        f.write(f"=== CONTENT ===\n{doc['content']}")
                    
                    generated_docs.append({
                        "filename": filename,
                        "type": doc_type,
                        "metadata": doc["metadata"]
                    })
                    
                    print(f"Generated {i+1}/{total_docs}: {doc_type} | Project {doc['metadata'].get('project_code','')}")
                    break
        
        # Save index
        with open(os.path.join(self.output_dir, "document_index.json"), 'w') as f:
            json.dump(generated_docs, f, indent=2)
        
        print(f"\nGenerated {len(generated_docs)} Systems Ltd documents in '{self.output_dir}'")
        return generated_docs

def generate_mixed_knowledge_base():
    """Generate a mixed knowledge base with structured and unstructured docs"""
    
    generator = DocumentGenerator()
    
    # Generate unstructured documents
    docs = generator.generate_document_set(30)
    
    # Create document type summary
    type_counts = {}
    for doc in docs:
        doc_type = doc['type']
        type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
    
    print(f"\nDocument Type Distribution:")
    for doc_type, count in type_counts.items():
        print(f"  {doc_type}: {count}")
    
    return docs

if __name__ == "__main__":
    generate_mixed_knowledge_base()