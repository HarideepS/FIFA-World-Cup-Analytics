# Hypothesis #1 — FIFA Ranking vs World Cup Performance

## Research Question:

Does a team's pre-tournament FIFA ranking have a significant relationship with its performance in the FIFA World Cup?

## Scope

Tournament: FIFA World Cup 2022
Teams: 32
Performance Metric: Goal Difference Per Match
Ranking Snapshot: FIFA rankings dated 6 October 2022, immediately preceding the tournament

## Hypotheses

Null Hypothesis (H₀):
There is no statistically significant relationship between pre-tournament FIFA ranking and Goal Difference Per Match in the 2022 FIFA World Cup.

Alternative Hypothesis (H₁):
There is a statistically significant relationship between pre-tournament FIFA ranking and Goal Difference Per Match in the 2022 FIFA World Cup.

## Variables

| Variable                    | Role                     | Description                               |
| --------------------------- | ------------------------ | ----------------------------------------- |
| `rank`                      | X / Independent Variable | Pre-tournament FIFA ranking               |
| `Goal_Difference_Per_Match` | Y / Dependent Variable   | Goal difference divided by matches played |

Goal Difference:
Goals Scored − Goals Conceded

Goal Difference Per Match:
Goal Difference ÷ Matches Played

#### Using GD/Match instead of raw Goal Difference helps account for differences in the number of matches played.

## Data Preparation

The 64 matches from the 2022 FIFA World Cup were transformed from match-level data into a team-level performance dataset.

Each match was converted into two team-level observations:
Home team's performance
Away team's performance

This produced:
64 matches → 128 team-match observations → 32 team-level records

The team-level dataset was then used to calculate:

Matches Played
Goals Scored
Goals Conceded
Goal Difference
Goal Difference Per Match

The team-level performance data was then merged with the FIFA ranking snapshot using team names.

## Data Quality Challenge — Entity Matching

One entity-matching inconsistency was identified:
Performance dataset → United States
FIFA ranking data → USA

The FIFA ranking dataset contained:
USA → Rank 16

The team name was standardized to United States before merging.

This allowed all 32/32 teams to be successfully matched.

Challenge classification: Dataset entity/name standardization.

## Statistical Analysis

### Spearman Rank Correlation

Correlation = -0.5923
p-value = 0.000355

The negative correlation indicates that higher numerical FIFA rank values (weaker ranking positions) tend to be associated with lower Goal Difference Per Match.

Since:
0.000355 < 0.05
the relationship is statistically significant at the 5% significance level.

### Pearson Correlation

Correlation = -0.5443
p-value = 0.001281

Pearson also identifies a statistically significant negative relationship.

The similarity between the Spearman and Pearson results provides supporting evidence that the observed relationship is not dependent on using only one correlation method.

## Hypothesis Decision:

Reject H₀

Both statistical tests produced p-values below the 0.05 significance threshold.

Therefore:
There is statistically significant evidence of an association between pre-tournament FIFA ranking and Goal Difference Per Match in the 2022 FIFA World Cup.

## Interpretation

Better-ranked teams generally tended to achieve stronger Goal Difference Per Match performance during the 2022 FIFA World Cup.

However, the analysis establishes association, not causation. FIFA ranking should therefore not be interpreted as directly causing World Cup performance.

## Visual Evidence

A scatter plot of:
X: FIFA Ranking
Y: Goal Difference Per Match

showed the same overall negative trend identified by the correlation analysis.

The relationship was not perfectly linear, with several teams deviating from the general pattern, demonstrating that FIFA ranking does not completely determine tournament performance.

## Final H1 Conclusion:

Hypothesis #1 is supported. The analysis found a statistically significant negative association between pre-tournament FIFA ranking and Goal Difference Per Match in the 2022 FIFA World Cup. Both Spearman (ρ = -0.5923, p < 0.001) and Pearson (r = -0.5443, p = 0.0013) correlation tests support this finding. Better-ranked teams generally demonstrated stronger goal-difference performance per match, although the relationship represents an association rather than causation.
