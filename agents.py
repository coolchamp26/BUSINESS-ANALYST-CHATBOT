import re
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

# ─── Questions ──────────────────────────────────────────────────────────────

QUESTIONS = [
    {"id": 0, "text": "What is your business name or the name of the product/service you're analyzing?",
     "hint": "e.g. 'Acme Corp' or 'My SaaS product'"},
    {"id": 1, "text": "What industry or sector does your business operate in?",
     "hint": "e.g. 'FinTech', 'Healthcare', 'E-commerce'"},
    {"id": 2, "text": "Who is your target customer? Describe them briefly.",
     "hint": "e.g. 'SMB owners aged 30-50 in the US'"},
    {"id": 3, "text": "What is the core problem your product or service solves?",
     "hint": "Be specific — what pain point does it address?"},
    {"id": 4, "text": "Who are your main competitors and what makes you different?",
     "hint": "e.g. 'Salesforce, but we're cheaper and easier to use'"},
    {"id": 5, "text": "What is your current revenue model or monetization strategy?",
     "hint": "e.g. 'Subscription SaaS at $49/month', 'Marketplace commission'"},
    {"id": 6, "text": "What is your biggest current challenge or bottleneck?",
     "hint": "e.g. 'Customer acquisition', 'Churn', 'Technical debt'"},
    {"id": 7, "text": "What does success look like for you in the next 12 months?",
     "hint": "e.g. '$1M ARR', '10k users', 'Launch in 3 new markets'"},
]


# ─── Local Validation ────────────────────────────────────────────────────────

GIBBERISH_RE = re.compile(r"^[^a-zA-Z]*$|(.)\1{4,}")  # all non-alpha or repeating chars
MIN_WORDS = {0: 1, 1: 1, 2: 3, 3: 4, 4: 3, 5: 3, 6: 3, 7: 3}
MAX_LEN = 500

GREETINGS = {"hi", "hello", "hey", "ok", "okay", "yes", "no", "sure", "thanks", "thank you", "idk", "hmm"}


def validate_answer(question_id: int, question: str, answer: str) -> dict:
    ans = answer.strip()

    if not ans:
        return {"valid": False, "reason": "Please provide an answer — don't leave this blank."}

    if len(ans) > MAX_LEN:
        return {"valid": False, "reason": f"Too long! Keep it under {MAX_LEN} characters."}

    if GIBBERISH_RE.match(ans):
        return {"valid": False, "reason": "That doesn't look like a valid answer. Try describing it in words."}

    words = ans.lower().split()
    if len(words) == 1 and words[0] in GREETINGS:
        return {"valid": False, "reason": "That looks like a greeting, not an answer. Please respond to the question."}

    min_w = MIN_WORDS.get(question_id, 2)
    if len(words) < min_w:
        return {"valid": False, "reason": f"Too brief! Please give at least {min_w} words so we can understand your answer."}

    return {"valid": True, "reason": ""}


# ─── Final Analysis via Claude ────────────────────────────────────────────────

ANALYSIS_SYSTEM = """You are a senior business analyst. Given structured answers from a founder or product manager, 
produce a concise strategic analysis in exactly 4 sections:
1. Business Overview (2 sentences)
2. Key Strengths (3 bullet points, one line each)
3. Critical Risks & Challenges (2 bullet points)
4. 90-Day Action Plan (3 prioritized steps)

Be direct, specific, and actionable. No fluff. Use markdown formatting."""


async def generate_analysis(answers: dict[str, str]) -> dict:
    qa_block = "\n".join(
        f"Q{qid} — {QUESTIONS[int(qid)]['text']}\nA: {ans}"
        for qid, ans in sorted(answers.items(), key=lambda x: int(x[0]))
        if int(qid) < len(QUESTIONS)
    )

    prompt = f"Here are the responses from a business stakeholder:\n\n{qa_block}\n\nProvide the strategic analysis."

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",  # cheapest, fastest — perfect for hackathon
            max_tokens=600,
            system=ANALYSIS_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text
        return {"analysis": text, "tokens_used": response.usage.input_tokens + response.usage.output_tokens}
    except Exception as e:
        return {"analysis": _fallback_analysis(answers), "tokens_used": 0, "error": str(e)}


def _fallback_analysis(answers: dict[str, str]) -> str:
    return f"""## Business Overview
{answers.get('0', 'Your business')} operates in the {answers.get('1', 'specified')} industry, targeting {answers.get('2', 'identified customers')}.

## Key Strengths
- Clear problem focus: {answers.get('3', 'N/A')}
- Differentiation vs competition: {answers.get('4', 'N/A')}
- Revenue model defined: {answers.get('5', 'N/A')}

## Critical Risks & Challenges
- {answers.get('6', 'Key challenge not specified')}
- Execution risk in reaching stated goal: {answers.get('7', 'Goal not specified')}

## 90-Day Action Plan
1. Address your primary challenge: {answers.get('6', 'TBD')}
2. Double down on your differentiator against {answers.get('4', 'competitors')}
3. Track progress toward: {answers.get('7', 'your 12-month goal')}"""
