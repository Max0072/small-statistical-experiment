# Does Education Spending Drive Economic Growth?
### A Cross-Country Statistical Analysis


---

## 1. Research Question
We will try to find out if the government spends on education are associated with economic growth across countries and over time. Specifically: Do countries that spend more on education grow faster economically?

This question is motivated by **human capital theory**, which says that investment in education raises labor productivity and therefore speeds up economic growth. However, the relationship is more complicated because of reverse causality, confounding variables, and the long lag between education investment and its economic returns.

---

## 2. Dataset

### 2.1 Data Sources
We got two indicators from the World Bank Open Data portal:

`SE.XPD.TOTL.GD.ZS` - Government expenditure on education (% of GDP)

`NY.GDP.MKTP.KD.ZG` - GDP growth rate (annual %)

The dataset covers up to 215 countries over 1960–2024.

### 2.2 Sample Construction and Correctness
- Within-country observations across years are not independent, a country's education spending is correlated with previous year spending.

- Countries lacking education data are systematically different: they tend to be poorer, conflict-affected, and institutionally weaker. 

### 2.3 Data Cleaning and Outlier Handling
We applied the following cleaning steps:

1. Excluded regional and income-group aggregates using `pycountry`, leaving only sovereign countries.
2. Removed observations with `edu > 20%` — implausibly high values likely caused by data errors.
3. Removed observations with `edu < 0.01%` — effectively zero, likely missing values coded as zero.
4. Excluded extreme GDP growth values above 40% and below −30%, corresponding to post-war recoveries (Kuwait 1992), COVID-19 shocks (Macao 2020, Maldives 2020), and volatile small island economies. These are real events but distort the overall regression.

After cleaning, the final dataset contains 5,047 observations.

**Descriptive statistics (after cleaning):**

| Variable | Mean | Std Dev | Min | Median | Max |
|---|---|---|---|---|---|
| Education spending (% GDP) | 4.28% | 1.89 | 0.32% | 4.15% | 16.4% |
| GDP growth (annual %) | 3.55% | 4.90 | −24.4% | 3.71% | 37.5% |

---

## 3. Statistical Analysis

### 3.1 Methods

**Spearman correlation** — measures how strong the relationship between edu and gdp_growth is. We use Spearman instead of Pearson because the distributions are not normal.

**OLS regression** — fits a line through the data to see the direction and size of the effect. Results are descriptive, not causal.

**t-test (OECD vs non-OECD)** — checks if the average edu and gdp_growth are significantly different between developed and developing countries.

### 3.2 Results

#### Spearman Correlation

| Statistic | Value |
|---|---|
| Spearman ρ | **−0.149** |
| p-value | 1.78 × 10⁻²⁶ |
| N | 5,047 |

Weak negative relationship. Countries that spend more on education tend to grow slightly slower.

#### OLS Regression

```
gdp_growth ~ edu
```

| Term | Coefficient | Std Error | t | p-value | 95% CI |
|---|---|---|---|---|---|
| Intercept | 4.900 | 0.170 | 28.89 | < 0.001 | [4.57, 5.23] |
| Education spending | **−0.316** | 0.036 | −8.72 | < 0.001 | [−0.39, −0.25] |

| Model Statistic | Value |
|---|---|
| R² | **0.015** |
| Adjusted R² | 0.015 |
| F-statistic | 76.07 (p < 0.001) |
| Durbin-Watson | 1.651 |

Each extra 1% of GDP spent on education is linked to a 0.316 p.p. drop in GDP growth. But R² = 0.015 — edu explains only 1.5% of the variance. The model has almost no predictive power.

#### t-test: OECD vs. Non-OECD

| Variable | Non-OECD Mean | OECD Mean | t-statistic | p-value |
|---|---|---|---|---|
| Education spending (% GDP) | 4.03% | 4.95% | 15.70 | < 0.001 |
| GDP growth (annual %) | 3.82% | 2.79% | −6.66 | < 0.001 |

Both differences are significant. OECD countries spend more on education but grow slower — because rich countries always grow slower than developing ones.

### 3.3 Interpretation
The negative correlation is real, but it does not prove that education spending causes slower growth. It most likely exists because of the following reasons:

- Rich countries spend more on education simply because they can afford it — and rich countries grow slower by default, since they are already developed.
- Developing countries grow fast due to catch-up growth (adopting existing technologies), not because they spend less on education.
- We compare spending and growth in the same year, but education affects the economy with a delay of 10–30 years.

So the correlation reflects the structure of the data, not a real causal effect.

---

## 4. Discussion and Further Research

### 4.1 Limitations
- We compare education spending and GDP growth in the same year. In reality, education affects the economy after 10–30 years.
- No control variables: income level, institutions, geography.
- Countries with missing data tend to be poorer and less stable, so the sample is biased toward richer countries.

### 4.2 What to do next
- Add GDP per capita as a control variable to account for development level.
- Use shifted edu (spending 10 years ago) to capture delayed effects.
- Use country fixed effects to compare each country to itself over time instead of comparing different countries.

---

## 5. Conclusion
We found a weak negative correlation between education spending and GDP growth, but it doesn't mean that education slows down the growth.

A simple two-variable analysis is not enough to study this question. You may need shifted data and proper controls.
