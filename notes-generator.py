import os
import time
from openai import OpenAI
import random

# ——— CONFIG ——————————————————————————————————
# 1) Install dependencies:
#    pip install openai>=1.0.0
#
# 2) Set your OpenAI API key in env:
#    export OPENAI_API_KEY="sk-..."
#
# 3) Adjust these as desired:
MODEL      = "gpt-3.5-turbo"      # or "gpt-4"
NUM_NOTES  = 32768                 # how many to generate
KEYWORDS   = ["hypertension", "HTN", "diabetes", "DM", "aspirin", "CT abdomen"]
LONG_RATE  = 1/50                 # ~1 in 50 should be long
MAX_CHARS  = 300                  # cap length
OUTPUT_FILE = "fake_med_notes.txt"


# ——— PROMPT TEMPLATES —————————————————————————
SYSTEM_PROMPT = """
You are a medical scribe assistant for a doctor who sees lots of kinds of patients
, and you have a sense of humor and occasionally make mistakes.
Generate exactly one de-identified outpatient note,
no more than {max_chars} characters long (including spaces). It should read like realistic
clinical free text, occasionally with a brief demographic statement, a one-sentence
history of present illness, a sentence or two of exam/ROS/plan, and optionally sprinkle in
one of these keywords: {keywords}. But remember that you try to be a bit funny.
Treat each request as a brand‐new session; do not reference or build on any previous outputs
as I need a diverse range of outputs.
""".strip()

SYSTEM_PROMPT2 = """
You are a medical scribe assistant for an unusual kind of doctor who sees lots of kinds of patients.
Generate exactly one de-identified outpatient note,
no more than {max_chars} characters long (including spaces). It should read like realistic
clinical free text, occasionally with a brief demographic statement, a one-sentence
history of present illness, a sentence or two of exam/ROS/plan. Include a lot of
very technical medical terminology.
""".strip()

USER_INSTRUCTION = "Generate one note now."


# ——— GENERATION FUNCTION ————————————————————————
def generate_note():
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT if random.randint(0, 50) == 0 else SYSTEM_PROMPT2},
            {"role": "user",   "content": USER_INSTRUCTION},
        ],
        temperature=1.4,
        max_tokens=MAX_CHARS // 2,  # plenty for ~300 chars
        n=1,
    )
    text = resp.choices[0].message.content.strip()
    # enforce length cap client‑side
    #if len(text) > MAX_CHARS:
    #    text = text[:MAX_CHARS].rsplit(" ", 1)[0]
    return text


# ——— MAIN LOOP —————————————————————————————
if __name__ == "__main__":
    for i in range(NUM_NOTES):
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        note = generate_note()
        with open(OUTPUT_FILE, "a") as f:
            f.write(note + "\n\n")
            time.sleep(0.3)  # simple rate‑limit safeguard

    print(f"Generated {NUM_NOTES} notes → {OUTPUT_FILE}")
