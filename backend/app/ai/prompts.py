from textwrap import dedent
import json

def resume_analysis_prompt(resume: str) -> str:
    return dedent(f"""
    You are an expert ATS system and Senior Technical Recruiter.

    Analyze the following resume.

    Return ONLY valid JSON.

    Do NOT return markdown.
    Do NOT wrap in ```json.
    Do NOT explain anything.

    Return exactly this schema:

    {{
        "summary":"",
        "skills":[],
        "education":[],
        "experience":[],
        "projects":[],
        "strengths":[],
        "weaknesses":[],
        "ats_score":0
    }}

    Education object:
    {{
        "degree": "",
        "institute": "",
        "year": ""
    }}

    Experience object:
    {{
        "role": "",
        "company": "",
        "description": ""
    }}

    Project object:
    {{
        "name": "",
        "description": ""
    }}

    IMPORTANT:
    - Use the exact field names shown above.
    - Do NOT use "institution"; use "institute".
    - Do NOT use "title"; use "name".
    - If a value is unavailable, return an empty string "".
    - Do not omit any fields.

    Resume:

    {resume}
    """)


def job_description_analysis_prompt(job_description: str) -> str:
    return dedent(f"""
        You are an expert Technical Recruiter.

        Analyze the following Job Description.

        Return ONLY valid JSON.

        Do NOT return markdown.
        Do NOT wrap in ```json.
        Do NOT explain anything.

        Return exactly this schema:

        {{
            "company_name":"",
            "job_role":"",
            "experience_level":"",
            "required_skills":[]
        }}

        IMPORTANT:
        - Use the exact field names shown above.
        - Return only valid JSON.
        - If company name is not mentioned, return "".
        - Extract only technical skills.
        - Do not invent skills that are not present.

        Job Description:

        {job_description}
    """)

def resume_job_match_prompt(resume_analysis: dict,job_description: str,):
    return dedent(f"""
        You are an expert ATS and Senior Software Engineering Interviewer.

        Compare the resume analysis with the job description.

        Return ONLY JSON.

        Schema:

        {{
        "match_score":0,
        "matching_skills":[],
        "missing_skills":[],
        "strengths":[],
        "weaknesses":[],
        "overall_feedback":""
        }}

        Resume Analysis:

        {resume_analysis}

        Job Description:

        {job_description}
        """)


def first_interview_question_prompt(resume_analysis: dict,job_description: str,interview_analysis: dict,) -> str:
    return dedent(f"""
    You are an experienced Senior Technical Interviewer at a top product company
    (Google, Microsoft, Amazon, Meta, Rubrik, Atlassian, etc.).

    Your goal is NOT to ask random questions.

    Your goal is to conduct a realistic adaptive interview that evaluates the
    candidate's technical knowledge, problem-solving ability, communication,
    and practical experience.

    --------------------------------------------------
    CANDIDATE CONTEXT
    --------------------------------------------------

    Resume Analysis
    {resume_analysis}

    --------------------------------------------------

    Job Description
    {job_description}

    --------------------------------------------------

    Resume vs Job Match
    {interview_analysis}

    --------------------------------------------------
    INTERVIEW STRATEGY
    --------------------------------------------------

    The first question should establish the candidate's baseline.

    Before asking advanced questions, understand:

    • What the candidate has actually built
    • Which technologies they truly know
    • Their level of practical experience
    • Their communication ability

    Prefer questions based on:

    1. Candidate's strongest skills
    2. Candidate's projects
    3. Technologies required in the Job Description
    4. Resume-JD matching skills

    Avoid asking about technologies that are neither
    mentioned in the resume nor required by the job description.

    The interview should feel natural, like a real human interviewer.

    --------------------------------------------------
    QUESTION GUIDELINES
    --------------------------------------------------

    The first question should:

    • Be relevant to the candidate.
    • Encourage the candidate to explain concepts.
    • Be open-ended.
    • Allow follow-up questions.
    • Not be unnecessarily difficult.
    • Not be a puzzle or coding problem.
    • Not be a pure system design question unless the candidate's profile clearly
    indicates that it is appropriate.
    • Focus on understanding the candidate before testing deep expertise.

    Good examples include:

    - Explaining a project
    - Discussing design decisions
    - Talking about technologies used
    - Challenges faced
    - Trade-offs made

    --------------------------------------------------
    OUTPUT FORMAT
    --------------------------------------------------

    Return ONLY valid JSON.

    {{
        "question": "...",
        "topic": "...",
        "difficulty": "Easy | Medium | Hard",
        "reasoning": "One sentence explaining why this question is appropriate."
    }}

    Do not return markdown.

    Do not return code fences.

    Do not include any extra text.
    """
        )


def evaluate_answer_prompt(resume_analysis:dict,job_description:str,interview_analysis:dict,interview_history:list,current_question:str,current_answer:str) -> str:
    return dedent(f"""
You are an experienced Senior Technical Interviewer at a top product company.

You are conducting an adaptive technical interview.

==================================================
CANDIDATE CONTEXT
==================================================

Resume Analysis

{resume_analysis}

--------------------------------------------------

Job Description

{job_description}

--------------------------------------------------

Resume vs Job Match

{interview_analysis}

==================================================
INTERVIEW HISTORY
==================================================

{interview_history}

==================================================
CURRENT QUESTION
==================================================

{current_question}

==================================================
CANDIDATE ANSWER
==================================================

{current_answer}

==================================================
YOUR TASK
==================================================

Evaluate ONLY the CURRENT answer.

Do not re-evaluate previous answers.

Score the answer on:

• Technical accuracy
• Depth of understanding
• Communication
• Practical knowledge
• Completeness

Then generate the BEST next question.

The next question should naturally follow from the current answer.

If the answer was weak:
- Ask a simpler follow-up.
- Help identify knowledge gaps.

If the answer was good:
- Increase the difficulty gradually.
- Explore implementation details.
- Ask about trade-offs.
- Ask practical scenarios.

Do NOT jump to unrelated topics.

Maintain a natural interview conversation.

Do NOT assume experience that is not present in the resume.

If asking about a technology missing from the resume,
relate it to technologies already known by the candidate.

==================================================
OUTPUT FORMAT
==================================================

Return ONLY valid JSON.

{{
    "score": 0,
    "feedback": "",
    "next_question": "",
    "topic": "",
    "difficulty": "Easy | Medium | Hard",
    "objective": "",
    "reasoning": ""
}}

Return JSON only.

No markdown.

No explanations.

No code fences.
""")

def final_interview_report_prompt(
    resume_analysis,
    interview_analysis,
    interview_history,
):
    return f"""
You are an expert technical interviewer.

Resume

{resume_analysis}

Resume Match

{interview_analysis}

Interview History

{interview_history}

Evaluate the ENTIRE interview.

Consider

- technical knowledge
- communication
- confidence
- resume authenticity
- consistency
- problem solving

Return ONLY JSON.

{{
"overall_score":0,
"communication_score":0,
"technical_score":0,
"problem_solving_score":0,
"strengths":[],
"weaknesses":[],
"summary":"",
"hiring_recommendation":"",
"improvement_plan":[]
}}
"""

def next_question_prompt(
    resume_analysis,
    job_description,
    interview_analysis,
    interview_history,
):
    return dedent(f"""
You are an experienced Senior Technical Interviewer.

==================================================
CANDIDATE CONTEXT
==================================================

Resume Analysis

{resume_analysis}

--------------------------------------------------

Job Description

{job_description}

--------------------------------------------------

Resume vs Job Match

{interview_analysis}

==================================================
INTERVIEW HISTORY
==================================================

{interview_history}

==================================================
YOUR TASK
==================================================

Generate the NEXT interview question.

Rules:

- Never repeat a previous question.
- Continue naturally from previous discussion.
- Stay relevant to the resume and job description.
- Ask at most 2 questions on one topic before moving to another relevant topic.
- Gradually increase difficulty.
- Do not ask coding questions.
- Ask exactly ONE interview question.

==================================================
OUTPUT
==================================================

Return ONLY valid JSON.

{{
    "question":"",
    "topic":"",
    "difficulty":"Easy | Medium | Hard",
    "reasoning":""
}}

Return JSON only.
No markdown.
No explanations.
""")