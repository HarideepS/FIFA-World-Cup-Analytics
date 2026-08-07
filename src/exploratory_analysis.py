import pandas as pd

team_summary = pd.read_csv("data/processed/team_performance_summary.csv")

SECTION = "=" * 70
SUBSECTION = "-" * 70

#ANALYSIS: LEGACY & LONGEVITY

print(SECTION)
print("LEGACY & LONGEVITY")
print(SECTION)

print()
print("Top 10 Teams by FIFA World Cup Participations (1930-2022)")
print(SUBSECTION)
print(
    team_summary
        .sort_values(by='Participations',ascending=False)
    [
        ['Team' ,'Participations']
    ].head(10)
)
print()
print("Insight:")
print(
    "Brazil is the only nation to have participated in all 22 FIFA World Cups, "
    "while the remaining historically successful teams are closely grouped "
    "between 16 and 18 appearances, highlighting Brazil's unmatched consistency."
)
print()


print()
print("Top 10 Teams by Matches Played in FIFA World Cup (1930-2022)")
print(SUBSECTION)
print(
    team_summary
    .sort_values(by='Matches_Played', ascending=False)
    [
        ['Team','Matches_Played']
    ].head(10)
)
print()
print("Insight:")
print(
   "The rankings remain largely consistent with the participation leaderboard, "
   "suggesting that teams with frequent World Cup appearances also accumulate the highest number of matches,"
    "through sustained qualification over decades."
)
print()


print()
print("Top 10 Teams by Wins in FIFA World Cup (1930-2022)")
print(SUBSECTION)
print(
    team_summary
    .sort_values(by='Wins', ascending=False)
    [
        ['Team','Wins']
    ].head(10)
)
print()
print("Insight:")
print(
    "Brazil continues to lead in total World Cup wins, " 
    "while historical team separation (e.g., Germany and West Germany) influences the overall rankings, "
    "demonstrating how entity representation can affect cumulative historical statistics."
)
print()


print()
print("Top 10 Teams by Goals Scored in FIFA World Cup (1930-2022)")
print(SUBSECTION)
print(
    team_summary
    .sort_values(by='Goals_Scored', ascending=False)
    [
        ['Team','Goals_Scored']
    ].head(10)
)
print()
print("Insight:")
print(
     "Brazil's lead in total World Cup goals reflects its sustained attacking "
    "success across multiple tournaments, while the separation of Germany and "
    "West Germany distributes their historical goal totals across two entities."
)
print()

#ANALYSIS: EFFICIENCY

print(SECTION)
print("EFFICIENCY")
print(SECTION)

experienced_teams = team_summary[
    team_summary['Participations'] >= 5
    ]

print()
print("Top 10 Teams by Win Percentage (Minimum 5 Participations)")
print(SUBSECTION)
print(
    experienced_teams
    .sort_values(by='Win_Percentage', ascending=False)
    [
        ['Team','Participations','Win_Percentage']
    ].head(10)
)
print()
print("Insight:")
print(
    "Applying a minimum participation threshold produces a fairer comparison by "
    "reducing the influence of teams with very small sample sizes, highlighting "
    "consistently successful nations over multiple tournaments."
)
print()


print()
print("Top 10 Teams by Goals Per Match (Minimum 5 Participations)")
print(SUBSECTION)
print(
    experienced_teams
    .sort_values(by='Goals_Per_Match', ascending=False)
    [
        ['Team','Participations','Goals_Per_Match']
    ].head(10)
)
print()
print("Insight:")
print(
    "Filtering by experienced teams emphasizes sustained attacking efficiency, "
    "ensuring the rankings are not dominated by nations with only a few World Cup matches."
)
print()


#ANALYSIS: DOMINANCE

print(SECTION)
print("DOMINANCE")
print(SECTION)

print()
print("Top 10 Teams by Goal Difference")
print(SUBSECTION)
print(
    team_summary
    .sort_values(by="Goal_Difference", ascending=False)
    [
        ['Team','Goal_Difference']
    ].head(10)
)
print()
print("Insight:")
print(
    "Goal Difference reflects long-term dominance by balancing attacking output "
    "with defensive strength across multiple World Cup campaigns."
)
print()


print()
print("Top 10 Team by Goal Difference Per Match (Minimum 5 Participations)")
print(SUBSECTION)
print(
    experienced_teams
    .sort_values(by='Goal_Difference_Per_Match', ascending=False)
    [
        ['Team','Participations','Goal_Difference_Per_Match']
    ].head(10)
)
print()
print("Insight:")
print(
    "Normalizing Goal Difference by matches played provides a fairer measure of "
    "dominance by accounting for differences in tournament longevity."
)
print()