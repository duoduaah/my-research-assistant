import boto3
import sys
import argparse
from pathlib import Path

#project_root = Path.cwd().parent
#sys.path.append(str(project_root))

from src.agents.counter_argument import CounterArgumentAgent
from src.preprocessing.normalize_similarity import normalize_similarity
from src.preprocessing.clean_json import clean_json
from src.preprocessing.select_counter_claims import select_counter_claims
from src.preprocessing.build_final import build_final_response
from src.pipelines.inference import run_summary, get_fresh_claims, get_retrieved_claims

counterarg = CounterArgumentAgent()

def main(user_query):
    retrieved = get_retrieved_claims(user_query, 2)
    fresh = get_fresh_claims(user_query, 10)
    summarized = run_summary(retrieved, fresh)

    fresh_claims_sim_scored = [normalize_similarity(c) for c in fresh]
    all_claims = retrieved + fresh_claims_sim_scored

    selected_claims = select_counter_claims(all_claims)
    counter_res = counterarg.run_counterarg(selected_claims)
    counter_res = clean_json(counter_res)

    final = build_final_response(user_query, summarized, counter_res)
    print(final)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="research assistant, provide your query")
    parser.add_argument("-u", "--user_query", type=str, required=True, help="research question")
    args = parser.parse_args()
    main(args.user_query)