#Hypothesis Testing

import pandas as pd

from scipy.stats import spearmanr, pearsonr

import matplotlib.pyplot as plt

from pathlib import Path

pd.set_option('display.max_columns', None)

matches = pd.read_csv("data/raw/matches_1930_2022.csv")

matches_2022 = matches[matches['Year'] == 2022]

home_performance = matches_2022[
    ['home_team', 'home_score', 'away_score']
].copy()
# Without .copy(): "Here's a window looking at part of the original."
# With .copy(): "Here's your own photocopy. Do whatever you want to it."
home_performance=home_performance.rename(
    columns={
        'home_team': 'Team',
        'home_score': 'Goals_Scored',
        'away_score': 'Goals_Conceded'
    }
)


away_performance = matches_2022[
    ['away_team', 'away_score', 'home_score']
].copy()

away_performance = away_performance.rename(
    columns={
        'away_team':'Team',
        'away_score':'Goals_Scored',
        'home_score':'Goals_Conceded'
    }
)


team_match_performance = pd.concat(
    [home_performance,away_performance],
    ignore_index=True
)

#print(team_match_performance.shape)

team_groups = team_match_performance.groupby('Team')

team_performance_2022 = team_groups.agg(
    Matches_Played=('Team','count'),
    Goals_Scored=('Goals_Scored','sum'),
    Goals_Conceded=('Goals_Conceded','sum')
).reset_index()

team_performance_2022['Goal_Difference'] = (
    team_performance_2022['Goals_Scored'] - team_performance_2022['Goals_Conceded']
)

team_performance_2022['Goal_Difference_Per_Match'] = (
                    team_performance_2022['Goal_Difference']
                    / team_performance_2022['Matches_Played']
                    )

team_performance_2022 = team_performance_2022.sort_values(by='Goal_Difference_Per_Match',
                                                          ascending=False)

"""
print(team_performance_2022[
        [
            'Team',
            'Matches_Played',
            'Goals_Scored',
            'Goals_Conceded',
            'Goal_Difference',
            'Goal_Difference_Per_Match'
            ]
    ]
)
"""

print('=' * 70)

rankings = pd.read_csv("data/raw/fifa_ranking_2022-10-06.csv")

"""
print(
    rankings[
        ['team', 'team_code', 'rank']
    ].head(10)
)

print('How Many are there in both datasets?')
print(
    team_performance_2022['Team'].isin(
        rankings['team']
    ).value_counts()
)

print('Which is not there?')
print(
    team_performance_2022[
        ~team_performance_2022['Team'].isin(rankings['team'])
    ]['Team']
)

print('What anomaly?')
print(
    rankings[
        rankings['team_code'] == 'USA'
    ][
        ['team', 'team_code', 'rank']
    ]
)
"""

#Normalize the team name for USA to match the other dataset
rankings['team'] = rankings['team'].replace('USA','United States')

#Check if the normalization worked
"""
print(
    rankings[
        rankings['team'] == 'United States'
    ][
        ['team', 'team_code', 'rank']
    ]
)
"""

#Merge the two datasets on team name

hypothesis_data = pd.merge(
    team_performance_2022,
    rankings[['team','rank']],
    left_on='Team',
    right_on='team',
    how='inner'
)

#print(hypothesis_data.shape)

hypothesis_data = hypothesis_data[
    [
        'Team',
        'rank',
        'Matches_Played',
        'Goal_Difference',
        'Goal_Difference_Per_Match'
    ]
]

hypothesis_data = hypothesis_data.sort_values(by='rank')

print(hypothesis_data[[
        'Team','rank','Goal_Difference_Per_Match']
    ]
)

print()
print("=" * 70)
print("HYPOTHESIS #1 — FIFA RANKING vs WORLD CUP PERFORMANCE")
print("=" * 70)

print()
print("Spearman Correlation Test")
spearman_correlation, spearman_p_value = spearmanr(
    hypothesis_data['rank'],
    hypothesis_data['Goal_Difference_Per_Match']
)
print("Spearman Correlation:", spearman_correlation)
print("Spearman P-Value:", spearman_p_value) 

print()

print("Pearson Correlation Test")
pearson_correlation, pearson_p_value = pearsonr(
    hypothesis_data['rank'],
    hypothesis_data['Goal_Difference_Per_Match']
)
print("Pearson Correlation:", pearson_correlation)
print("Pearson P-Value:", pearson_p_value)

print()
print(
    "Conclusion: There is a statistically significant negative association "
    "between pre-tournament FIFA ranking and Goal Difference Per Match "
    "in the 2022 FIFA World Cup. Better-ranked teams generally tended "
    "to achieve stronger goal-difference performance per match."
)

print()
print(
    "Statistical Decision: Reject the Null Hypothesis (H0) at the 5% "
    "significance level."
)

print()
print(
    "Note: The analysis identifies an association between FIFA ranking "
    "and performance; it does not establish causation."
)

print()

plt.scatter(
    hypothesis_data['rank'],
    hypothesis_data['Goal_Difference_Per_Match']
)
plt.xlabel('FIFA Ranking (Lower is Better)')
plt.ylabel('Goal Difference Per Match')
plt.title('FIFA Ranking vs Goal Difference Per Match - 2022 World Cup')


project_root = Path(__file__).resolve().parent.parent

visuals_dir = project_root / "visuals" / "hypothesis_1"
visuals_dir.mkdir(parents=True, exist_ok=True)

plt.savefig(
    visuals_dir / "fifa_rank_vs_gd_per_match_2022.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()