""" 
Augmented Document Generator for Systems Ltd Projects
Creates messy, unstructured documents based on real project data
"""

import os
import json
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
import uuid
from agent.services.llm_service import get_llm

class ProjectDocumentGenerator:
    """Generates realistic, messy documents for Systems Ltd projects"""
    
    def __init__(self, output_dir: str = "project_docs"):
        self.output_dir = output_dir
        self.llm = get_llm("gemini-2.5-flash-lite")
        os.makedirs(output_dir, exist_ok=True)
        
        # Systems Ltd-specific data
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
    
    def _inject_project_issues(self, project: Dict) -> str:
        """Create problem statement based on project description"""
        issues = []
        description = project["description"].lower()
        
        if "gap" in description or "incomplete" in description:
            issues.append("integration gaps")
        if "delay" in description or "overlap" in description:
            issues.append("timeline challenges")
        if "bug" in description or "issue" in description:
            issues.append("technical defects")
        if "adoption" in description or "acceptance" in description:
            issues.append("user adoption problems")
        if "legacy" in description or "old system" in description:
            issues.append("legacy system constraints")
        if "vague" in description or "unclear" in description:
            issues.append("requirements ambiguity")
            
        return ", ".join(issues) if issues else "scope management challenges"

    def generate_project_postmortem(self, project_name: str, project: Dict) -> Dict[str, Any]:
        """Generate messy project post-mortem with inconsistencies"""
        client = project.get("client", "Confidential Client")
        year = project.get("year", datetime.now().year - random.randint(0, 3))
        issues = self._inject_project_issues(project)
        project_code = f"SL-{random.randint(1000,9999)}-{year}"
        
        prompt = f"""Generate a realistic project post-mortem document for Systems Ltd's project: {project_name}

Client: {client} ({project['industry']} industry)
Project Code: {project_code}
Location: {project['location']}
Year: {year}
Key Issues: {issues}

Project Description: {project['description']}
Tech Stack: {project.get('tech_stack', 'Not fully documented')}

Make this document realistic by including:
- Conflicting accounts of what went wrong
- Blame-shifting between teams
- Incomplete metrics and KPIs
- Corporate jargon obscuring real issues
- "TBD" items that were never resolved
- Both positive spin and harsh criticism
- Action items with no clear owners
- Budget overruns with vague justifications

Structure the document messily with:
- Inconsistent section headings
- Missing data where you'd expect numbers
- Contradictory assessments from different team members
- Overly optimistic "lessons learned" vs. harsh reality
- Recommendations that don't address core problems"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "project_postmortem",
            "project_name": project_name,
            "vendor": "Systems Ltd",
            "client": client,
            "industry": project["industry"],
            "location": project["location"],
            "year": year,
            "project_code": project_code,
            "issues": issues,
            "created_date": (datetime.now() - timedelta(days=random.randint(60, 730))).isoformat(),
            "authors": [self._get_systems_employee() for _ in range(random.randint(2, 4))],
            "office": random.choice(self.systems_offices)
        }
        
        return {
            "content": self._add_postmortem_noise(content, project),
            "metadata": metadata
        }
    
    def generate_technical_runbook(self, project_name: str, project: Dict) -> Dict[str, Any]:
        """Generate incomplete technical documentation"""
        client = project.get("client", "Confidential Client")
        tech_stack = project.get("tech_stack", "Various technologies")
        year = project.get("year", datetime.now().year - random.randint(0, 2))
        project_code = f"SL-{random.randint(1000,9999)}-{year}"
        issues = self._inject_project_issues(project)
        
        prompt = f"""Generate a technical runbook for Systems Ltd's project: {project_name}

Client: {client}
Project Code: {project_code}
Environment: {random.choice(['Production', 'Staging', 'DR'])}
Key Issues: {issues}

Project Description: {project['description']}
Tech Stack: {tech_stack}

Make this documentation realistic by including:
- Outdated sections mixed with current information
- "TODO" items that were never completed
- Hardcoded values from development phase
- Environment-specific details that don't match production
- Troubleshooting steps that reference people who left
- Code snippets with inconsistent formatting
- Missing diagrams and architecture references
- Assumptions that are no longer valid
- Emergency procedures with gaps
- Contact information that's outdated

Structure haphazardly with:
- Missing sections where you'd expect critical info
- Overly detailed trivial sections
- Tribal knowledge like "See Asif for DB issues"
- Version mismatches between components
- Deprecated methods still listed as primary"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "technical_runbook",
            "project_name": project_name,
            "vendor": "Systems Ltd",
            "client": client,
            "tech_stack": tech_stack,
            "project_code": project_code,
            "environment": random.choice(['Production', 'Staging', 'DR']),
            "last_updated": (datetime.now() - timedelta(days=random.randint(100, 500))).isoformat(),
            "version": f"{random.randint(1, 3)}.{random.randint(0, 5)}",
            "support_contact": self._get_systems_employee()
        }
        
        return {
            "content": self._add_technical_noise(content, project),
            "metadata": metadata
        }
    
    def generate_meeting_notes(self, project_name: str, project: Dict) -> Dict[str, Any]:
        """Generate messy meeting notes with incomplete information"""
        client = project.get("client", "Confidential Client")
        year = project.get("year", datetime.now().year - random.randint(0, 1))
        project_code = f"SL-{random.randint(1000,9999)}-{year}"
        issues = self._inject_project_issues(project)
        
        prompt = f"""Generate realistic meeting notes for a crisis/status meeting about: {project_name}

Client: {client}
Project Code: {project_code}
Key Issues: {issues}

Project Description: {project['description']}

Make these notes feel authentic with:
- Half-finished sentences and unclear action items
- Arguments between team members
- Technical details that don't match other docs
- Budget concerns that are vaguely referenced
- Decisions that get walked back later
- Attendance issues and late arrivals
- Off-topic discussions that derail meeting
- Next steps with no owners or deadlines

Include:
- Disorganized bullet points
- Questions marked "FOLLOW UP" that never were
- Contradictory statements from different participants
- Sensitive topics marked [CLIENT CONFIDENTIAL]
- Technical debt that's acknowledged but not addressed
- References to missing documentation"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "meeting_notes",
            "project_name": project_name,
            "vendor": "Systems Ltd",
            "client": client,
            "project_code": project_code,
            "meeting_type": random.choice(["Crisis Meeting", "Escalation Discussion", "Recovery Planning"]),
            "date": (datetime.now() - timedelta(days=random.randint(10, 180))).isoformat(),
            "location": random.choice(["Virtual Teams", "Client Office", "Karachi HQ"]),
            "duration": f"{random.randint(45, 120)} minutes"
        }
        
        return {
            "content": self._add_meeting_noise(content),
            "metadata": metadata
        }
    
    def generate_email_thread(self, project_name: str, project: Dict) -> Dict[str, Any]:
        """Generate email thread with escalating issues"""
        client = project.get("client", "Confidential Client")
        year = project.get("year", datetime.now().year - random.randint(0, 1))
        project_code = f"SL-{random.randint(1000,9999)}-{year}"
        issues = self._inject_project_issues(project)
        
        prompt = f"""Generate a realistic email thread about escalating issues with: {project_name}

Client: {client}
Project Code: {project_code}
Key Issues: {issues}

Project Description: {project['description']}

Create 5-7 emails showing:
- Initial problem report from client
- Defensive response from delivery team
- Escalation to management
- Conflicting technical assessments
- Blame shifting between teams
- Vague commitments to resolve
- Eventual unsatisfactory resolution

Include:
- Missing attachments that were promised
- Auto-replies interrupting the thread
- Timezone confusion (PKT vs client time)
- Sensitive information accidentally included
- Forwarded messages with missing context
- Tone that becomes increasingly frustrated
- Corporate jargon masking real problems"""

        content = self.llm.invoke(prompt).content
        
        metadata = {
            "document_type": "email_thread",
            "project_name": project_name,
            "vendor": "Systems Ltd",
            "client": client,
            "project_code": project_code,
            "issue_type": issues.split(",")[0] if issues else "Project Issues",
            "thread_length": random.randint(5, 8),
            "date_range": f"{random.randint(2, 10)} days",
            "participants": random.randint(4, 7)
        }
        
        return {
            "content": self._add_email_noise(content),
            "metadata": metadata
        }
    
    def _add_postmortem_noise(self, content: str, project: Dict) -> str:
        """Add project-specific noise to postmortem"""
        noise_items = [
            f"\n[INTERNAL: Do not share with {project.get('client', 'client')}]\n",
            "\n**SECTION INCOMPLETE - PM LEFT COMPANY**\n",
            "\n--- Contradicts Jira tickets from {random.choice(['Dev', 'QA'])} team ---\n",
            f"\n[NOTE: Actual benefits differ from promised {', '.join(project.get('benefits', []))}]\n",
            "\n[ACTION ITEM: Never assigned or completed]\n"
        ]
        
        for _ in range(random.randint(2, 4)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(noise_items) + content[pos:]
        
        # Add missing metrics note
        if not project.get("metrics"):
            metrics_note = "\n[PERFORMANCE METRICS: Never established baseline - ROI unmeasurable]\n"
            content = content.replace("Key Metrics:", metrics_note + "Key Metrics:", 1)
        
        return content
    
    def _add_technical_noise(self, content: str, project: Dict) -> str:
        """Add technical documentation noise"""
        tech_stack = project.get("tech_stack", "")
        noise_items = [
            "\n<!-- TODO: Update diagram from outdated version -->\n",
            "\n[WARNING: Configuration differs from production environment]\n",
            "\n**SECTION DEPRECATED - NEW SYSTEM INCOMPATIBLE**\n",
            f"\n```\n# {tech_stack.split(',')[0]} config - may be outdated\n# Last verified: unknown\n```\n",
            "\n[LEGACY: Required for {client} integration]\n".format(client=project.get("client", "client")),
            "\n[SECURITY WARNING: Hardcoded credentials - change in production]\n"
        ]
        
        for _ in range(random.randint(3, 5)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(noise_items) + content[pos:]
        
        return content
    
    def _add_meeting_noise(self, content: str) -> str:
        """Add meeting-specific noise"""
        interruptions = [
            "\n[Audio cut out - missed 2 minutes]\n",
            "\n[Side discussion about unrelated budget issues]\n",
            "\n[ACTION ITEM: Unclear owner - never followed up]\n",
            "\n[Attendee left early for another meeting]\n",
            "\n[Important decision made without key stakeholder]\n"
        ]
        
        for _ in range(random.randint(3, 5)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(interruptions) + content[pos:]
        
        return content
    
    def _add_email_noise(self, content: str) -> str:
        """Add email-specific noise"""
        email_artifacts = [
            "\n[Sent from mobile - please excuse typos]\n",
            "\n--- Legal disclaimer automatically appended ---\n",
            "\n[Attachment: missing_spec.docx NOT FOUND]\n",
            "\n[Urgent: Response needed before COB tomorrow]\n",
            "\n[Auto-reply: Recipient on leave until next month]\n"
        ]
        
        for _ in range(random.randint(2, 4)):
            pos = random.randint(0, len(content))
            content = content[:pos] + random.choice(email_artifacts) + content[pos:]
        
        return content
    
    def generate_project_documents(self, project_name: str, project: Dict) -> List[Dict]:
        """Generate full document set for a single project"""
        print(f"Generating documents for: {project_name}")
        
        documents = []
        
        # Always generate these documents
        documents.append(self.generate_project_postmortem(project_name, project))
        documents.append(self.generate_meeting_notes(project_name, project))
        documents.append(self.generate_email_thread(project_name, project))
        
        # Only generate runbook if tech stack is available
        if project.get("tech_stack"):
            documents.append(self.generate_technical_runbook(project_name, project))
        
        return documents
    
    def generate_all_project_docs(self, projects_data: Dict[str, Dict]) -> List[Dict]:
        """Generate documents for all projects"""
        print(f"Generating documents for {len(projects_data)} projects...")
        
        all_documents = []
        
        for project_name, project_data in projects_data.items():
            try:
                project_docs = self.generate_project_documents(project_name, project_data)
                all_documents.extend(project_docs)
                
                # Save project documents immediately
                for doc in project_docs:
                    doc_id = f"SL-{doc['metadata']['document_type']}-{uuid.uuid4().hex[:6]}"
                    filename = f"{doc_id}.txt"
                    filepath = os.path.join(self.output_dir, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(f"=== SYSTEMS LTD PROJECT DOCUMENT ===\n")
                        f.write(f"Project: {project_name}\n")
                        f.write(f"=== METADATA ===\n{json.dumps(doc['metadata'], indent=2)}\n\n")
                        f.write(f"=== CONTENT ===\n{doc['content']}")
                    
                    # Add to index
                    doc["filename"] = filename
            except Exception as e:
                print(f"Error generating documents for {project_name}: {str(e)}")
        
        # Save master index
        index_path = os.path.join(self.output_dir, "project_document_index.json")
        with open(index_path, 'w') as f:
            json.dump([{
                "project": project_name,
                "filename": doc["filename"],
                "type": doc["metadata"]["document_type"],
                "client": doc["metadata"].get("client", ""),
                "year": doc["metadata"].get("year", "")
            } for doc in all_documents], f, indent=2)
        
        print(f"\nGenerated {len(all_documents)} documents across {len(projects_data)} projects")
        print(f"Documents saved to: {self.output_dir}")
        return all_documents

# Example project data
PROJECTS_DATA = {
  "Aga Khan University Hospital OR Management": {
    "client": "Aga Khan University Hospital",
    "industry": "Healthcare",
    "location": "Karachi, Pakistan",
    "year": 2023,
    "description": "Tablet-based Operating Room scheduling and checklist system. Staff coordination dashboard, shift reporting, nurses' notifications. Implementation overlapped with existing legacy system, some integration gaps noted. User acceptance training delivered but full adoption not confirmed.",
    "benefits": ["efficiency", "data accuracy"],
    "metrics": None,
    "tech_stack": "Android tablets, web dashboards (possibly Angular), backend Java/.NET unclear"
  },
  "Dynamics 365 ERP Rollout for Outfitters": {
    "client": "Outfitters",
    "industry": "Retail",
    "location": "Pakistan",
    "year": 2022,
    "description": "End-to-end rollout of Microsoft Dynamics 365 ERP for retail, finance and e-commerce integration. Middleware connectors built in-house. 7‑month implementation; some modules went live earlier than planned. Internal delays due to vendor coordination issues mentioned.",
    "benefits": ["timely decision making", "process unification", "reduced manual reporting"],
    "metrics": None,
    "tech_stack": "Dynamics 365, SQL Server, middleware (custom APIs), front-end UI unclear"
  },
  "Allied Bank RPA Automation": {
    "client": "Allied Bank",
    "industry": "Banking",
    "location": "Pakistan",
    "year": 2022,
    "description": "Built bots using Automation Anywhere to automate account opening, password reset workflows, and basic customer service requests. Delivered within 3 months, but lacked detailed baseline metrics. Internal user feedback: fewer manual errors, though no ROI numbers made public.",
    "benefits": ["operational efficiency", "reduced manual workload", "faster turnaround"],
    "metrics": {"duration_months": 3},
    "tech_stack": "Automation Anywhere, VB scripting, some API integration"
  },
  "Islamic Bank API Platform": {
    "client": "Islamic Bank of Pakistan",
    "industry": "Islamic Banking",
    "location": "Pakistan",
    "year": None,
    "description": "Implemented API management platform to modernize old core banking backend, enabling mobile onboarding and third-party apps. Vague on exact architecture. Some concerns raised internally about latency and legacy-system constraints.",
    "benefits": ["modern onboarding", "digital access"],
    "metrics": None,
    "tech_stack": ""
  },
  "Hami AI‑assistant Platform": {
    "client": "Boston Health AI / Hami",
    "industry": "Healthcare Tech",
    "location": "Global",
    "year": 2024,
    "description": "Partnered to launch 'Hami', an AI-powered physician assistant mobile/web app. Includes chat-based recommendation engine, symptom triage, and physician availability suggestions. Initial user reception good but some bugs reported in early build.",
    "benefits": ["patient engagement", "AI-driven triage", "physician intake assistance"],
    "metrics": {"user_base_estimated": "tens of thousands"},
    "tech_stack": "React Native (mobile), React web, Node.js backend, AI/ML (Python?), unclear cloud provider"
  },
  "Unnamed Gulf Telco Self‑Care Portal": {
    "client": "Unnamed Gulf Telco",
    "industry": "Telecom",
    "location": "Middle East",
    "year": 2023,
    "description": "Launched mobile + web self‑care portal integrated with billing backend. Reduced support calls. Some post-launch stability issues reported initially; remedied in patch releases",
    "benefits": ["reduced call‑center volumes", "customer empowerment"],
    "metrics": {"launch_quick": True, "roi": "est positive"},
    "tech_stack": "Angular frontend, Java/Spring backend, REST APIs, Oracle billing system integration"
  },
  "Manufacturing ERP Integration": {
    "client": None,
    "industry": "Manufacturing",
    "location": "Pakistan",
    "year": 2021,
    "description": "Generic ERP integration project synchronizing inventory, finance, and supply modules. No client name, vague notes on phase cancellation midway. Possibly internal PoC.",
    "benefits": [],
    "metrics": None,
    "tech_stack": "Possibly SAP/Fiori or custom .NET solution—details missing"
  },
  "Provincial Citizen Services Portal": {
    "client": "Sindh Provincial Department",
    "industry": "Government",
    "location": "Sindh, Pakistan",
    "year": 2020,
    "description": "Online public services portal allowing citizens to request permits, file complaints, track application status. Description vague. No usage metrics. Some modules listed but UX feedback not recorded.",
    "benefits": ["citizen engagement"],
    "metrics": {"users_monthly": None},
    "tech_stack": "PHP/LAMP or .NET unspecified, maybe MySQL, front-end basic HTML/CSS"
  },
  "Data Warehouse for GCC Bank": {
    "client": "Unnamed GCC Bank",
    "industry": "Banking",
    "location": "Middle East",
    "year": 2022,
    "description": "Designed and built a data warehouse and analytics engine focused on credit risk reporting. Reduced data latency from overnight to near-real-time, but dashboards were later only partially adopted by users.",
    "benefits": ["better risk insight", "faster reporting"],
    "metrics": {"data_latency": "reduced by hours"},
    "tech_stack": "ETL (Informatica?), SQL Server DW, Tableau/Power BI front-end, some Python scripts"
  },
  "Logistics Mobile App Prototype": {
    "client": "Local Logistics Co.",
    "industry": "Logistics",
    "location": "Pakistan",
    "year": None,
    "description": "Prototype for LTL and FTL carrier. Features for drivers (routes, delivery status) and dispatchers (tracking). Low adoption; downloads under 1,000. Project paused due to funding cutoff.",
    "benefits": ["tracking", "route optimization"],
    "metrics": {"downloads": "<1,000"},
    "tech_stack": "Flutter mobile, Firebase backend, Google Maps APIs"
  }
}

if __name__ == "__main__":
    # Initialize generator
    generator = ProjectDocumentGenerator(output_dir="project_docs")
    
    # Generate documents for all projects
    generator.generate_all_project_docs(PROJECTS_DATA)