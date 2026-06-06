import json
import logging
import re
import os
from typing import List, Dict, Any, Optional
import google.generativeai as genai

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("flowarchitect-agents")

class BaseAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.is_live = False
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.is_live = True
                logger.info("Gemini API configured successfully. Operating in LIVE mode.")
            except Exception as e:
                logger.error(f"Error configuring Gemini API: {e}. Falling back to SIMULATION mode.")
        else:
            logger.info("No Gemini API key supplied. Operating in SIMULATION mode.")

    def _call_gemini(self, system_instruction: str, prompt: str, schema: Optional[Dict[str, Any]] = None) -> str:
        if not self.is_live:
            raise RuntimeError("Gemini is not configured.")
        try:
            # Using recommended model
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_instruction
            )
            
            generation_config = {}
            if schema:
                generation_config = {
                    "response_mime_type": "application/json",
                    "response_schema": schema
                }
                
            response = model.generate_content(prompt, generation_config=generation_config)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}. Raising error to trigger fallback.")
            raise e

class DiscoveryAgent(BaseAgent):
    """
    Discovery Agent:
    - Analyzes existing conversation history.
    - Determines which data points are missing (Industry, Team Size, Channels, CRM, Repetitive Tasks, Pain Points).
    - Asks adaptive, industry-aware questions.
    """
    
    DISCOVERY_QUESTIONS = [
        "What industry is your business in and what is the company name?",
        "How many employees work at your company, and what is your general role?",
        "How do customers contact you (e.g. Website, WhatsApp, Email, Phone, Social Media)?",
        "How do you manage leads and sales (e.g. CRM, Excel, or manually)?",
        "How do you handle customer support tickets or inquiries?",
        "What repetitive tasks consume the most time for your team daily?",
        "Which software tools do you currently use for operations (e.g. Google Workspace, Slack, Shopify, HubSpot)?",
        "What are your biggest operational challenges or blockers right now?"
    ]

    def get_next_question(self, messages: List[Dict[str, str]], business_context: Dict[str, Any], step: int) -> Dict[str, Any]:
        # In Live Mode, we can use Gemini to draft a highly contextualized follow-up question
        if self.is_live and step > 0:
            try:
                history_str = "\n".join([f"{m['sender']}: {m['content']}" for m in messages])
                system_prompt = (
                    "You are the Discovery Agent for FlowArchitect AI. Your job is to conduct an interactive business consulting interview.\n"
                    "Analyze the conversation history. Formulate the next single question to uncover details about their business operations, "
                    "focusing on manual work, customer support, sales, tools, or bottlenecks. Keep the question professional, friendly, "
                    "and highly specific based on the industry they mentioned previously."
                )
                prompt = f"Conversation History:\n{history_str}\n\nDraft the next follow-up question:"
                ai_question = self._call_gemini(system_prompt, prompt)
                return {
                    "content": ai_question.strip(),
                    "agent_name": "DiscoveryAgent",
                    "step": step
                }
            except Exception:
                pass # Fallback to preset questions if API call fails
                
        # Heuristic/Fallback to preset questions
        if step < len(self.DISCOVERY_QUESTIONS):
            question = self.DISCOVERY_QUESTIONS[step]
            # Adapt the question if we have industry info
            if business_context.get("industry") and step > 1:
                ind = business_context["industry"].lower()
                question = question.replace("your team", f"your {ind} team").replace("your company", f"your {ind} business")
            return {
                "content": question,
                "agent_name": "DiscoveryAgent",
                "step": step
            }
        else:
            return {
                "content": "Thank you! I have gathered enough information to compile your business profile. Let's run the Analysis Agent to map out your automation roadmap.",
                "agent_name": "DiscoveryAgent",
                "step": step,
                "completed": True
            }

    def validate_user_response(self, question: str, response: str) -> Dict[str, Any]:
        """
        Validates if the user's reply is a relevant and safe answer to the question.
        Returns:
            {"valid": bool, "reason": str}
        """
        clean_resp = response.strip()
        if not clean_resp:
            return {"valid": False, "reason": "Response cannot be empty."}
            
        # Basic length check
        if len(clean_resp) < 2:
            return {"valid": False, "reason": "Please provide a more descriptive answer (at least 2 characters)."}
            
        # Check for keyboard smash/gibberish (e.g., asdf, qwer, zxcv, sdfsdf)
        if re.match(r'^[asdfghjklqwertyuiopzxcvbnm\s]{4,}$', clean_resp.lower()):
            if clean_resp.lower() in ["asdf", "sdfg", "asdfasdf", "qwer", "qwerty", "zxcv", "zxcvbnm", "aaaa", "bbbb"]:
                return {"valid": False, "reason": "Please enter a valid response rather than placeholder characters."}

        # Check for generic greetings or words that don't answer the question
        greetings = {"hi", "hello", "hey", "test", "testing", "yo", "sup", "ok", "okay", "fine"}
        if clean_resp.lower() in greetings:
            return {"valid": False, "reason": "That greeting doesn't seem to answer the question. Please provide operational details."}

        if self.is_live:
            try:
                system_prompt = (
                    "You are the Discovery Agent validator for FlowArchitect AI. Your job is to check if the user's reply "
                    "is a relevant and constructive answer to the consultation question asked.\n"
                    "If the answer is a greeting (e.g. 'hello'), gibberish, spam, or completely off-topic, mark it as invalid.\n"
                    "If it is a brief but valid answer (e.g. '5 employees' or 'no CRM used' or '10 staff'), mark it as valid.\n"
                    "Return a JSON object with: \n"
                    "1. valid: boolean\n"
                    "2. reason: string (brief explanation of what is missing or incorrect if invalid, or empty if valid)"
                )
                schema = {
                    "type": "OBJECT",
                    "properties": {
                        "valid": {"type": "BOOLEAN"},
                        "reason": {"type": "STRING"}
                    },
                    "required": ["valid", "reason"]
                }
                prompt = f"Question asked: \"{question}\"\nUser Response: \"{clean_resp}\"\n\nValidate this response:"
                res = self._call_gemini(system_prompt, prompt, schema=schema)
                return json.loads(res)
            except Exception as e:
                logger.error(f"Live validation failed: {e}. Falling back to default heuristics.")
                
        # Heuristic validation when simulation mode is active or live API call fails
        q_lower = question.lower()
        r_lower = clean_resp.lower()

        # Step 0: Company Name & Industry
        if "industry" in q_lower or "company name" in q_lower:
            block_words = {"none", "nothing", "no", "yes", "dunno", "why", "na", "n/a"}
            if r_lower in block_words:
                return {"valid": False, "reason": "Please state a valid company name and the industry you operate in."}
            if len(clean_resp) < 3:
                return {"valid": False, "reason": "Please provide a valid company name or industry (at least 3 characters)."}

        # Step 1: Employees & Role
        elif "employees" in q_lower or "team size" in q_lower or "how many employees" in q_lower:
            indicators = [
                "founder", "ceo", "owner", "manager", "admin", "agent", "director", "staff", "employee", "people",
                "myself", "me", "alone", "solo", "team", "contractor", "intern", "developer", "designer", "consultant"
            ]
            has_number = any(char.isdigit() for char in r_lower)
            has_indicator = any(word in r_lower for word in indicators)
            number_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "zero", "many", "few", "some", "several", "no"]
            has_num_word = any(word in r_lower for word in number_words)
            
            if not (has_number or has_indicator or has_num_word):
                return {
                    "valid": False,
                    "reason": "Please state the number of employees (e.g., '5', 'solo', 'none') and your role (e.g., 'founder', 'manager')."
                }

        # Step 2: Customer Contact Channels
        elif "customers contact you" in q_lower or "channels" in q_lower:
            channels = [
                "website", "site", "web", "whatsapp", "email", "mail", "phone", "call", "social", "instagram", "ig",
                "facebook", "fb", "linkedin", "dm", "chat", "message", "text", "walk-in", "store", "person", "online",
                "form", "portal", "none", "nothing"
            ]
            has_channel = any(word in r_lower for word in channels)
            if not has_channel:
                return {
                    "valid": False,
                    "reason": "Please specify how customers contact you (e.g., 'email', 'website form', 'WhatsApp', or 'phone')."
                }

        # Step 3: Sales / CRM Tooling
        elif "leads and sales" in q_lower or "crm" in q_lower:
            crm_words = [
                "crm", "excel", "sheet", "google sheet", "manual", "hubspot", "salesforce", "notion", "trello",
                "notebook", "paper", "email", "chat", "none", "nothing", "no tool", "zoho", "pipedrive", "monday"
            ]
            has_crm = any(word in r_lower for word in crm_words)
            if not has_crm:
                return {
                    "valid": False,
                    "reason": "Please mention how you track leads or sales (e.g., 'Excel sheets', 'HubSpot CRM', 'manually', or 'none')."
                }

        # Step 4: Customer Support Inquiries
        elif "support tickets" in q_lower or "customer support" in q_lower:
            support_words = [
                "email", "phone", "whatsapp", "zendesk", "freshdesk", "intercom", "manual", "helpdesk", "ticket",
                "chat", "none", "nothing", "don't have", "do not have", "no support"
            ]
            has_support = any(word in r_lower for word in support_words)
            if not has_support:
                return {
                    "valid": False,
                    "reason": "Please describe how you handle customer inquiries (e.g., 'manually via email', 'freshdesk', 'we don't have support tickets')."
                }

        # Step 5: Repetitive daily tasks
        elif "repetitive" in q_lower or "consume the most time" in q_lower:
            task_words = [
                "entry", "data", "scheduling", "booking", "copy", "paste", "sending", "follow", "invoice", "billing",
                "report", "email", "chat", "phone", "calls", "meeting", "check", "verify", "none", "nothing", "manual"
            ]
            has_task = any(word in r_lower for word in task_words)
            word_count = len(r_lower.split())
            if not (has_task or word_count >= 2):
                return {
                    "valid": False,
                    "reason": "Please describe a repetitive task (e.g., 'data entry', 'manually sending emails', or state 'none')."
                }

        # Step 6: Software stack
        elif "software tools" in q_lower or "currently use for operations" in q_lower:
            stack_words = [
                "google", "workspace", "gmail", "slack", "shopify", "hubspot", "excel", "notion", "trello", "zoom",
                "activecampaign", "mailchimp", "whatsapp", "drive", "none", "nothing", "word", "office", "make", "zapier"
            ]
            has_stack = any(word in r_lower for word in stack_words)
            if not has_stack:
                return {
                    "valid": False,
                    "reason": "Please name some of the software tools you use daily (e.g., 'Gmail, Excel', 'Slack', or state 'none')."
                }

        # Step 7: Challenges / blockers
        elif "challenges" in q_lower or "blockers" in q_lower:
            challenge_words = [
                "delay", "time", "loss", "cost", "manual", "slow", "growth", "leads", "none", "nothing", "hard", "difficult",
                "tracking", "follow", "errors", "mistakes", "scale", "scaling", "hiring", "money"
            ]
            has_challenge = any(word in r_lower for word in challenge_words)
            word_count = len(r_lower.split())
            if not (has_challenge or word_count >= 2):
                return {
                    "valid": False,
                    "reason": "Please describe your biggest operational challenge (e.g., 'leads slip through cracks', 'slow manual reports', or state 'none')."
                }

        return {"valid": True, "reason": ""}



class AnalysisAgent(BaseAgent):
    """
    Analysis Agent:
    - Identifies operational bottlenecks.
    - Detects manual inefficiencies.
    - Calculates scores (0-100) for Customer Support, Sales, Operations, Marketing, and Analytics.
    """
    
    def analyze(self, chat_history: List[Dict[str, str]], context: Dict[str, Any]) -> Dict[str, Any]:
        history_str = "\n".join([f"{m['sender']}: {m['content']}" for m in chat_history])
        
        if self.is_live:
            try:
                system_prompt = (
                    "You are the Analysis Agent. Analyze the interview transcripts of this business.\n"
                    "Provide a JSON object containing:\n"
                    "1. industry: The main business industry\n"
                    "2. company_name: Name of company (or default if unknown)\n"
                    "3. company_size: Size description\n"
                    "4. business_summary: {key_processes: list, existing_tools: string, operational_bottlenecks: string}\n"
                    "5. pain_points: {manual_work: string, customer_communication: string, sales_inefficiencies: string, support_inefficiencies: string, reporting_challenges: string}\n"
                    "6. readiness_scores: {Customer_Support: int, Sales: int, Operations: int, Marketing: int, Analytics: int}"
                )
                schema = {
                    "type": "OBJECT",
                    "properties": {
                        "industry": {"type": "STRING"},
                        "company_name": {"type": "STRING"},
                        "company_size": {"type": "STRING"},
                        "business_summary": {
                            "type": "OBJECT",
                            "properties": {
                                "key_processes": {"type": "ARRAY", "items": {"type": "STRING"}},
                                "existing_tools": {"type": "STRING"},
                                "operational_bottlenecks": {"type": "STRING"}
                            },
                            "required": ["key_processes", "existing_tools", "operational_bottlenecks"]
                        },
                        "pain_points": {
                            "type": "OBJECT",
                            "properties": {
                                "manual_work": {"type": "STRING"},
                                "customer_communication": {"type": "STRING"},
                                "sales_inefficiencies": {"type": "STRING"},
                                "support_inefficiencies": {"type": "STRING"},
                                "reporting_challenges": {"type": "STRING"}
                            },
                            "required": ["manual_work", "customer_communication", "sales_inefficiencies", "support_inefficiencies", "reporting_challenges"]
                        },
                        "readiness_scores": {
                            "type": "OBJECT",
                            "properties": {
                                "Customer_Support": {"type": "INTEGER"},
                                "Sales": {"type": "INTEGER"},
                                "Operations": {"type": "INTEGER"},
                                "Marketing": {"type": "INTEGER"},
                                "Analytics": {"type": "INTEGER"}
                            },
                            "required": ["Customer_Support", "Sales", "Operations", "Marketing", "Analytics"]
                        }
                    },
                    "required": ["industry", "company_name", "company_size", "business_summary", "pain_points", "readiness_scores"]
                }
                
                result_str = self._call_gemini(system_prompt, f"Interview logs:\n{history_str}", schema=schema)
                parsed = json.loads(result_str)
                # Normalize keys for readiness scores
                scores = parsed["readiness_scores"]
                parsed["readiness_scores"] = {
                    "Customer Support": scores.get("Customer_Support", 50),
                    "Sales": scores.get("Sales", 50),
                    "Operations": scores.get("Operations", 50),
                    "Marketing": scores.get("Marketing", 50),
                    "Analytics": scores.get("Analytics", 50)
                }
                return parsed
            except Exception as e:
                logger.error(f"Analysis Agent Live call failed: {e}. Falling back to simulation.")
                
        # Heuristic Fallback
        industry = context.get("industry", "Retail")
        name = context.get("company_name", f"{industry} Co")
        size = context.get("company_size", "5-20 employees")
        
        # Analyze key words in chat history to customize bottlenecks
        chat_text_lower = history_str.lower()
        
        manual_work_found = "Manual data entries into tracking spreadsheets and scheduling logs."
        if "spreadsheet" in chat_text_lower or "excel" in chat_text_lower:
            manual_work_found = "Updating Excel spreadsheets and transferring order/patient details manually."
        elif "call" in chat_text_lower or "phone" in chat_text_lower:
            manual_work_found = "Answering phone calls and booking appointments manually."
            
        comm_issue = "Slow responses to customer inquiries due to lack of automated text templates."
        if "whatsapp" in chat_text_lower or "chat" in chat_text_lower:
            comm_issue = "Chasing clients on WhatsApp and managing notifications manually."
            
        return {
            "industry": industry,
            "company_name": name,
            "company_size": size,
            "business_summary": {
                "industry": industry,
                "company_size": size,
                "key_processes": [
                    "Responding to incoming customer inquiries",
                    "Recording data in spreadsheets / legacy software",
                    "Scheduling meetings or consultations",
                    "Generating weekly performance reviews"
                ],
                "existing_tools": "Excel, Gmail, Phone calls, Basic calendar",
                "operational_bottlenecks": "Manual entry of booking details and double-data entries leading to 10+ hours wasted per week."
            },
            "pain_points": {
                "manual_work": manual_work_found,
                "customer_communication": comm_issue,
                "sales_inefficiencies": "No lead qualification or automated follow-ups for warm leads.",
                "support_inefficiencies": "Answering the same operational questions repetitively.",
                "reporting_challenges": "No central database, making tracking conversion metrics slow and prone to errors."
            },
            "readiness_scores": {
                "Customer Support": 45,
                "Sales": 40,
                "Operations": 50,
                "Marketing": 45,
                "Analytics": 30
            }
        }

class AutomationAgent(BaseAgent):
    """
    Automation Agent:
    - Recommends AI integrations.
    - Generates actionable, visual blueprints (Triggers, Steps, Tools, Setup time).
    - Recommends software stacks and monthly cost estimates.
    """
    
    def generate_recommendations(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        industry = analysis["industry"]
        bottlenecks = analysis["business_summary"]["operational_bottlenecks"]
        
        if self.is_live:
            try:
                system_prompt = (
                    "You are the Automation Agent. Given a business analysis, generate 3 highly relevant, professional AI/automation recommendations.\n"
                    "Format the output strictly as a JSON object with two fields:\n"
                    "1. recommendations: an array of recommendations, where each has:\n"
                    "   - title: Title of tool\n"
                    "   - category: 'Customer Support', 'Sales', 'Operations', 'Marketing', or 'Analytics'\n"
                    "   - problem: Pain point targeted\n"
                    "   - solution: Automated solution description\n"
                    "   - effort: 'Low', 'Medium', or 'High'\n"
                    "   - impact: 'Low', 'Medium', or 'High'\n"
                    "   - priority: 'High', 'Medium', or 'Low'\n"
                    "   - description: 1-2 sentence description\n"
                    "   - setup_time: Time estimate (e.g. '3 Days')\n"
                    "   - blueprint: {trigger: string, process: array of strings, tools: array of strings, difficulty: string, setup_time: string}\n"
                    "2. tech_stack: an array of software stack tools, where each has:\n"
                    "   - category: e.g. 'Workflow Automation'\n"
                    "   - tool: e.g. 'n8n'\n"
                    "   - cost: monthly cost in INR (integer, e.g. 1500)\n"
                    "   - difficulty: 'Low', 'Medium', 'High'\n"
                    "   - setup_time: '1 Week', '3 Days', etc."
                )
                
                schema = {
                    "type": "OBJECT",
                    "properties": {
                        "recommendations": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "title": {"type": "STRING"},
                                    "category": {"type": "STRING"},
                                    "problem": {"type": "STRING"},
                                    "solution": {"type": "STRING"},
                                    "effort": {"type": "STRING"},
                                    "impact": {"type": "STRING"},
                                    "priority": {"type": "STRING"},
                                    "description": {"type": "STRING"},
                                    "setup_time": {"type": "STRING"},
                                    "blueprint": {
                                        "type": "OBJECT",
                                        "properties": {
                                            "trigger": {"type": "STRING"},
                                            "process": {"type": "ARRAY", "items": {"type": "STRING"}},
                                            "tools": {"type": "ARRAY", "items": {"type": "STRING"}},
                                            "difficulty": {"type": "STRING"},
                                            "setup_time": {"type": "STRING"}
                                        },
                                        "required": ["trigger", "process", "tools", "difficulty", "setup_time"]
                                    }
                                },
                                "required": ["title", "category", "problem", "solution", "effort", "impact", "priority", "description", "setup_time", "blueprint"]
                            }
                        },
                        "tech_stack": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "category": {"type": "STRING"},
                                    "tool": {"type": "STRING"},
                                    "cost": {"type": "INTEGER"},
                                    "difficulty": {"type": "STRING"},
                                    "setup_time": {"type": "STRING"}
                                },
                                "required": ["category", "tool", "cost", "difficulty", "setup_time"]
                            }
                        }
                    },
                    "required": ["recommendations", "tech_stack"]
                }
                
                prompt = f"Business Industry: {industry}\nBottlenecks: {bottlenecks}\nPain Points: {json.dumps(analysis['pain_points'])}"
                result_str = self._call_gemini(system_prompt, prompt, schema=schema)
                return json.loads(result_str)
            except Exception as e:
                logger.error(f"Automation Agent Live call failed: {e}. Falling back to simulation.")
                
        # Heuristic simulation
        return {
            "recommendations": [
                {
                    "title": "AI Customer Support Assistant",
                    "category": "Customer Support",
                    "problem": "Manual responses to repetitive support emails and messages.",
                    "solution": "Deploy a conversational AI agent integrated with WhatsApp and Email.",
                    "effort": "Low",
                    "impact": "High",
                    "priority": "High",
                    "description": "Answers FAQs instantly and forwards complex cases to your team.",
                    "setup_time": "3 Days",
                    "blueprint": {
                        "trigger": "Customer submits web contact form or sends message",
                        "process": [
                            "Webhook triggers FastAPI endpoint",
                            "Gemini categorizes ticket topic",
                            "Retrieves relevant solution from knowledge base",
                            "Sends reply to customer via Twilio API",
                            "Logs ticket in database / spreadsheet"
                        ],
                        "tools": ["FastAPI", "Gemini API", "Twilio SMS", "Excel Online API"],
                        "difficulty": "Medium",
                        "setup_time": "3 Days"
                    }
                },
                {
                    "title": "Automated Lead Qualification Drips",
                    "category": "Sales",
                    "problem": "Losing track of client follow-ups; high manual work checking lead budget.",
                    "solution": "Create automated SMS/Email workflows qualifying leads based on their responses.",
                    "effort": "Medium",
                    "impact": "High",
                    "priority": "High",
                    "description": "Engages prospects, captures details, and schedules appointments automatically.",
                    "setup_time": "5 Days",
                    "blueprint": {
                        "trigger": "Lead details received from Facebook / Landing page",
                        "process": [
                            "Zapier webhook runs",
                            "AI generates personalized qualification text",
                            "Sends email/SMS flow with calendar link",
                            "If client schedules, slots registered in CRM"
                        ],
                        "tools": ["Zapier", "Gemini", "HubSpot CRM", "Calendly"],
                        "difficulty": "Medium",
                        "setup_time": "5 Days"
                    }
                }
            ],
            "tech_stack": [
                {"category": "Customer Support", "tool": "Twilio + Gemini API", "cost": 2500, "difficulty": "Medium", "setup_time": "3 Days"},
                {"category": "CRM & Scheduling", "tool": "HubSpot Starter + Calendly", "cost": 1800, "difficulty": "Low", "setup_time": "2 Days"},
                {"category": "Workflow Engine", "tool": "Zapier / Make.com", "cost": 1500, "difficulty": "Low", "setup_time": "1 Day"}
            ]
        }

class ROIAgent(BaseAgent):
    """
    ROI Agent:
    - Predicts lead increases, conversion improvements, cost savings, and hours saved.
    - Generates numbers for charts.
    """
    
    def estimate_roi(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        if self.is_live:
            try:
                system_prompt = (
                    "You are the ROI Agent. Given a business profile, forecast realistic before vs after automation metrics.\n"
                    "Output strictly as a JSON object with: \n"
                    "1. current_leads: int\n"
                    "2. predicted_leads: int\n"
                    "3. current_conversion: float (e.g. 15.0)\n"
                    "4. predicted_conversion: float (e.g. 22.0)\n"
                    "5. current_support_cost: int (monthly cost in INR)\n"
                    "6. predicted_support_cost: int (monthly cost in INR)\n"
                    "7. hours_saved_weekly: int\n"
                    "8. monthly_cost_savings: int"
                )
                
                schema = {
                    "type": "OBJECT",
                    "properties": {
                        "current_leads": {"type": "INTEGER"},
                        "predicted_leads": {"type": "INTEGER"},
                        "current_conversion": {"type": "NUMBER"},
                        "predicted_conversion": {"type": "NUMBER"},
                        "current_support_cost": {"type": "INTEGER"},
                        "predicted_support_cost": {"type": "INTEGER"},
                        "hours_saved_weekly": {"type": "INTEGER"},
                        "monthly_cost_savings": {"type": "INTEGER"}
                    },
                    "required": [
                        "current_leads", "predicted_leads", "current_conversion", "predicted_conversion",
                        "current_support_cost", "predicted_support_cost", "hours_saved_weekly", "monthly_cost_savings"
                    ]
                }
                
                prompt = f"Industry: {analysis['industry']}\nSize: {analysis['company_size']}\nBottlenecks: {analysis['business_summary']['operational_bottlenecks']}"
                result_str = self._call_gemini(system_prompt, prompt, schema=schema)
                return json.loads(result_str)
            except Exception as e:
                logger.error(f"ROI Agent Live call failed: {e}. Falling back to simulation.")
                
        # Heuristic simulation
        return {
            "current_leads": 120,
            "predicted_leads": 170,
            "current_conversion": 18.0,
            "predicted_conversion": 26.5,
            "current_support_cost": 40000,
            "predicted_support_cost": 15000,
            "hours_saved_weekly": 16,
            "monthly_cost_savings": 25000
        }

class RoadmapAgent(BaseAgent):
    """
    Roadmap Agent:
    - Generates 3-phase transformation strategy (Quick Wins, Process Automation, Advanced AI).
    - Structures timelines and key deliverables.
    """
    
    def generate_roadmap(self, recommendations: List[Dict[str, Any]], industry: str) -> Dict[str, Any]:
        if self.is_live:
            try:
                system_prompt = (
                    "You are the Roadmap Agent. Given the industry and recommendations, compile a 3-phase week-by-week implementation plan.\n"
                    "Output strictly as a JSON object with: \n"
                    "1. phase1: array of steps (title, timeline, action, deliverables)\n"
                    "2. phase2: array of steps (title, timeline, action, deliverables)\n"
                    "3. phase3: array of steps (title, timeline, action, deliverables)"
                )
                
                schema = {
                    "type": "OBJECT",
                    "properties": {
                        "phase1": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "title": {"type": "STRING"},
                                    "timeline": {"type": "STRING"},
                                    "action": {"type": "STRING"},
                                    "deliverables": {"type": "STRING"}
                                },
                                "required": ["title", "timeline", "action", "deliverables"]
                            }
                        },
                        "phase2": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "title": {"type": "STRING"},
                                    "timeline": {"type": "STRING"},
                                    "action": {"type": "STRING"},
                                    "deliverables": {"type": "STRING"}
                                },
                                "required": ["title", "timeline", "action", "deliverables"]
                            }
                        },
                        "phase3": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "title": {"type": "STRING"},
                                    "timeline": {"type": "STRING"},
                                    "action": {"type": "STRING"},
                                    "deliverables": {"type": "STRING"}
                                },
                                "required": ["title", "timeline", "action", "deliverables"]
                            }
                        }
                    },
                    "required": ["phase1", "phase2", "phase3"]
                }
                
                prompt = f"Industry: {industry}\nRecommendations: {json.dumps(recommendations)}"
                result_str = self._call_gemini(system_prompt, prompt, schema=schema)
                return json.loads(result_str)
            except Exception as e:
                logger.error(f"Roadmap Agent Live call failed: {e}. Falling back to simulation.")
                
        # Heuristic simulation
        return {
            "phase1": [
                {"title": "Deploy FAQ & Chat Assistant", "timeline": "Week 1-2", "action": "Hook up chat webhook and load business context into Gemini.", "deliverables": "FAQ assistant operational."}
            ],
            "phase2": [
                {"title": "CRM & Appointment Integration", "timeline": "Week 3-5", "action": "Connect calendar and contact forms to automatically write to CRM.", "deliverables": "Leads automatically synced."}
            ],
            "phase3": [
                {"title": "Predictive Workflow Insights", "timeline": "Week 6-8", "action": "Launch analytics pipeline linking sales channels.", "deliverables": "Operational dashboard live."}
            ]
        }
