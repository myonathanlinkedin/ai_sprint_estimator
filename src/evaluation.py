import pandas as pd, json, numpy as np, os

def evaluate(parsed_csv: str, out_summary: str):
    df = pd.read_csv(parsed_csv)
    summary = {"stories": {}, "global": {}}
    all_estimates = []

    for sid, g in df.groupby("story_id"):
        # Parse estimates from raw_output if estimate column is null
        estimates = []
        for _, row in g.iterrows():
            if pd.notna(row["estimate"]) and row["estimate"] != "":
                try:
                    estimates.append(float(row["estimate"]))
                except:
                    pass
            else:
                # Parse from raw_output
                raw = row["raw_output"]
                try:
                    import json
                    if "```json" in raw:
                        start = raw.find("```json") + 7
                        end = raw.find("```", start)
                        json_str = raw[start:end].strip()
                    else:
                        json_str = raw
                    parsed = json.loads(json_str)
                    if "estimate" in parsed:
                        estimates.append(float(parsed["estimate"]))
                except:
                    pass
        
        ests = pd.Series(estimates)
        mean = ests.mean() if len(ests) > 0 else None
        std = ests.std(ddof=0) if len(ests) > 0 else None
        cv = std / mean if mean and std else None
        consistency = None
        if len(ests) > 0:
            within1 = ((ests - ests.mean()).abs() <= 1).sum() / len(ests)
            consistency = within1
        summary["stories"][int(sid)] = {
            "n_trials": len(g),
            "mean": mean,
            "std": std,
            "cv": cv,
            "consistency_within_±1": consistency
        }
        all_estimates.extend(ests.tolist())

    if len(all_estimates) > 0:
        arr = np.array(all_estimates)
        summary["global"] = {
            "mean": arr.mean().item(),
            "std": arr.std().item(),
            "p50": np.percentile(arr, 50).item(),
            "p90": np.percentile(arr, 90).item()
        }

    os.makedirs(os.path.dirname(out_summary), exist_ok=True)
    with open(out_summary, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    return summary

