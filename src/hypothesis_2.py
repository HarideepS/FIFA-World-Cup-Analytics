# H2: Team Market Value vs World Cup Progression

import pandas as pd

import matplotlib.pyplot as plt

from scipy.stats import spearmanr, pearsonr

from pathlib import Path


pd.set_option('display.max_columns', None)


# Load raw datasets

matches = pd.read_csv(
    "data/raw/matches_1930_2022.csv"
)

market_value = pd.read_csv(
    "data/raw/team_market_value_2022.csv"
)

world_cup = pd.read_csv(
    "data/raw/world_cup.csv"
)

# Filter matches to the 2022 World Cup

matches_2022 = matches[
    matches['Year'] == 2022
]

# Validation Check -> 2022 matches: 64
"""
print("2022 matches:", len(matches_2022))
"""


# Create one row per team appearance in each round

home_rounds = matches_2022[
    ['home_team', 'Round']
].rename(
    columns={'home_team': 'Team'}
)

away_rounds = matches_2022[
    ['away_team', 'Round']
].rename(
    columns={'away_team': 'Team'}
)

team_rounds = pd.concat(
    [home_rounds, away_rounds],
    ignore_index=True
)

# Validation Check -> team_rounds should contain 128 rows.
# print(team_rounds.shape)


# Assign an ordered progression level to each tournament round

round_order = {
    'Group stage': 0,
    'Round of 16': 1,
    'Quarter-finals': 2,
    'Semi-finals': 3,
    'Final': 4,
    'Third-place match': 3
}

team_rounds['Progression_Level'] = (
    team_rounds['Round'].map(round_order)
)

# Validation Check -> a NaN here would mean: "We encountered a Round value that wasn't in our dictionary."
# print(team_rounds['Progression_Level'].isna().sum())


# Determine the furthest stage reached by each team

team_progression = (
    team_rounds
    .groupby('Team')['Progression_Level']
    .max()
    .reset_index()
)

# Validation Check -> (32, 2) and 32
# print(team_progression.shape)
# print(team_progression['Team'].nunique())


# Identify the 2022 World Cup champion

champion = world_cup.loc[
    world_cup['Year'] == 2022,
    'Champion'
].iloc[0]

# Assign the highest progression level to the champion

team_progression.loc[
    team_progression['Team'] == champion,
    'Progression_Level'
] = 5

# Validation Check -> Argentina    5  |  France       4
"""
print(
    team_progression[
        team_progression['Team'].isin(
            ['Argentina', 'France']
        )
    ]
)
"""


# Normalize team names to match the market-value dataset

team_progression['Team'] = team_progression['Team'].replace({
    'IR Iran': 'Iran',
    'Korea Republic': 'South Korea'
})

# Validation Check -> Empty DataFrame : Every progression team now exists in the market-value dataset.
"""
unmatched_teams = team_progression[
    ~team_progression['Team'].isin(
        market_value['Team']
    )
]

print(unmatched_teams)
"""


# Merge market value with tournament progression

hypothesis_2_data = pd.merge(
    market_value,
    team_progression,
    on='Team',
    how='inner'
)

# Validation Check -> (32, 3) and 32
"""
print(hypothesis_2_data.shape)
print(hypothesis_2_data['Team'].nunique())
"""

# Test the relationship between market value and tournament progression

spearman_correlation, spearman_p_value = spearmanr(
    hypothesis_2_data['Market_Value_EUR_M'],
    hypothesis_2_data['Progression_Level']
)

pearson_correlation, pearson_p_value = pearsonr(
    hypothesis_2_data['Market_Value_EUR_M'],
    hypothesis_2_data['Progression_Level']
)

print()
print("=" * 70)
print("HYPOTHESIS #2 — TEAM MARKET VALUE vs WORLD CUP PROGRESSION")
print("=" * 70)

print()
print("Spearman Correlation Test")
print("Spearman Correlation:", spearman_correlation)
print("Spearman P-Value:", spearman_p_value)

print()
print("Pearson Correlation Test")
print("Pearson Correlation:", pearson_correlation)
print("Pearson P-Value:", pearson_p_value)


# Visualize the relationship

plt.scatter(
    hypothesis_2_data['Market_Value_EUR_M'],
    hypothesis_2_data['Progression_Level']
)

plt.xlabel('Team Market Value (€ Millions)')
plt.ylabel('Tournament Progression Level')
plt.title('Team Market Value vs World Cup Progression - 2022')

progression_mapping = (
    "Progression Level Mapping\n"
    "0  Group Stage\n"
    "1  Round of 16\n"
    "2  Quarter-finals\n"
    "3  Semi-finals\n"
    "4  Runner-up\n"
    "5  Champion"
)

plt.text(
    1.02,
    0.5,
    progression_mapping,
    transform=plt.gca().transAxes,
    verticalalignment='center',
    bbox=dict(
        boxstyle='round,pad=0.5',
        facecolor='white',
        edgecolor='gray'
    )
)

plt.tight_layout()

project_root = Path(__file__).resolve().parent.parent

visuals_dir = project_root / "visuals" / "hypothesis_2"
visuals_dir.mkdir(parents=True, exist_ok=True)

plt.savefig(
    visuals_dir / "market_value_vs_progression_2022.png",
    dpi=300,
    bbox_inches='tight'
)

plt.close()