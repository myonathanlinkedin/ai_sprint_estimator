import pandas as pd
import json
from src.evaluation import evaluate
from src.model_inference import query_model


def run_pipeline(trials: int = 3):
    df = pd.read_csv("data/user_stories.csv")
    records = []

    print(f"Running sprint effort estimation pipeline with {trials} "
          f"trials per story...")
    print(f"Processing {len(df)} user stories...")

    for _, row in df.iterrows():
        print(f"Processing story {row['id']}: {row['story'][:50]}...")
        for t in range(trials):
            raw, latency = query_model(row["story"])

            # Parse the JSON response to extract estimate
            try:
                # Handle markdown code fences
                if "```json" in raw:
                    # Extract JSON from markdown code block
                    start = raw.find("```json") + 7
                    end = raw.find("```", start)
                    json_str = raw[start:end].strip()
                else:
                    json_str = raw
                
                parsed = json.loads(json_str)
                estimate = parsed.get("estimate", None)
            except (json.JSONDecodeError, KeyError):
                estimate = None

            records.append({
                "story_id": row["id"],
                "trial": t,
                "story": row["story"],
                "raw_output": raw,
                "response_time": latency,
                "estimate": estimate
            })

    out_csv = "results/model_outputs.csv"
    pd.DataFrame(records).to_csv(out_csv, index=False)
    print(f"Results saved to {out_csv}")

    summary = evaluate(out_csv, "results/benchmark_summary.json")
    print("Benchmark summary saved to results/benchmark_summary.json")

    # Print summary
    print("\n=== BENCHMARK SUMMARY ===")
    if 'global' in summary and summary['global']:
        print("Global Statistics:")
        print(f"  Mean estimate: {summary['global']['mean']:.2f}")
        print(f"  Standard deviation: {summary['global']['std']:.2f}")
        print(f"  Median (p50): {summary['global']['p50']:.2f}")
        print(f"  90th percentile: {summary['global']['p90']:.2f}")
    else:
        print("Global Statistics: No valid estimates found")

    print("\nPer-Story Statistics:")
    for story_id, stats in summary['stories'].items():
        if stats['mean'] is not None:
            print(f"  Story {story_id}: mean={stats['mean']:.2f}, "
                  f"std={stats['std']:.2f}, "
                  f"consistency={stats['consistency_within_±1']:.2f}")
        else:
            print(f"  Story {story_id}: No valid estimates")


if __name__ == "__main__":
    run_pipeline(trials=5)