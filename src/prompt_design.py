PROMPT_SYSTEM = "You are an experienced Agile coach. Give a concise, structured JSON output."

PROMPT_USER_TEMPLATE = (
    "Estimate story points (integer 1-10) for the user story below. "
    "Return valid JSON only with keys: estimate (int), reasons (list of short strings), "
    "similar_examples (short string), confidence (low|med|high).\n\n"
    "User story: \"{story}\"\n"
    "Be concise."
)

