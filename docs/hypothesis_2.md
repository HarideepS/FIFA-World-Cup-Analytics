# Hypothesis 2 — Team Market Value vs World Cup Progression

## Hypothesis

> Teams with greater market value tend to progress further in the FIFA World Cup.

## Objective

Test whether a team's market value was positively associated with how far it progressed in the 2022 FIFA World Cup.

---

## Data Sources

### 1. Team Market Value

Source: Transfermarkt — 2022 FIFA World Cup participating teams.

The dataset contains the total market value of each of the 32 participating teams.

Market values were standardized to **€ millions**.

### 2. Match Data

Source: `data/raw/matches_1930_2022.csv`

Used to determine the furthest stage reached by each team based on the `Round` field.

### 3. Tournament Summary

Source: `data/raw/world_cup.csv`

Used to distinguish the 2022 World Cup champion from the runner-up, since both teams appear in the `Final` round.

---

## Variables

| Variable             | Type        | Description                              |
| -------------------- | ----------- | ---------------------------------------- |
| `Team`               | Categorical | National team                            |
| `Market_Value_EUR_M` | Continuous  | Total team market value in € millions    |
| `Progression_Level`  | Ordinal     | Furthest stage reached in the tournament |

### Progression Encoding

| Outcome        | Progression Level |
| -------------- | ----------------: |
| Group Stage    |                 0 |
| Round of 16    |                 1 |
| Quarter-finals |                 2 |
| Semi-finals    |                 3 |
| Runner-up      |                 4 |
| Champion       |                 5 |

The third-place match was assigned the same progression level as the semi-finals because participating in the third-place match does not represent progression beyond the semi-final stage.

---

## Methodology

The 2022 World Cup matches were filtered from the historical match dataset.

Home and away team appearances were combined into a single team-round dataset. Each tournament round was mapped to an ordered progression level.

For each team, the maximum progression level was used to determine its furthest stage reached.

The champion was then identified from the tournament summary and assigned progression level `5`.

Team names were normalized where necessary to ensure consistency across datasets:

- `IR Iran` → `Iran`
- `Korea Republic` → `South Korea`

The resulting progression data was merged with the market-value dataset using `Team` as the key.

The final analytical dataset contained **32 teams**.

---

## Statistical Analysis

### Primary Test — Spearman Rank Correlation

Spearman correlation was selected as the primary test because tournament progression is an **ordinal variable**.

**Result:**

- Spearman correlation (ρ): **0.6312**
- P-value: **0.000107**

The positive coefficient indicates a positive monotonic association between team market value and tournament progression.

Since:

`p < 0.05`

the null hypothesis is rejected at the 5% significance level.

### Supporting Test — Pearson Correlation

Pearson correlation was used as a supporting analysis to assess the linear association between market value and the numerically encoded progression level.

**Result:**

- Pearson correlation (r): **0.6122**
- P-value: **0.000196**

The Pearson result also indicates a statistically significant positive relationship.

---

## Statistical Decision

**Reject the Null Hypothesis (H₀) at the 5% significance level.**

The analysis provides statistically significant evidence of a positive association between team market value and tournament progression in the 2022 FIFA World Cup.

---

## Conclusion

Teams with greater market value **tended to progress further** in the 2022 FIFA World Cup.

The Spearman correlation of **0.6312** indicates a moderate-to-strong positive monotonic association. The supporting Pearson correlation of **0.6122** also indicates a positive linear relationship.

However, the results demonstrate **association, not causation**. Market value may reflect several underlying factors, including player quality, squad depth, experience, and other resources that may also influence tournament performance.

Therefore, the analysis does not establish that higher market value causes teams to progress further.

---

## Visualization

The relationship between team market value and tournament progression is visualized in:

`visuals/hypothesis_2/market_value_vs_progression_2022.png`

---

## Result Summary

| Metric               |                   Result |
| -------------------- | -----------------------: |
| Teams analyzed       |                       32 |
| Spearman ρ           |               **0.6312** |
| Spearman p-value     |             **0.000107** |
| Pearson r            |               **0.6122** |
| Pearson p-value      |             **0.000196** |
| Significance level   |                 **0.05** |
| Statistical decision |            **Reject H₀** |
| Conclusion           | **Positive association** |
