# Industry Templates Library for FlowArchitect AI

TEMPLATES = {
    "dental_clinic": {
        "company_name": "Apex Dental Clinic",
        "industry": "Healthcare / Dental Services",
        "company_size": "10-20 employees",
        "business_summary": {
            "industry": "Dental Care",
            "company_size": "15 employees (3 dentists, 2 hygienists, 2 receptionists, 8 support staff)",
            "key_processes": [
                "Patient appointment scheduling and reminders",
                "Patient onboarding, medical history check-ins",
                "Billing, insurance claim filings",
                "Patient follow-ups and recall campaigns"
            ],
            "existing_tools": "Dentrix (Legacy on-premise EHR), Google Calendar, Outlook Email",
            "operational_bottlenecks": "Receptionists spend 4 hours daily making manual appointment confirmation calls. High patient no-show rate (18%). Delayed insurance pre-authorizations."
        },
        "pain_point_analysis": {
            "manual_work": "Calling patients one-by-one to confirm bookings and reschedule appointments manually.",
            "customer_communication": "No automated text channels (patients must call or email); missed incoming patient queries outside of 9 AM - 5 PM office hours.",
            "sales_inefficiencies": "No system to follow up with patients who inquired about cosmetic procedures (Invisalign, implants) but didn't book immediately.",
            "support_inefficiencies": "Answering repetitive phone queries about pricing, insurance network, and operating hours takes up reception hours.",
            "reporting_challenges": "No dashboard for tracking patient retention rates, booking sources, or active treatment pipeline value."
        },
        "automation_readiness": {
            "Customer Support": 40,
            "Sales": 30,
            "Operations": 50,
            "Marketing": 45,
            "Analytics": 20
        },
        "recommendations": [
            {
                "title": "AI WhatsApp Booking & Appointment Assistant",
                "category": "Customer Support",
                "problem": "Front-desk staff overloaded with scheduling calls; high no-show rate.",
                "solution": "Deploy a WhatsApp conversational agent integrated with the booking system for automated calendar checks, reservation, and patient confirmation.",
                "effort": "Medium",
                "impact": "High",
                "priority": "High",
                "description": "An interactive agent that manages real-time calendars, responds to FAQs, handles cancellations, and sends automated reminder/confirmation sequences.",
                "setup_time": "4 Days",
                "blueprint": {
                    "trigger": "Patient sends WhatsApp message inquiring about booking or availability",
                    "process": [
                        "Message received via Twilio WhatsApp API",
                        "Gemini classifies intent and queries available doctor calendar slots",
                        "System returns matching slots to patient; patient selects a time",
                        "Appointment locked in Google Calendar / Clinic EHR",
                        "WhatsApp confirmation sent with prep instructions",
                        "Clinic CRM updated with appointment status"
                    ],
                    "tools": ["WhatsApp Business API / Twilio", "Gemini API", "Google Calendar API", "Clinic CRM / EHR"],
                    "difficulty": "Medium",
                    "setup_time": "4 Days"
                }
            },
            {
                "title": "Automated Insurance Verification & Triage",
                "category": "Operations",
                "problem": "Manual checking of insurance eligibility delays check-in and treatment approvals.",
                "solution": "Configure an OCR-based document processing flow that parses insurance card uploads and queries verification APIs automatically.",
                "effort": "High",
                "impact": "High",
                "priority": "Medium",
                "description": "Patients upload insurance cards in advance. The system extracts data and verifies copay details, updating the patient chart before arrival.",
                "setup_time": "7 Days",
                "blueprint": {
                    "trigger": "Patient submits new patient registration form with insurance card photo",
                    "process": [
                        "PDF or image uploaded to secure storage",
                        "Gemini extracts card details (Member ID, Group No, Provider)",
                        "Webhook triggers insurance verification portal API query",
                        "Eligibility status and copay summaries returned",
                        "Clinic EHR updated with verified status and copay alert"
                    ],
                    "tools": ["FastAPI", "Gemini OCR (Structured Schema)", "Insurance API", "Secure EHR Storage"],
                    "difficulty": "High",
                    "setup_time": "7 Days"
                }
            },
            {
                "title": "Cosmetic Treatment Lead Follow-up Automation",
                "category": "Sales",
                "problem": "Inquiries about premium dental procedures (Invisalign, implants) are lost due to lack of follow-ups.",
                "solution": "Build an email/SMS drip campaign triggered by consultations, providing educational content and booking incentives.",
                "effort": "Low",
                "impact": "High",
                "priority": "High",
                "description": "Nurtures patients after their initial diagnostic checkup with case studies and testimonials, offering interest-free payment plans.",
                "setup_time": "3 Days",
                "blueprint": {
                    "trigger": "Dentist tags patient chart with 'Cosmetic Candidate - Invisalign'",
                    "process": [
                        "EHR webhook updates ActiveCampaign / HubSpot CRM",
                        "Welcome email sent with Invisalign 3D video simulation and testimonial",
                        "Day 3: SMS sent offering free virtual consultation",
                        "Day 7: Task created in receptionist panel if patient did not schedule"
                    ],
                    "tools": ["ActiveCampaign", "SMS Gateway (Twilio)", "Clinic CRM"],
                    "difficulty": "Low",
                    "setup_time": "3 Days"
                }
            }
        ],
        "tech_stack": [
            {"category": "Customer Support", "tool": "Twilio (WhatsApp) + Gemini API", "cost": 3000, "difficulty": "Medium", "setup_time": "5 Days"},
            {"category": "CRM & Scheduling", "tool": "Google Calendar + HubSpot CRM Starter", "cost": 1500, "difficulty": "Low", "setup_time": "2 Days"},
            {"category": "Workflow Automation", "tool": "n8n (Self-hosted or Cloud)", "cost": 1800, "difficulty": "Medium", "setup_time": "3 Days"},
            {"category": "Patient Reviews", "tool": "NiceJob (Automated feedback requests)", "cost": 3500, "difficulty": "Low", "setup_time": "1 Day"},
            {"category": "Document AI", "tool": "Google Cloud Document AI / Gemini OCR", "cost": 2000, "difficulty": "High", "setup_time": "7 Days"}
        ],
        "roi_prediction": {
            "current_leads": 80,
            "predicted_leads": 120,
            "current_conversion": 15.0,
            "predicted_conversion": 22.5,
            "current_support_cost": 45000,
            "predicted_support_cost": 15000,
            "hours_saved_weekly": 18,
            "monthly_cost_savings": 30000
        },
        "roadmap_plan": {
            "phase1": [
                {"title": "Deploy WhatsApp FAQ & Hours Bot", "timeline": "Week 1", "action": "Implement WhatsApp Business API with pre-scripted FAQ handling static queries.", "deliverables": "Working WhatsApp endpoint answering patient FAQs."},
                {"title": "Calendar Scheduling Integration", "timeline": "Week 2", "action": "Connect WhatsApp booking automation to Google Calendar / Doctor schedules.", "deliverables": "Direct appointment bookings written to calendar."}
            ],
            "phase2": [
                {"title": "Deploy Cosmetic CRM Pipeline", "timeline": "Week 3-4", "action": "Configure CRM stages for treatment options and write follow-up automation campaigns.", "deliverables": "HubSpot CRM integration with trigger-based SMS drips."}
            ],
            "phase3": [
                {"title": "AI Insurance Extraction Engine", "timeline": "Week 5-8", "action": "Integrate Gemini Vision API to extract card details and run eligibility check pipelines.", "deliverables": "Automated document scanning matching client cards with insurance databases."}
            ]
        },
        "workflow_diagram": {
            "nodes": [
                {"id": "n1", "label": "Patient Inquires via WhatsApp", "type": "trigger", "x": 100, "y": 200, "details": "Incoming WhatsApp text inquiring about cost or availability."},
                {"id": "n2", "label": "Gemini AI Intent Check", "type": "process", "x": 280, "y": 200, "details": "Gemini parses message to identify booking or general info intent."},
                {"id": "n3", "label": "EHR Calendar Query", "type": "process", "x": 460, "y": 200, "details": "Queries doctor schedule to find open slots."},
                {"id": "n4", "label": "Automated Booking", "type": "action", "x": 640, "y": 200, "details": "Patient confirms slot; database locked and calendar event created."},
                {"id": "n5", "label": "CRM Log & Check-in Prep", "type": "action", "x": 820, "y": 200, "details": "Patient profile updated. Automated intake questionnaire sent."}
            ],
            "edges": [
                {"source": "n1", "target": "n2"},
                {"source": "n2", "target": "n3"},
                {"source": "n3", "target": "n4"},
                {"source": "n4", "target": "n5"}
            ]
        }
    },
    "ecommerce_store": {
        "company_name": "SwiftCart Apparel",
        "industry": "Retail / E-commerce",
        "company_size": "5-10 employees",
        "business_summary": {
            "industry": "Fashion E-commerce",
            "company_size": "8 employees",
            "key_processes": [
                "Customer support ticket management",
                "Inventory tracking and updates",
                "Order fulfillment & dispatch notifications",
                "Abandoned cart recovery & marketing"
            ],
            "existing_tools": "Shopify, Zendesk, Mailchimp, Excel",
            "operational_bottlenecks": "60% of customer support tickets are repetitive 'Where is my order?' (WISMO) queries. Stock count updates are done manually from warehouse spreadsheets twice a week, leading to overselling issues."
        },
        "pain_point_analysis": {
            "manual_work": "Manually updating stock levels across multiple Sales channels (Shopify, Amazon).",
            "customer_communication": "Support agents spend hours copy-pasting tracking links from shipping portals into customer chats.",
            "sales_inefficiencies": "Generic, non-personalized emails are failing to convert abandoned cart shoppers.",
            "support_inefficiencies": "Support response time averages 14 hours during weekends when staffing is minimal.",
            "reporting_challenges": "Difficult to calculate net profit margins due to untracked ad-spend vs inventory cost fluctuations."
        },
        "automation_readiness": {
            "Customer Support": 75,
            "Sales": 65,
            "Operations": 60,
            "Marketing": 70,
            "Analytics": 50
        },
        "recommendations": [
            {
                "title": "Shopify API AI Order Status Assistant",
                "category": "Customer Support",
                "problem": "High support volume answering shipment tracking questions.",
                "solution": "Integrate an AI Agent with Shopify Order Tracking webhook to resolve status queries instantly.",
                "effort": "Low",
                "impact": "High",
                "priority": "High",
                "description": "Automatically reads tracking info from Shopify and informs customers in natural language.",
                "setup_time": "2 Days",
                "blueprint": {
                    "trigger": "Customer asks 'Where is my order #1042?' via web chat",
                    "process": [
                        "Chatbot queries Shopify Admin API for order #1042",
                        "Extracts shipping provider and tracking number",
                        "Calls carrier API (e.g. FedEx, USPS) to get latest location",
                        "Synthesizes friendly tracking update text",
                        "Sends update link and ETA directly in chat"
                    ],
                    "tools": ["Shopify API", "Gemini API", "AfterShip / Carrier Webhooks"],
                    "difficulty": "Low",
                    "setup_time": "2 Days"
                }
            },
            {
                "title": "Real-time Multi-channel Inventory Syncer",
                "category": "Operations",
                "problem": "Overselling stock due to lag in manual inventory updates across Shopify and Amazon.",
                "solution": "Deploy an n8n workflow that triggers when inventory updates in the ERP, auto-updating web storefronts.",
                "effort": "Medium",
                "impact": "High",
                "priority": "High",
                "description": "Eliminates double-selling and manual stock sheets by synchronizing inventory in near real-time.",
                "setup_time": "5 Days",
                "blueprint": {
                    "trigger": "Warehouse management system updates stock levels in Excel/ERP",
                    "process": [
                        "Webhook sent to automation hub (n8n)",
                        "Workflow checks stock counts for SKU matching",
                        "Triggers batch update calls to Shopify Inventory API",
                        "Triggers batch update calls to Amazon Seller Central API",
                        "Logs status report to Slack channel"
                    ],
                    "tools": ["n8n", "Shopify API", "Amazon Seller API", "Slack API"],
                    "difficulty": "Medium",
                    "setup_time": "5 Days"
                }
            }
        ],
        "tech_stack": [
            {"category": "Customer Support", "tool": "Tidio Chat / Gemini Live Chat", "cost": 2500, "difficulty": "Low", "setup_time": "2 Days"},
            {"category": "Workflow Automation", "tool": "n8n (Self-hosted on Render)", "cost": 1500, "difficulty": "Medium", "setup_time": "3 Days"},
            {"category": "Email Marketing", "tool": "Klaviyo (Personalized AI Drips)", "cost": 4000, "difficulty": "Medium", "setup_time": "4 Days"},
            {"category": "Shipment Tracking", "tool": "AfterShip API", "cost": 1200, "difficulty": "Low", "setup_time": "1 Day"}
        ],
        "roi_prediction": {
            "current_leads": 1200,
            "predicted_leads": 1500,
            "current_conversion": 2.1,
            "predicted_conversion": 3.2,
            "current_support_cost": 60000,
            "predicted_support_cost": 20000,
            "hours_saved_weekly": 24,
            "monthly_cost_savings": 40000
        },
        "roadmap_plan": {
            "phase1": [
                {"title": "Deploy Order Status FAQ Chatbot", "timeline": "Week 1", "action": "Hook up Shopify store to automated AI chat assistant for ship status.", "deliverables": "WISMO ticket counts reduced by 50%."},
                {"title": "AI Abandoned Cart Flow", "timeline": "Week 2", "action": "Design Klaviyo dynamic flows based on products viewed and cart value.", "deliverables": "Targeted recovery emails active."}
            ],
            "phase2": [
                {"title": "Automated Stock Syncing", "timeline": "Week 3-4", "action": "Connect shop inventory database to warehouse shipping records via n8n.", "deliverables": "Zero stock discrepancy across channels."}
            ],
            "phase3": [
                {"title": "Predictive Restock Planner", "timeline": "Week 5-6", "action": "Apply AI forecasting to past order history to recommend order times for suppliers.", "deliverables": "Replenishment dashboard indicating lead times."}
            ]
        },
        "workflow_diagram": {
            "nodes": [
                {"id": "e1", "label": "Customer Abandons Cart", "type": "trigger", "x": 100, "y": 200, "details": "Visitor drops off at checkout flow without completing checkout."},
                {"id": "e2", "label": "Gemini AI Segment Classifier", "type": "process", "x": 280, "y": 200, "details": "Classifies buyer persona, cart size, and history."},
                {"id": "e3", "label": "Klaviyo Personalized Offer", "type": "process", "x": 460, "y": 200, "details": "Generates tailor-made coupon code and email copy."},
                {"id": "e4", "label": "SMS/Email Drip Dispatched", "type": "action", "x": 640, "y": 200, "details": "Triggers multi-stage recovery flow automatically."},
                {"id": "e5", "label": "Cart Recovered & Conversion", "type": "action", "x": 820, "y": 200, "details": "Customer clicks link and completes checkout."}
            ],
            "edges": [
                {"source": "e1", "target": "e2"},
                {"source": "e2", "target": "e3"},
                {"source": "e3", "target": "e4"},
                {"source": "e4", "target": "e5"}
            ]
        }
    },
    "real_estate": {
        "company_name": "Horizon Properties",
        "industry": "Real Estate / Brokerage",
        "company_size": "5-15 agents",
        "business_summary": {
            "industry": "Real Estate",
            "company_size": "10 agents",
            "key_processes": [
                "Lead generation and property inquiry collection",
                "Buyer qualification & scheduling property showings",
                "Listing updates across real estate portals (Zillow, Magicbricks)",
                "Contract drafting and document collection"
            ],
            "existing_tools": "Zillow Premier Agent, Follow Up Boss CRM, WhatsApp Business, DocuSign",
            "operational_bottlenecks": "Agents spend 30% of their day responding to cold leads who do not have pre-approved mortgages or are just browsing. Scheduling open house showings involves a constant back-and-forth of emails and phone calls."
        },
        "pain_point_analysis": {
            "manual_work": "Manually qualifying incoming portal leads before scheduling viewings.",
            "customer_communication": "Delayed response times to online listing inquiries (often 3-4 hours), losing buyers to competing agents.",
            "sales_inefficiencies": "No systematic follow-ups for prospects after showing a property.",
            "support_inefficiencies": "Answering simple questions about listings (HOA fees, parking spots, square footage) manually over and over.",
            "reporting_challenges": "No clear view of active agent pipeline conversion metrics or showing feedback logs."
        },
        "automation_readiness": {
            "Customer Support": 55,
            "Sales": 45,
            "Operations": 50,
            "Marketing": 60,
            "Analytics": 35
        },
        "recommendations": [
            {
                "title": "AI Assistant for 24/7 Lead Qualification",
                "category": "Sales",
                "problem": "Agents wasting time on unqualified window shoppers.",
                "solution": "Deploy a conversational WhatsApp and Web AI agent to qualify leads on budget, timeline, and mortgage pre-approval.",
                "effort": "Medium",
                "impact": "High",
                "priority": "High",
                "description": "Instantly responds to listing inquiries, queries financing readiness, and books qualified buyers directly into agent schedules.",
                "setup_time": "3 Days",
                "blueprint": {
                    "trigger": "User submits Zillow or Facebook Lead Form",
                    "process": [
                        "Lead details pushed to Follow Up Boss CRM",
                        "AI agent sends WhatsApp greeting within 2 minutes",
                        "Asks 3 qualifying questions (Budget, Location, Pre-approval status)",
                        "If qualified, schedules viewing via Cal.com API",
                        "If unqualified, adds to monthly educational email list"
                    ],
                    "tools": ["Twilio / Cal.com", "Gemini", "Follow Up Boss CRM", "Zapier"],
                    "difficulty": "Medium",
                    "setup_time": "3 Days"
                }
            },
            {
                "title": "Open House Feedback Loop & Drip Marketing",
                "category": "Marketing",
                "problem": "Agents fail to gather review ratings and feedback after property showings.",
                "solution": "Automated feedback request SMS trigger sent 1 hour after a scheduled showing.",
                "effort": "Low",
                "impact": "Medium",
                "priority": "High",
                "description": "Sends feedback form via SMS; positive feedback triggers review prompt, negative feedback alerts agent.",
                "setup_time": "2 Days",
                "blueprint": {
                    "trigger": "Appointment marked 'Completed' in scheduling database",
                    "process": [
                        "Webhook triggers after-showing SMS via Twilio",
                        "User rates property 1-5 stars",
                        "If 4 or 5 stars, sends link to review agent page",
                        "If <4, alerts listing agent and drafts follow-up email asking for details"
                    ],
                    "tools": ["Twilio SMS", "Make.com", "Google Forms / Typeform"],
                    "difficulty": "Low",
                    "setup_time": "2 Days"
                }
            }
        ],
        "tech_stack": [
            {"category": "Customer Support & Booking", "tool": "Cal.com + Twilio SMS API", "cost": 2200, "difficulty": "Low", "setup_time": "2 Days"},
            {"category": "CRM Integration", "tool": "Follow Up Boss / HubSpot CRM", "cost": 3000, "difficulty": "Medium", "setup_time": "3 Days"},
            {"category": "Automation Integrator", "tool": "Make.com (Inbound webhooks)", "cost": 1200, "difficulty": "Low", "setup_time": "1 Day"},
            {"category": "AI Lead Profiler", "tool": "Gemini API (Data extraction)", "cost": 1500, "difficulty": "Medium", "setup_time": "2 Days"}
        ],
        "roi_prediction": {
            "current_leads": 150,
            "predicted_leads": 200,
            "current_conversion": 4.0,
            "predicted_conversion": 6.5,
            "current_support_cost": 30000,
            "predicted_support_cost": 10000,
            "hours_saved_weekly": 15,
            "monthly_cost_savings": 20000
        },
        "roadmap_plan": {
            "phase1": [
                {"title": "Deploy Zillow Auto-Responder", "timeline": "Week 1", "action": "Link listing portals to a webhook that triggers an instant SMS introduction.", "deliverables": "Average response time reduced to 60 seconds."},
                {"title": "Cal.com Calendar Sync", "timeline": "Week 2", "action": "Give agents customized booking links and sync calendars to prevent double booking.", "deliverables": "Self-serve showing scheduling live."}
            ],
            "phase2": [
                {"title": "Qualifying Chat Agent", "timeline": "Week 3-4", "action": "Hook up conversational Gemini agent to collect buyer preferences and budgets.", "deliverables": "Pre-screened leads routed to agents."}
            ],
            "phase3": [
                {"title": "Document Automation Portal", "timeline": "Week 5-8", "action": "Build a portal that scans buyer pre-approval letters and drafts DocuSign offers.", "deliverables": "Contracts compiled with 90% manual reduction."}
            ]
        },
        "workflow_diagram": {
            "nodes": [
                {"id": "r1", "label": "New Property Inquiry", "type": "trigger", "x": 100, "y": 200, "details": "User submits lead form on listing website."},
                {"id": "r2", "label": "Instant AI Qualify Chat", "type": "process", "x": 280, "y": 200, "details": "SMS sent asking budget, timing, mortgage approval status."},
                {"id": "r3", "label": "Mortgage Docs Scan", "type": "process", "x": 460, "y": 200, "details": "AI extracts mortgage limits and pre-approval values."},
                {"id": "r4", "label": "Cal.com Showing Booked", "type": "action", "x": 640, "y": 200, "details": "Qualified buyer booked directly into agent's calendar."},
                {"id": "r5", "label": "Agent Meeting Alerts", "type": "action", "x": 820, "y": 200, "details": "Agent receives full qualified profile & notification."}
            ],
            "edges": [
                {"source": "r1", "target": "r2"},
                {"source": "r2", "target": "r3"},
                {"source": "r3", "target": "r4"},
                {"source": "r4", "target": "r5"}
            ]
        }
    },
    "hospital": {
        "company_name": "Metro Health Hospital",
        "industry": "Healthcare / Medical Centers",
        "company_size": "100+ employees",
        "business_summary": {
            "industry": "Hospital",
            "company_name": "Metro Health Hospital",
            "company_size": "250 staff",
            "key_processes": ["Patient registration", "EHR entries", "Ward assignment", "Billing discharge"],
            "existing_tools": "Epic Systems EHR, Excel, PagerDuty, Call centers",
            "operational_bottlenecks": "Discharge workflow is bottlenecked by manual insurance approval processing, occupying beds 4 hours longer than needed."
        },
        "pain_point_analysis": {
            "manual_work": "Entering billing data and patient chart histories into multiple systems.",
            "customer_communication": "Patients waiting on hold for appointments, lab results, and billing queries.",
            "sales_inefficiencies": "Unmanaged patient referral follow-ups with local practitioners.",
            "support_inefficiencies": "Front-desk answering 'how to prepare for colonoscopy' and similar prep instruction queries.",
            "reporting_challenges": "Compiling reports on bed utilization, ER wait times, and readmission rates."
        },
        "automation_readiness": {
            "Customer Support": 35,
            "Sales": 25,
            "Operations": 40,
            "Marketing": 30,
            "Analytics": 45
        },
        "recommendations": [
            {
                "title": "AI Patient Prep Assistant",
                "category": "Customer Support",
                "problem": "Patient procedures rescheduled due to failed pre-treatment prep instructions.",
                "solution": "Deploy SMS automated check-in and prep checklists (e.g. fast for 12 hours before surgery).",
                "effort": "Medium",
                "impact": "High",
                "priority": "High",
                "description": "Conversational agent reminding patients of prep steps and answering specific queries.",
                "setup_time": "5 Days",
                "blueprint": {
                    "trigger": "Appointment marked in EHR scheduling",
                    "process": [
                        "Webhook checks procedure type",
                        "Generates custom schedule of instructions",
                        "SMS notifications sent automatically at T-72h, T-24h, T-12h",
                        "Patient answers questions to confirm compliance"
                    ],
                    "tools": ["Epic API", "Twilio SMS", "Gemini API"],
                    "difficulty": "Medium",
                    "setup_time": "5 Days"
                }
            }
        ],
        "tech_stack": [
            {"category": "Integration EHR", "tool": "Redox Engine API / HL7 Integration", "cost": 15000, "difficulty": "High", "setup_time": "15 Days"},
            {"category": "Patient Chat", "tool": "Gemini Medical Model", "cost": 5000, "difficulty": "High", "setup_time": "10 Days"},
            {"category": "Alerts & Notifications", "tool": "Pagers/Twilio Enterprise", "cost": 4000, "difficulty": "Medium", "setup_time": "4 Days"}
        ],
        "roi_prediction": {
            "current_leads": 1200,
            "predicted_leads": 1350,
            "current_conversion": 90.0,
            "predicted_conversion": 95.0,
            "current_support_cost": 250000,
            "predicted_support_cost": 180000,
            "hours_saved_weekly": 120,
            "monthly_cost_savings": 70000
        },
        "roadmap_plan": {
            "phase1": [
                {"title": "Deploy FAQ and Prep SMS Bot", "timeline": "Week 1-3", "action": "Hook clinic phone lists to automated prep flows.", "deliverables": "FAQ response rate 90%."}
            ],
            "phase2": [
                {"title": "Referral Management Automation", "timeline": "Week 4-6", "action": "Automate clinic referral notifications for incoming doctors.", "deliverables": "Referrals dashboard active."}
            ],
            "phase3": [
                {"title": "Epic HL7 Webhook Sync", "timeline": "Week 7-12", "action": "Connect AI pipeline directly into EHR records.", "deliverables": "Automatic check-in logging."}
            ]
        },
        "workflow_diagram": {
            "nodes": [
                {"id": "h1", "label": "Procedure Scheduled in EHR", "type": "trigger", "x": 100, "y": 200, "details": "Epic database triggers procedure confirmation."},
                {"id": "h2", "label": "Prep Instructions Generation", "type": "process", "x": 280, "y": 200, "details": "Gemini drafts instructions according to medical guidelines."},
                {"id": "h3", "label": "Scheduled Patient SMS Drip", "type": "process", "x": 460, "y": 200, "details": "Drips reminders 3 days, 1 day, and 12 hours before check-in."},
                {"id": "h4", "label": "Patient Compliance Validation", "type": "action", "x": 640, "y": 200, "details": "Patient confirms fasting status via text reply."},
                {"id": "h5", "label": "Nurse Ward Alert", "type": "action", "x": 820, "y": 200, "details": "Status flagged 'Ready' in surgical system."}
            ],
            "edges": [
                {"source": "h1", "target": "h2"},
                {"source": "h2", "target": "h3"},
                {"source": "h3", "target": "h4"},
                {"source": "h4", "target": "h5"}
            ]
        }
    },
    "coaching_institute": {
        "company_name": "Lumin Educational Academy",
        "industry": "Education / Coaching",
        "company_size": "10-25 employees",
        "business_summary": {
            "industry": "Coaching Institute",
            "company_name": "Lumin Educational Academy",
            "company_size": "20 tutors & admin staff",
            "key_processes": ["Lead inquiries", "Course registration", "Student fee payments", "Grade sheets and doubt solving"],
            "existing_tools": "WordPress LMS, WhatsApp Groups, Excel sheets, Cash/Bank transfers",
            "operational_bottlenecks": "Tutors spend 3 hours daily answering student doubts on WhatsApp. Fee collection is chased manually every month via phone calls."
        },
        "pain_point_analysis": {
            "manual_work": "Chasing tuition fees and manually matching bank slips to student receipts.",
            "customer_communication": "Disorganized parent-teacher update schedules; delay in replying to course fee questions.",
            "sales_inefficiencies": "No tracking of website visitors who filled dynamic brochure forms but never enrolled.",
            "support_inefficiencies": "Students asking identical doubts about curriculum materials, timing, and homework.",
            "reporting_challenges": "No database of parent satisfaction ratings or student drop-out alerts."
        },
        "automation_readiness": {
            "Customer Support": 50,
            "Sales": 55,
            "Operations": 40,
            "Marketing": 60,
            "Analytics": 30
        },
        "recommendations": [
            {
                "title": "AI Student Doubt Solver & FAQ Bot",
                "category": "Customer Support",
                "problem": "Teachers overloaded answering basic course questions.",
                "solution": "Deploy a Telegram/WhatsApp assistant that retrieves answers from lesson transcripts.",
                "effort": "Medium",
                "impact": "High",
                "priority": "High",
                "description": "Searches course documents and transcripts to answer curriculum questions instantly.",
                "setup_time": "3 Days",
                "blueprint": {
                    "trigger": "Student posts question in class WhatsApp group",
                    "process": [
                        "Webhook sends message content to RAG pipeline",
                        "System queries course handbook and vector database",
                        "Gemini drafts student-friendly explanation",
                        "Answers sent back to group tagging the student"
                    ],
                    "tools": ["WhatsApp Cloud API", "Gemini Embeddings", "Pinecone Vector DB"],
                    "difficulty": "Medium",
                    "setup_time": "3 Days"
                }
            }
        ],
        "tech_stack": [
            {"category": "Doubt Assistant", "tool": "Pinecone (Vector DB) + Gemini RAG", "cost": 2000, "difficulty": "Medium", "setup_time": "4 Days"},
            {"category": "Billing Automation", "tool": "Razorpay Subscription Webhooks", "cost": 1000, "difficulty": "Low", "setup_time": "2 Days"},
            {"category": "CRM & Communications", "tool": "Klaviyo + Twilio", "cost": 2500, "difficulty": "Low", "setup_time": "3 Days"}
        ],
        "roi_prediction": {
            "current_leads": 220,
            "predicted_leads": 310,
            "current_conversion": 12.0,
            "predicted_conversion": 18.5,
            "current_support_cost": 35000,
            "predicted_support_cost": 10000,
            "hours_saved_weekly": 20,
            "monthly_cost_savings": 25000
        },
        "roadmap_plan": {
            "phase1": [
                {"title": "Razorpay Fee Auto-Reminders", "timeline": "Week 1-2", "action": "Integrate Razorpay auto-debit and send payment links.", "deliverables": "Manual collections reduced."}
            ],
            "phase2": [
                {"title": "AI Doubt Solving Pilot", "timeline": "Week 3-4", "action": "Index course chapters and launch WhatsApp RAG bot.", "deliverables": "Teacher chat burden reduced by 60%."}
            ],
            "phase3": [
                {"title": "Automated Performance Analytics", "timeline": "Week 5-7", "action": "Generate student performance emails for parents automatically.", "deliverables": "Parent review scores increase."}
            ]
        },
        "workflow_diagram": {
            "nodes": [
                {"id": "c1", "label": "Student Asks Doubt in Group", "type": "trigger", "x": 100, "y": 200, "details": "Question posted in class group chat."},
                {"id": "c2", "label": "RAG Database Vector Search", "type": "process", "x": 280, "y": 200, "details": "Queries lesson texts for relevant source snippets."},
                {"id": "c3", "label": "Gemini Drafts Explanation", "type": "process", "x": 460, "y": 200, "details": "Formats text step-by-step with formulas."},
                {"id": "c4", "label": "Auto-Response Dispatched", "type": "action", "x": 640, "y": 200, "details": "Answers in chat, adding tutor warning tag if confidence is low."},
                {"id": "c5", "label": "Tutor Dash Logged", "type": "action", "x": 820, "y": 200, "details": "Question logged for teacher review in case edits are needed."}
            ],
            "edges": [
                {"source": "c1", "target": "c2"},
                {"source": "c2", "target": "c3"},
                {"source": "c3", "target": "c4"},
                {"source": "c4", "target": "c5"}
            ]
        }
    },
    "saas_startup": {
        "company_name": "DevFlow AI",
        "industry": "Software as a Service",
        "company_size": "10-30 employees",
        "business_summary": {
            "industry": "SaaS",
            "company_name": "DevFlow AI",
            "company_size": "18 employees",
            "key_processes": ["User signups", "Product onboarding tours", "Stripe billing", "Support ticket resolution"],
            "existing_tools": "Stripe, Intercom, HubSpot, AWS, Slack",
            "operational_bottlenecks": "Free trial users churn during the first 48 hours because they get stuck setting up the API key and receive no support response."
        },
        "pain_point_analysis": {
            "manual_work": "Chasing sales leads manually based on user actions in the dashboard.",
            "customer_communication": "Delayed response to tech issues; generic onboarding sequences that do not match the buyer profile.",
            "sales_inefficiencies": "No lead scoring (agents treat single developers and enterprise CTOs identically).",
            "support_inefficiencies": "Support engineers answering same configuration questions.",
            "reporting_challenges": "Churn alerts are only noticed during monthly reviews, when it is too late to recover."
        },
        "automation_readiness": {
            "Customer Support": 80,
            "Sales": 70,
            "Operations": 65,
            "Marketing": 75,
            "Analytics": 85
        },
        "recommendations": [
            {
                "title": "Onboarding Behavior AI Drips",
                "category": "Sales",
                "problem": "Users churn before completing setup steps.",
                "solution": "Connect Segment analytics to Intercom via AI workflows to trigger custom instructions for struggling accounts.",
                "effort": "Medium",
                "impact": "High",
                "priority": "High",
                "description": "Detects if API keys are generated but unused. Automatically sends debug resources.",
                "setup_time": "4 Days",
                "blueprint": {
                    "trigger": "User signs up but hasn't created API key within 24h",
                    "process": [
                        "Segment identifies event gap",
                        "Gemini writes a personalized follow-up with code snippets matching user stack",
                        "Sends email via Customer.io API",
                        "Flags account as 'Onboarding At Risk' in HubSpot CRM"
                    ],
                    "tools": ["Segment", "Gemini API", "Customer.io", "HubSpot"],
                    "difficulty": "Medium",
                    "setup_time": "4 Days"
                }
            }
        ],
        "tech_stack": [
            {"category": "Onboarding Flows", "tool": "Segment + Customer.io + Gemini", "cost": 6000, "difficulty": "Medium", "setup_time": "4 Days"},
            {"category": "CRM Integration", "tool": "HubSpot Enterprise Suite", "cost": 8000, "difficulty": "Medium", "setup_time": "5 Days"},
            {"category": "Doubt Desk", "tool": "Intercom Resolution Bot", "cost": 4500, "difficulty": "Low", "setup_time": "2 Days"}
        ],
        "roi_prediction": {
            "current_leads": 2000,
            "predicted_leads": 2500,
            "current_conversion": 1.5,
            "predicted_conversion": 2.8,
            "current_support_cost": 120000,
            "predicted_support_cost": 40000,
            "hours_saved_weekly": 35,
            "monthly_cost_savings": 80000
        },
        "roadmap_plan": {
            "phase1": [
                {"title": "Behavioral Onboarding Setup", "timeline": "Week 1-2", "action": "Hook Segment tracking events into Customer.io.", "deliverables": "Onboarding drips active."}
            ],
            "phase2": [
                {"title": "HubSpot Lead Scoring Engine", "timeline": "Week 3-4", "action": "Add automatic scoring rules for target enterprise profiles.", "deliverables": "CTO profiles routed to sales reps."}
            ],
            "phase3": [
                {"title": "AI Config Agent for API debugs", "timeline": "Week 5-8", "action": "Train Gemini model on API error codes to write instant fixes.", "deliverables": "Intercom bot resolving dev tickets."}
            ]
        },
        "workflow_diagram": {
            "nodes": [
                {"id": "s1", "label": "User Sign Up", "type": "trigger", "x": 100, "y": 200, "details": "New account registration created on dashboard."},
                {"id": "s2", "label": "Check Setup Completion", "type": "process", "x": 280, "y": 200, "details": "Scans if user key has processed requests."},
                {"id": "s3", "label": "Gemini AI Stack Detector", "type": "process", "x": 460, "y": 200, "details": "Analyzes the user's technology preferences and framework."},
                {"id": "s4", "label": "Targeted Code Email Sent", "type": "action", "x": 640, "y": 200, "details": "Dispatches instructions and code blocks for quick integration."},
                {"id": "s5", "label": "Activation Verified", "type": "action", "x": 820, "y": 200, "details": "User hits API; status flipped to 'Active User' in HubSpot."}
            ],
            "edges": [
                {"source": "s1", "target": "s2"},
                {"source": "s2", "target": "s3"},
                {"source": "s3", "target": "s4"},
                {"source": "s4", "target": "s5"}
            ]
        }
    },
    "restaurant": {
        "company_name": "Taverna Gusto",
        "industry": "Hospitality / F&B",
        "company_size": "15-30 employees",
        "business_summary": {
            "industry": "Restaurant",
            "company_name": "Taverna Gusto",
            "company_size": "22 staff",
            "key_processes": ["Table booking", "Order taking", "Supplier orders", "Feedback logging"],
            "existing_tools": "Toast POS, OpenTable, Pen & Paper, WhatsApp",
            "operational_bottlenecks": "Phone booking during dinner rush delays kitchen tickets; inventory counts are handwritten, leading to ingredient outages."
        },
        "pain_point_analysis": {
            "manual_work": "Calling food suppliers individually to order ingredients based on paper checklists.",
            "customer_communication": "No booking updates sent to guests, leading to an 11% table booking no-show rate.",
            "sales_inefficiencies": "No loyalty database or automated coupon rewards for weekend diners.",
            "support_inefficiencies": "Staff spends hours taking reservations and checking menu diets over phone lines.",
            "reporting_challenges": "Wasted ingredients are untracked, hiding real profit leaks."
        },
        "automation_readiness": {
            "Customer Support": 45,
            "Sales": 40,
            "Operations": 35,
            "Marketing": 50,
            "Analytics": 25
        },
        "recommendations": [
            {
                "title": "AI Reservation Agent",
                "category": "Customer Support",
                "problem": "Front-desk answers reservation calls during peak dinner hours, hurting service.",
                "solution": "Deploy a WhatsApp agent that links OpenTable calendar slots directly.",
                "effort": "Low",
                "impact": "High",
                "priority": "High",
                "description": "Answers bookings, sends menu PDFs, and provides directions automatically.",
                "setup_time": "3 Days",
                "blueprint": {
                    "trigger": "Customer messages asking to book a table for 4",
                    "process": [
                        "OpenTable API queried for slot times",
                        "Gemini writes availability options to chat",
                        "Customer selects slots and inputs name",
                        "SMS confirmation sent with calendar invite"
                    ],
                    "tools": ["OpenTable API", "Twilio API", "Gemini API"],
                    "difficulty": "Low",
                    "setup_time": "3 Days"
                }
            }
        ],
        "tech_stack": [
            {"category": "Table Booking", "tool": "OpenTable + WhatsApp Twilio Integration", "cost": 3000, "difficulty": "Low", "setup_time": "2 Days"},
            {"category": "Inventory Automator", "tool": "Toast POS + MarketMan API", "cost": 4000, "difficulty": "Medium", "setup_time": "4 Days"},
            {"category": "Feedback Campaigns", "tool": "Zapier + Mailchimp", "cost": 1500, "difficulty": "Low", "setup_time": "2 Days"}
        ],
        "roi_prediction": {
            "current_leads": 400,
            "predicted_leads": 550,
            "current_conversion": 89.0,
            "predicted_conversion": 96.0,
            "current_support_cost": 25000,
            "predicted_support_cost": 10000,
            "hours_saved_weekly": 12,
            "monthly_cost_savings": 15000
        },
        "roadmap_plan": {
            "phase1": [
                {"title": "WhatsApp Reservator Hookup", "timeline": "Week 1-2", "action": "Connect OpenTable to a WhatsApp number via Twilio.", "deliverables": "Table reservations booked."}
            ],
            "phase2": [
                {"title": "Automated Reviews Collection", "timeline": "Week 3-4", "action": "Trigger review links via email 2 hours after paying on Toast POS.", "deliverables": "Google reviews count grows by 40%."}
            ],
            "phase3": [
                {"title": "MarketMan POS Inventory Sync", "timeline": "Week 5-8", "action": "Auto-reorder ingredients from suppliers when stock dips below threshold.", "deliverables": "Zero ingredient stockouts."}
            ]
        },
        "workflow_diagram": {
            "nodes": [
                {"id": "rs1", "label": "WhatsApp Booking Inquiry", "type": "trigger", "x": 100, "y": 200, "details": "Guest texts asking for table availability."},
                {"id": "rs2", "label": "Query Table Slots", "type": "process", "x": 280, "y": 200, "details": "Checks real-time availability in OpenTable."},
                {"id": "rs3", "label": "Suggest Times & Diet FAQ", "type": "process", "x": 460, "y": 200, "details": "Gemini offers available times and answers allergy questions."},
                {"id": "rs4", "label": "Lock Reservation", "type": "action", "x": 640, "y": 200, "details": "Books table and writes info to host stand iPad."},
                {"id": "rs5", "label": "SMS Confirmation Drip", "type": "action", "x": 820, "y": 200, "details": "Dispatches verification text & reservation link."}
            ],
            "edges": [
                {"source": "rs1", "target": "rs2"},
                {"source": "rs2", "target": "rs3"},
                {"source": "rs3", "target": "rs4"},
                {"source": "rs4", "target": "rs5"}
            ]
        }
    },
    "marketing_agency": {
        "company_name": "PixelGlow Agency",
        "industry": "Marketing & Advertising",
        "company_size": "5-15 employees",
        "business_summary": {
            "industry": "Marketing Agency",
            "company_name": "PixelGlow Agency",
            "company_size": "12 team members",
            "key_processes": ["Client onboarding", "Social media content scheduling", "Reporting metrics", "Lead capture"],
            "existing_tools": "Google Sheets, Slack, Asana, Buffer, Loom, Zapier",
            "operational_bottlenecks": "Account managers spend the first week of every month manually pulling ad metrics from Facebook and Google into client slideshow reports."
        },
        "pain_point_analysis": {
            "manual_work": "Manually downloading CSVs and preparing monthly client marketing slides.",
            "customer_communication": "Clients constantly calling to ask what active campaigns are spending in real-time.",
            "sales_inefficiencies": "Slow quote generation for prospective clients who request proposals on the website.",
            "support_inefficiencies": "Onboarding clients requires several back-and-forth emails for access tokens.",
            "reporting_challenges": "Aggregating multi-channel ad spend vs ROI metrics in a clean visual layout."
        },
        "automation_readiness": {
            "Customer Support": 60,
            "Sales": 65,
            "Operations": 50,
            "Marketing": 85,
            "Analytics": 40
        },
        "recommendations": [
            {
                "title": "Automated Multi-Channel Client Reporting",
                "category": "Analytics",
                "problem": "Manual CSV formatting and reporting takes up 30 hours of account managers' time monthly.",
                "solution": "Use Looker Studio integrated with Supermetrics webhooks to refresh agency dashboards automatically.",
                "effort": "Medium",
                "impact": "High",
                "priority": "High",
                "description": "Auto-compiles Facebook, Google, and LinkedIn ad stats into a unified dashboard sent to clients on the 1st of the month.",
                "setup_time": "4 Days",
                "blueprint": {
                    "trigger": "1st day of the month at 9:00 AM",
                    "process": [
                        "Looker Studio updates Facebook Ads, Google Ads API values",
                        "Gemini extracts high-level trends and summarizes key takeaways",
                        "Builds PDF report on Google Drive",
                        "Emails report link to clients via Gmail API",
                        "Notifies account managers on Slack"
                    ],
                    "tools": ["Looker Studio", "Supermetrics", "Gemini API", "Gmail API", "Slack API"],
                    "difficulty": "Medium",
                    "setup_time": "4 Days"
                }
            }
        ],
        "tech_stack": [
            {"category": "Reporting", "tool": "Looker Studio + Supermetrics", "cost": 4500, "difficulty": "Medium", "setup_time": "3 Days"},
            {"category": "AI Copywriter", "tool": "Gemini Writer (Custom Drips)", "cost": 2000, "difficulty": "Low", "setup_time": "1 Day"},
            {"category": "Workflow Integrator", "tool": "Zapier Professional", "cost": 2500, "difficulty": "Low", "setup_time": "2 Days"}
        ],
        "roi_prediction": {
            "current_leads": 90,
            "predicted_leads": 130,
            "current_conversion": 18.0,
            "predicted_conversion": 26.0,
            "current_support_cost": 30000,
            "predicted_support_cost": 10000,
            "hours_saved_weekly": 16,
            "monthly_cost_savings": 20000
        },
        "roadmap_plan": {
            "phase1": [
                {"title": "Automate Onboarding Access Form", "timeline": "Week 1-2", "action": "Create Typeform onboarding hooks that request asset permissions automatically.", "deliverables": "Client onboarding time halved."}
            ],
            "phase2": [
                {"title": "Ad Reporting Dashboard Hookup", "timeline": "Week 3-4", "action": "Sync Supermetrics to agency's reporting dashboards.", "deliverables": "Real-time client portal active."}
            ],
            "phase3": [
                {"title": "Gemini Proposal Generator", "timeline": "Week 5-7", "action": "Deploy Gemini engine that drafts marketing strategies from lead forms.", "deliverables": "Sales proposals generated in minutes."}
            ]
        },
        "workflow_diagram": {
            "nodes": [
                {"id": "m1", "label": "Client Sign Up & Payment", "type": "trigger", "x": 100, "y": 200, "details": "Stripe processes setup payment; invoice created."},
                {"id": "m2", "label": "Onboarding Portal Triggered", "type": "process", "x": 280, "y": 200, "details": "Typeform sent requesting ad account IDs and brand files."},
                {"id": "m3", "label": "Gemini Audit & Outline", "type": "process", "x": 460, "y": 200, "details": "Reads brand data and extracts competitors to recommend keywords."},
                {"id": "m4", "label": "Asana Project Setup", "type": "action", "x": 640, "y": 200, "details": "Creates tasks for content schedule, designer asset reviews, and tracking setups."},
                {"id": "m5", "label": "Slack Channel & Client Alert", "type": "action", "x": 820, "y": 200, "details": "Shared Slack channel opened; invite link texted."}
            ],
            "edges": [
                {"source": "m1", "target": "m2"},
                {"source": "m2", "target": "m3"},
                {"source": "m3", "target": "m4"},
                {"source": "m4", "target": "m5"}
            ]
        }
    }
}
