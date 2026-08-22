import pandas as pd
import numpy as np

matches= pd.read_csv(
    "data/raw/matches_1930_2022.csv"
)

#Team Normalization

all_teams = sorted(
    pd.concat([
        matches['home_team'],
        matches['away_team']
    ]).unique()
)

#No.of Unique Teams
print(f'Unique raw team names: {len(all_teams)}')

team_normalization = {

    # Naming standardization
    'IR Iran': 'Iran',
    'Korea Republic': 'South Korea',
    'China PR': 'China',
    'Türkiye': 'Turkey',

    # Historical continuity
    'West Germany': 'Germany',
    'Germany DR': 'Germany',

    'Czechoslovakia': 'Czech Republic',

    'Dutch East Indies': 'Indonesia',

    'Soviet Union': 'Russia',

    'Yugoslavia': 'Serbia',
    'FR Yugoslavia': 'Serbia',
    'Serbia and Montenegro': 'Serbia'
}

matches['home_team_standardized'] = (
    matches['home_team']
    .replace(team_normalization)
)

matches['away_team_standardized'] = (
    matches['away_team']
    .replace(team_normalization)
)

raw_teams = set(
    pd.concat([
        matches['home_team'],
        matches['away_team']
    ]).unique()
)

standardized_teams = set(
    pd.concat([
        matches['home_team_standardized'],
        matches['away_team_standardized']
    ]).unique()
)
"""
print("Raw team names:", len(raw_teams))
print("Standardized team names:", len(standardized_teams))

normalization_changes = (
    matches[
        matches['home_team'] != matches['home_team_standardized']
    ][
        ['home_team', 'home_team_standardized']
    ]
    .drop_duplicates()
    .sort_values('home_team')
)

print(normalization_changes.to_string(index=False))

normalization_changes_away = (
    matches[
        matches['away_team'] != matches['away_team_standardized']
    ][
        ['away_team', 'away_team_standardized']
    ]
    .drop_duplicates()
    .sort_values('away_team')
)

print(normalization_changes_away.to_string(index=False))
"""

raw_team_history = pd.concat([
    matches[['Year', 'home_team']]
        .rename(columns={'home_team': 'Team'}),

    matches[['Year', 'away_team']]
        .rename(columns={'away_team': 'Team'})
]).drop_duplicates()

raw_standardized = raw_team_history.copy()

raw_standardized['Team_Standardized'] = (
    raw_standardized['Team']
    .replace(team_normalization)
)

collapsed = (
    raw_standardized
    .groupby(['Year', 'Team_Standardized'])['Team']
    .nunique()
)

print(
    collapsed[collapsed > 1]
)

for canonical_team, group in (
    raw_standardized
    .groupby(['Year', 'Team_Standardized'])
):
    if len(group) > 1:
        print(canonical_team)
        print(group)
        print()


team_history = pd.concat([
    matches[['Year', 'home_team']]
        .rename(columns={'home_team': 'Team'}),

    matches[['Year', 'away_team']]
        .rename(columns={'away_team': 'Team'})
]).drop_duplicates()

team_history['Historical_Team'] = (
    team_history['Team']
    .replace(team_normalization)
)

team_history = (
    team_history
    .sort_values(['Historical_Team', 'Year'])
    .reset_index(drop=True)
)

print(team_history.shape)
print(
    team_history.duplicated(['Year', 'Team']).sum()
)
print(
    team_history.duplicated(['Year', 'Historical_Team']).sum()
)
"""
print(
    team_history[
        team_history['Historical_Team'] == 'Germany'
    ]
)
"""
historical_editions = (
    team_history[
        ['Historical_Team', 'Year']
    ]
    .drop_duplicates()
    .sort_values(['Historical_Team', 'Year'])
)

historical_editions['Previous_WC_Editions'] = (
    historical_editions
    .groupby('Historical_Team')
    .cumcount()
)

team_history = team_history.merge(
    historical_editions[
        ['Historical_Team', 'Year', 'Previous_WC_Editions']
    ],
    on=['Historical_Team', 'Year'],
    how='left'
)
"""
print(
    team_history[
        team_history['Historical_Team'] == 'Germany'
    ][
        ['Year', 'Team', 'Historical_Team', 'Previous_WC_Editions']
    ]
    .to_string(index=False)
)
"""
home_matches = (
    matches[
        ['Year', 'home_team_standardized']
    ]
    .rename(columns={
        'home_team_standardized': 'Historical_Team'
    })
)

away_matches = (
    matches[
        ['Year', 'away_team_standardized']
    ]
    .rename(columns={
        'away_team_standardized': 'Historical_Team'
    })
)

historical_matches = pd.concat(
    [home_matches, away_matches],
    ignore_index=True
)

matches_per_edition = (
    historical_matches
    .groupby(['Historical_Team', 'Year'])
    .size()
    .reset_index(name='Matches_Played')
)
"""
print(
    matches_per_edition[
        matches_per_edition['Historical_Team'] == 'Germany'
    ].to_string(index=False)
)
"""

matches_per_edition = (
    matches_per_edition
    .sort_values(['Historical_Team', 'Year'])
)

matches_per_edition['Previous_WC_Matches'] = (
    matches_per_edition
    .groupby('Historical_Team')['Matches_Played']
    .cumsum()
    - matches_per_edition['Matches_Played']
)

team_history = team_history.merge(
    matches_per_edition[
        [
            'Historical_Team',
            'Year',
            'Previous_WC_Matches'
        ]
    ],
    on=['Historical_Team', 'Year'],
    how='left'
)
home_results = (
    matches[
        ['Year', 'home_team',
         'home_score', 'away_score']
    ]
    .rename(columns={
        'home_team': 'Team',
        'home_score': 'Team_Score',
        'away_score': 'Opponent_Score'
    })
)

home_results['Result'] = np.select(
    [
        home_results['Team_Score'] > home_results['Opponent_Score'],
        home_results['Team_Score'] < home_results['Opponent_Score']
    ],
    [
        'Win',
        'Loss'
    ],
    default='Draw'
)


away_results = (
    matches[
        ['Year', 'away_team',
         'away_score', 'home_score']
    ]
    .rename(columns={
        'away_team': 'Team',
        'away_score': 'Team_Score',
        'home_score': 'Opponent_Score'
    })
)

away_results['Result'] = np.select(
    [
        away_results['Team_Score'] > away_results['Opponent_Score'],
        away_results['Team_Score'] < away_results['Opponent_Score']
    ],
    [
        'Win',
        'Loss'
    ],
    default='Draw'
)


team_results = pd.concat(
    [home_results, away_results],
    ignore_index=True
)


performance = (
    team_results
    .groupby(['Team', 'Year'])
    .agg(
        Matches_Played=('Result', 'size'),
        Wins=('Result', lambda x: (x == 'Win').sum())
    )
    .reset_index()
)

performance['Win_Percentage'] = (
    performance['Wins']
    / performance['Matches_Played']
    * 100
)

print(
    matches[
        (matches['Year'] == 1974) &
        (
            matches['home_team'].isin(['Germany DR', 'West Germany']) |
            matches['away_team'].isin(['Germany DR', 'West Germany'])
        )
    ][
        ['Year', 'home_team', 'away_team', 'home_score', 'away_score']
    ].to_string(index=False)
)

print(
    team_results[
        (team_results['Year'] == 1974)
    ]['Team'].unique()
)

print(performance.shape)

# ============================================================
# TOURNAMENT PROGRESSION STRUCTURE
# ============================================================

tournament_stage_order = {

    1930: [
        'Group stage',
        'Semi-finals',
        'Final'
    ],

    1934: [
        'Round of 16',
        'Quarter-finals',
        'Semi-finals',
        'Final'
    ],

    1938: [
        'Round of 16',
        'Quarter-finals',
        'Semi-finals',
        'Final'
    ],

    1950: [
        'Group stage',
        'Final stage'
    ],

    1954: [
        'Group stage',
        'Group stage play-off',
        'Quarter-finals',
        'Semi-finals',
        'Final'
    ],

    1958: [
        'Group stage',
        'Group stage play-off',
        'Quarter-finals',
        'Semi-finals',
        'Final'
    ],

    1962: [
        'Group stage',
        'Quarter-finals',
        'Semi-finals',
        'Final'
    ],

    1966: [
        'Group stage',
        'Quarter-finals',
        'Semi-finals',
        'Final'
    ],

    1970: [
        'Group stage',
        'Quarter-finals',
        'Semi-finals',
        'Final'
    ],

    1974: [
        'First round',
        'Second round',
        'Final'
    ],

    1978: [
        'First round',
        'Second round',
        'Final'
    ],

    1982: [
        'First group stage',
        'Second group stage',
        'Semi-finals',
        'Final'
    ],

    1986: [
        'Group stage',
        'Round of 16',
        'Quarter-finals',
        'Semi-finals',
        'Final'
    ],

    1990: [
        'Group stage',
        'Round of 16',
        'Quarter-finals',
        'Semi-finals',
        'Final'
    ],

    1994: [
        'Group stage',
        'Round of 16',
        'Quarter-finals',
        'Semi-finals',
        'Final'
    ],

    1998: [
        'Group stage',
        'Round of 16',
        'Quarter-finals',
        'Semi-finals',
        'Final'
    ],

    2002: [
        'Group stage',
        'Round of 16',
        'Quarter-finals',
        'Semi-finals',
        'Final'
    ],

    2006: [
        'Group stage',
        'Round of 16',
        'Quarter-finals',
        'Semi-finals',
        'Final'
    ],

    2010: [
        'Group stage',
        'Round of 16',
        'Quarter-finals',
        'Semi-finals',
        'Final'
    ],

    2014: [
        'Group stage',
        'Round of 16',
        'Quarter-finals',
        'Semi-finals',
        'Final'
    ],

    2018: [
        'Group stage',
        'Round of 16',
        'Quarter-finals',
        'Semi-finals',
        'Final'
    ],

    2022: [
        'Group stage',
        'Round of 16',
        'Quarter-finals',
        'Semi-finals',
        'Final'
    ]
}


def build_stage_scores(stages):

    progression_stages = [
        stage
        for stage in stages
        if stage not in ['Final', 'Third-place match']
    ]

    if len(progression_stages) == 1:

        scores = {
            progression_stages[0]: 0.0
        }

    else:

        step = 4 / (len(progression_stages) - 1)

        scores = {
            stage: round(index * step, 2)
            for index, stage in enumerate(progression_stages)
        }

    return scores


stage_scores_by_year = {
    year: build_stage_scores(stages)
    for year, stages
    in tournament_stage_order.items()
}


# Validation
print(
    "Number of tournament structures:",
    len(stage_scores_by_year)
)

print("\n1954:")
for stage, score in stage_scores_by_year[1954].items():
    print(f"  {stage}: {score}")

print("\n1982:")
for stage, score in stage_scores_by_year[1982].items():
    print(f"  {stage}: {score}")


# ============================================================
# MATCH-LEVEL PROGRESSION SCORE
# ============================================================

def get_progression_score(row):

    year = row['Year']
    round_name = row['Round']

    # Final will be resolved later:
    # Champion = 6.0
    # Runner-up = 5.0
    if round_name == 'Final':
        return None

    # Third-place match does not represent progression
    # beyond the semi-final level.
    if round_name == 'Third-place match':
        return 4.0

    return stage_scores_by_year[year][round_name]


matches['Progression_Score'] = (
    matches.apply(
        get_progression_score,
        axis=1
    )
)

print(
    matches[
        ['Year', 'Round', 'Progression_Score']
    ]
    .drop_duplicates()
    .sort_values(
        ['Year', 'Progression_Score']
    )
    .to_string(index=False)
)

def get_progression_score(row):
    year = row['Year']
    round_name = row['Round']

    if round_name == 'Final':
        return None

    if round_name == 'Third-place match':
        return 4.0

    return stage_scores_by_year[year][round_name]

matches['Progression_Score'] = (
    matches.apply(
        get_progression_score,
        axis=1
    )
)


# ============================================================
# FINAL MATCH PROGRESSION
# ============================================================

finals = matches[
    matches['Round'] == 'Final'
].copy()


def get_final_winner(row):

    if row['home_score'] > row['away_score']:
        return row['home_team']

    if row['away_score'] > row['home_score']:
        return row['away_team']

    # Tied score → penalty shootout
    notes = row['Notes']

    if pd.notna(notes) and 'won on penalty kicks' in notes:

        winner = str(notes).split(
            ' won on penalty kicks'
        )[0]

        return winner

    return None

finals['Final_Winner'] = finals.apply(
    get_final_winner,
    axis=1
)

print(
    finals[
        [
            'Year',
            'home_team',
            'away_team',
            'home_score',
            'away_score',
            'Notes',
            'Final_Winner'
        ]
    ].to_string(index=False)
)

final_scores = pd.concat([
    finals[
        ['Year', 'home_team', 'Final_Winner']
    ]
    .rename(columns={'home_team': 'Team'}),

    finals[
        ['Year', 'away_team', 'Final_Winner']
    ]
    .rename(columns={'away_team': 'Team'})
])

final_scores['Progression_Score'] = np.where(
    final_scores['Team'] == final_scores['Final_Winner'],
    6.0,
    5.0
)

final_scores = final_scores.drop(
    columns='Final_Winner'
)

print(
    final_scores.to_string(index=False)
)

print(
    final_scores['Progression_Score'].value_counts()
)

# ============================================================
# FINAL TOURNAMENT PROGRESSION
# ============================================================

# Non-final matches
progression_matches = matches[
    matches['Round'] != 'Final'
].copy()

# Maximum progression reached before the Final
progression_by_team = (
    progression_matches
    .groupby(['Year', 'home_team'])['Progression_Score']
    .max()
    .reset_index()
    .rename(columns={'home_team': 'Team'})
)

away_progression = (
    progression_matches
    .groupby(['Year', 'away_team'])['Progression_Score']
    .max()
    .reset_index()
    .rename(columns={'away_team': 'Team'})
)

progression_by_team = pd.concat(
    [progression_by_team, away_progression],
    ignore_index=True
)

progression_by_team = (
    progression_by_team
    .groupby(['Year', 'Team'])['Progression_Score']
    .max()
    .reset_index()
)

progression_by_team = pd.concat(
    [
        progression_by_team,
        final_scores
    ],
    ignore_index=True
)

progression_by_team = (
    progression_by_team
    .groupby(['Year', 'Team'])['Progression_Score']
    .max()
    .reset_index()
)

def get_final_stage(score):

    if score == 6.0:
        return 'Champion'

    if score == 5.0:
        return 'Runner-up'

    if score == 4.0:
        return 'Semi-finals'

    return None

print(progression_by_team.shape)

print(
    progression_by_team.duplicated(
        ['Year', 'Team']
    ).sum()
)

print(
    progression_by_team[
        progression_by_team['Year'] == 2022
    ]
    .sort_values(
        'Progression_Score',
        ascending=False
    )
    .to_string(index=False)
)

def get_final_stage(row):

    year = row['Year']
    score = row['Progression_Score']

    if score == 6.0:
        return 'Champion'

    if score == 5.0:
        return 'Runner-up'

    stage_scores = stage_scores_by_year[year]

    for stage, stage_score in stage_scores.items():

        if stage_score == score:
            return stage

    return None

progression_by_team['Final_Stage'] = (
    progression_by_team.apply(
        get_final_stage,
        axis=1
    )
)

print(
    progression_by_team['Final_Stage'].isna().sum()
)


# ============================================================
# MERGE TOURNAMENT PROGRESSION
# ============================================================

team_history = team_history.merge(
    progression_by_team[
        [
            'Year',
            'Team',
            'Final_Stage',
            'Progression_Score'
        ]
    ],
    on=['Year', 'Team'],
    how='left',
    validate='one_to_one'
)

print(team_history.shape)

# ============================================================
# MERGE TOURNAMENT PERFORMANCE
# ============================================================

team_history = team_history.merge(
    performance[
        [
            'Year',
            'Team',
            'Matches_Played',
            'Wins',
            'Win_Percentage'
        ]
    ],
    on=['Year', 'Team'],
    how='left',
    validate='one_to_one'
)

print(team_history.shape)

print(
    team_history.columns.tolist()
)

print(
    team_history.isna().sum()
)

print(
    team_history[
        team_history['Year'] == 2022
    ]
    .sort_values(
        'Progression_Score',
        ascending=False
    )
    .to_string(index=False)
)

print(
    team_history[
        (team_history['Year'] == 1974) &
        (
            team_history['Team'].isin(
                ['Germany DR', 'West Germany']
            )
        )
    ].to_string(index=False)
)

print(
    team_history[
        [
            'Previous_WC_Editions',
            'Previous_WC_Matches',
            'Matches_Played',
            'Wins',
            'Win_Percentage',
            'Progression_Score'
        ]
    ].describe()
)

print(
    team_history[
        ['Final_Stage']
    ].value_counts()
)

print(
    team_history[
        ['Year', 'Team']
    ]
    .groupby('Year')
    .size()
)

# ============================================================
# SAVE PROCESSED HISTORICAL WORLD CUP DATASET
# ============================================================

team_history.to_csv(
    "data/processed/historical_world_cup_processed.csv",
    index=False
)

print(
    "Processed historical World Cup dataset saved."
)

print(
    team_history.shape
)