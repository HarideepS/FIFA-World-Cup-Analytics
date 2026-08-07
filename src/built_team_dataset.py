import pandas as pd

pd.set_option('display.max_columns', None)

df =pd.read_csv("data/raw/matches_1930_2022.csv")

home_matches = df[['home_team', 'away_team', 'home_score', 'away_score', 'Year']]

away_matches = df[['away_team', 'home_team', 'away_score', 'home_score', 'Year']]

away_matches.columns = [
    'Team',
    'Opponent',
    'Goals_Scored',
    'Goals_Conceded',
    'Year'
]

home_matches.columns = [
    'Team',
    'Opponent',
    'Goals_Scored',
    'Goals_Conceded',
    'Year'
]

team_matches = pd.concat([home_matches, away_matches], ignore_index=True)

print(team_matches.shape)

#print(team_matches['Team'].unique())

#print(team_matches['Team'].value_counts())

#print(team_matches.groupby('Team')['Goals_Scored'].size())

#print(team_matches.groupby('Team')['Goals_Scored'].sum())


team_matches['Win'] = (
    team_matches['Goals_Scored'] > team_matches['Goals_Conceded']
).astype(int)

team_matches['Draw'] = (
    team_matches['Goals_Scored'] == team_matches['Goals_Conceded'] 
).astype(int)

team_matches['Loss'] = (
    team_matches['Goals_Scored'] < team_matches['Goals_Conceded']
).astype(int)

summary = (team_matches
    .groupby('Team')
    .agg(
        Participations=('Year', 'nunique'),
        Matches_Played=('Team', 'size'),
        Goals_Scored=('Goals_Scored', 'sum'),
        Goals_Conceded=('Goals_Conceded', 'sum'),
        Wins=('Win', 'sum'),
        Draws=('Draw', 'sum'),
        Losses=('Loss', 'sum')
        )
        .reset_index()
    )   

summary['Goals_Per_Match'] = summary['Goals_Scored'] / summary['Matches_Played']

summary['Avg_Matches_Per_Tournament'] = summary['Matches_Played'] / summary['Participations']

summary['Goal_Difference'] = summary['Goals_Scored'] - summary['Goals_Conceded']

summary['Win_Percentage'] = summary['Wins'] / summary['Matches_Played']

# ===================================
# Validation Checks
# ===================================
assert (
    (
        team_matches['Win']
        + team_matches['Draw']
        + team_matches['Loss']
    ) == 1
).all(), "Validation Failed: Every match must have exactly one outcome."

assert (
    summary['Goal_Difference']
    ==
    summary['Goals_Scored']
    - summary['Goals_Conceded']
).all(), "Validation Failed: Goal Difference calculation is incorrect."

summary = summary[
    [
        'Team',

        # Experience
        'Participations',
        'Matches_Played',
        'Avg_Matches_Per_Tournament',

        # Match Results
        'Wins',
        'Draws',
        'Losses',
        'Win_Percentage',

        # Goal Statistics
        'Goals_Scored',
        'Goals_Conceded',
        'Goal_Difference',
        'Goals_Per_Match'
    ]
]

summary = summary.sort_values(
    by='Participations',
    ascending=False
)

print(summary.head(3))

