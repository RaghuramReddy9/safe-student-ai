import pandas as pd
from datetime import datetime
import os

LOG_PATH = "data/prompts_log.csv"

def log_interaction(prompt, response, score):
    entry= {
        "timestamp": datetime.now(),
        "prompt": prompt,
        "response": response,
        "toxicity_score": score
    }
    df = pd.DataFrame([entry])
    if not os.path.exists(LOG_PATH):
        df.to_csv(LOG_PATH, index=False)
    else:
        df.to_csv(LOG_PATH, mode='a', header=False, index=False)

    