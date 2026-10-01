# analyze.py
# SUMMARY (fill in these two lines AFTER you have run the script and read the numbers):

# Distance since last service, daily driving distance and load matter most for breakdowns.
# Age and total mileage made no difference, so the obvious guesses were wrong.

# Make KM-Waechter smarter: rank cars by breakdown risk from their history.
# Steps: load -> compare the two groups per column -> score only the columns that separate -> rank.

import pandas as pd

TARGET = "broke_down"
MIN_EFFECT = 0.5   # a column "separates" if the group means differ by >= 0.5 standard deviations

df = pd.read_csv("fleet_history.csv")
print(df.head(), "\n")
print(f"{len(df)} cars, {int(df[TARGET].sum())} broke down\n")

numeric_cols = [c for c in df.select_dtypes("number").columns if c != TARGET]
broke = df[df[TARGET] == 1]
fine = df[df[TARGET] == 0]

# --- Step 2: compare the two groups, column by column ---------------------------------
rows = []
for col in numeric_cols:
    spread = df[col].std()
    effect = (broke[col].mean() - fine[col].mean()) / spread if spread else 0.0
    rows.append({
        "column": col,
        "mean_broke": round(broke[col].mean(), 2),
        "mean_fine": round(fine[col].mean(), 2),
        "effect_size": round(effect, 2),          # in standard deviations; sign = direction
        "corr_with_breakdown": round(df[col].corr(df[TARGET]), 2),
    })
comparison = pd.DataFrame(rows).sort_values("effect_size", key=abs, ascending=False)
print("Group comparison (sorted by strength of separation):")
print(comparison.to_string(index=False), "\n")

# Text columns: breakdown rate per category (look for categories far from the overall rate)
for col in df.select_dtypes(exclude="number").columns:
    if df[col].nunique() <= 10:
        print(f"Breakdown rate by {col}:")
        print(df.groupby(col)[TARGET].agg(["mean", "count"]).round(2), "\n")

# --- Step 3: simple 0-100 risk score from the columns that DO separate ----------------
keep = comparison[comparison["effect_size"].abs() >= MIN_EFFECT]
print("Columns used in the score:", list(keep["column"]) or "NONE - lower MIN_EFFECT")

score = pd.Series(0.0, index=df.index)
for _, r in keep.iterrows():
    col = r["column"]
    scaled = (df[col] - df[col].min()) / (df[col].max() - df[col].min())  # 0..1
    if r["effect_size"] < 0:      # lower value = riskier, so flip it
        scaled = 1 - scaled
    score += scaled * abs(r["effect_size"])   # stronger separators count for more
if score.max() > 0:
    score = 100 * score / score.max()
df["risk_score"] = score.round(1)

# --- Step 4: ranked output, highest risk first ----------------------------------------
id_cols = [c for c in df.columns if df[c].dtype == object][:1]
show = id_cols + list(keep["column"]) + [TARGET, "risk_score"]
print("\nCars ranked by risk (highest first):")
print(df.sort_values("risk_score", ascending=False)[show].to_string(index=False))
