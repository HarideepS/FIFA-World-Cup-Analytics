import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import kruskal, spearmanr


# ============================================================
# H3: PREVIOUS WORLD CUP EXPERIENCE VS TOURNAMENT PERFORMANCE
# ============================================================

historical_wc = pd.read_csv(
    "data/processed/historical_world_cup_processed.csv"
)


# ============================================================
# DATA VALIDATION
# ============================================================

required_columns = [
    "Year",
    "Team",
    "Historical_Team",
    "Previous_WC_Editions",
    "Previous_WC_Matches",
    "Final_Stage",
    "Progression_Score",
]

missing_columns = [
    column
    for column in required_columns
    if column not in historical_wc.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

print("Dataset shape:", historical_wc.shape)
print(
    "Missing values:",
    historical_wc[required_columns].isna().sum().sum()
)


# First World Cup appearance must have zero previous experience.
first_appearance_check = historical_wc[
    historical_wc["Previous_WC_Editions"] == 0
]

first_time_match_violations = (
    first_appearance_check["Previous_WC_Matches"] != 0
).sum()

print(
    "First-time teams with non-zero previous matches:",
    first_time_match_violations
)


# Previous experience cannot decrease for a team over time.
historical_sorted = historical_wc.sort_values(
    ["Historical_Team", "Year"]
)

edition_violations = (
    historical_sorted
    .groupby("Historical_Team")["Previous_WC_Editions"]
    .diff()
    .dropna()
)

match_violations = (
    historical_sorted
    .groupby("Historical_Team")["Previous_WC_Matches"]
    .diff()
    .dropna()
)

print(
    "Edition-count violations:",
    (edition_violations < 0).sum()
)

print(
    "Match-count violations:",
    (match_violations < 0).sum()
)


# ============================================================
# CORRELATION ANALYSIS
# ============================================================

rho_editions, p_editions = spearmanr(
    historical_wc["Previous_WC_Editions"],
    historical_wc["Progression_Score"]
)

rho_matches, p_matches = spearmanr(
    historical_wc["Previous_WC_Matches"],
    historical_wc["Progression_Score"]
)

print("Previous WC Editions vs Progression Score")
print(f"Spearman rho: {rho_editions:.3f}")
print(f"p-value: {p_editions:.6f}")
print(f"Rho squared: {rho_editions ** 2:.3f}")

print("Previous WC Matches vs Progression Score")
print(f"Spearman rho: {rho_matches:.3f}")
print(f"p-value: {p_matches:.6f}")
print(f"Rho squared: {rho_matches ** 2:.3f}")


# ============================================================
# EXPERIENCE LEVEL ANALYSIS
# ============================================================

experience_progression = (
    historical_wc
    .groupby("Previous_WC_Editions")
    .agg(
        Teams=("Team", "count"),
        Mean_Progression=("Progression_Score", "mean"),
        Median_Progression=("Progression_Score", "median"),
    )
    .reset_index()
)

print("Progression by Previous World Cup Editions")
print(
    experience_progression.to_string(index=False)
)


# ============================================================
# EXPERIENCE BANDS
# ============================================================

historical_wc["Experience_Band"] = pd.cut(
    historical_wc["Previous_WC_Editions"],
    bins=[-1, 3, 7, 11, np.inf],
    labels=["0–3", "4–7", "8–11", "12+"],
)

experience_bands = (
    historical_wc
    .groupby("Experience_Band", observed=True)
    .agg(
        Teams=("Team", "count"),
        Mean_Progression=("Progression_Score", "mean"),
        Median_Progression=("Progression_Score", "median"),
    )
    .reset_index()
)

print("Progression by Experience Band")
print(
    experience_bands.to_string(index=False)
)


# ============================================================
# VISUALIZATION
# ============================================================

plt.figure(figsize=(9, 6))

plt.plot(
    experience_bands["Experience_Band"],
    experience_bands["Mean_Progression"],
    marker="o",
)

plt.xlabel("Previous World Cup Editions")
plt.ylabel("Mean Progression Score")
plt.title(
    "Tournament Progression by Previous World Cup Experience"
)

plt.grid(True)
plt.tight_layout()
plt.show()


# ============================================================
# KRUSKAL-WALLIS TEST
# ============================================================

groups = [
    group["Progression_Score"].values
    for _, group in historical_wc.groupby(
        "Experience_Band",
        observed=True,
    )
]

h_stat, p_value = kruskal(*groups)

print("Kruskal-Wallis Test")
print(f"H-statistic: {h_stat:.3f}")
print(f"p-value: {p_value:.6f}")