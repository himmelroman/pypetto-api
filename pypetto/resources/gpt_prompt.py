# =========== #
# GPT Prompts #
# =========== #

# Role
PROMPT_ROLE = \
    'You are an assistant for analytical and critical thinking, ' \
    'helping people to detect and challenge populism.\n'

# Claims & Questions task
PROMPT_CLAIMS_QUESTIONS = \
    'Your task is to extract the main claims made in the text, and generate 5 questions based on these claims.\n' \
    'The questions should demand details of plans and decisions that stem from the claims.\n'

PROMPT_CLAIMS_QUESTIONS_ENDING = 'Consider the following text:'

# Output formatting
PROMPT_OUTPUT_QUERY = \
    'Output only JSON, an object with two lists, ' \
    'one list with the claims named \"claims\" and one with the questions named \"questions\".\n'

PROMPT_OUTPUT_STREAM = \
    'Output each claim with prefix "{C#{num}}", and questions with "{Q#{num}}"\n'

PROMPT_OUTPUT_STREAM_REGEX = r"\{([CQ])#(\d)\}"
