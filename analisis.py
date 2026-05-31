import pandas as pd
import pycountry
import scipy
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf


# read csv
path = "./datasets"
edu = pd.read_csv(f"{path}/SE.XPD.TOTL.GD.ZS.csv", skiprows=4)
gdp = pd.read_csv(f"{path}/NY.GDP.MKTP.KD.ZG.csv", skiprows=4)


# Leave only countries
valid_codes = {c.alpha_3 for c in pycountry.countries}
edu = edu[edu["Country Code"].isin(valid_codes)]
gdp = gdp[gdp["Country Code"].isin(valid_codes)]


# Convert wide format to long format (one row per country per year)
year_cols = [c for c in edu.columns if c.isdigit()]
edu_long = edu.melt(
    id_vars=["Country Name", "Country Code"],
    value_vars=year_cols,
    var_name="year",
    value_name="edu",
)
gdp_long = gdp.melt(
    id_vars=["Country Name", "Country Code"],
    value_vars=year_cols,
    var_name="year",
    value_name="gdp_growth",
)
edu_long["year"] = edu_long["year"].astype(int)
gdp_long["year"] = gdp_long["year"].astype(int)


# Join two datasets for convenience
df = edu_long.merge(gdp_long, on=["Country Name", "Country Code", "year"])
df = df.dropna(subset=["edu", "gdp_growth"])


# Remove outliers
# edu > 20 is too high (data error), edu < 0.01 is almost zero (missing data)
# gdp extremes are wars, oil booms and other special events
df = df[df['edu'] <= 20]
df = df[df['edu'] >= 0.01]
df = df[df['gdp_growth'] <= 40]
df = df[df['gdp_growth'] >= -30]


print("=" * 50)
print("DATASET")
print("=" * 50)
print(f"Shape: {df.shape}")
print(df.head())
print(df.describe())


# show distributions
def construct_distribution_plot():
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].hist(df["edu"], bins=40, edgecolor="white")
    axes[0].set_title("Education expenditure (% of GDP)")
    axes[0].set_xlabel("edu")
    axes[1].hist(df["gdp_growth"], bins=40, edgecolor="white")
    axes[1].set_title("GDP growth (annual %)")
    axes[1].set_xlabel("gdp_growth")
    plt.tight_layout()
    plt.savefig("images/distributions.png", dpi=150)
    # plt.show()
construct_distribution_plot()


print("\n" + "=" * 50)
print("SPEARMAN CORRELATION")
print("=" * 50)
corr, p_corr = scipy.stats.spearmanr(df['edu'], df['gdp_growth'])
print(f"r = {corr:.4f}, p = {p_corr:.2e}")


# scatter plot with trend line
def construct_scatter_plot():
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.regplot(
        data=df, x="edu", y="gdp_growth", ax=ax,
        scatter_kws={"alpha": 0.2, "s": 10},
        line_kws={"color": "red"},
    )
    ax.set_title("Education expenditure vs GDP growth")
    ax.set_xlabel("Education expenditure (% of GDP)")
    ax.set_ylabel("GDP growth (annual %)")
    plt.tight_layout()
    plt.savefig("images/scatter.png", dpi=150)
    # plt.show()
construct_scatter_plot()


# t-test: compare OECD (developed) vs non-OECD (developing) countries
print("\n" + "=" * 50)
print("T-TEST: OECD vs NON-OECD")
print("=" * 50)
oecd = [
    'AUS', 'AUT', 'BEL', 'CAN', 'CHL', 'COL', 'CRI', 'CZE', 'DNK',
    'EST', 'FIN', 'FRA', 'DEU', 'GRC', 'HUN', 'ISL', 'IRL', 'ISR',
    'ITA', 'JPN', 'KOR', 'LVA', 'LTU', 'LUX', 'MEX', 'NLD', 'NZL',
    'NOR', 'POL', 'PRT', 'SVK', 'SVN', 'ESP', 'SWE', 'CHE', 'TUR',
    'GBR', 'USA',
]
df['is_oecd'] = df['Country Code'].isin(oecd)
developed = df[df['is_oecd']]
developing = df[~df['is_oecd']]
t_gdp, p_gdp = scipy.stats.ttest_ind(developed['gdp_growth'], developing['gdp_growth'])
t_edu, p_edu = scipy.stats.ttest_ind(developed['edu'], developing['edu'])
print(f"gdp_growth: t={t_gdp:.3f}, p={p_gdp:.4f}")
print(f"edu:        t={t_edu:.3f}, p={p_edu:.4f}")
print(df.groupby('is_oecd')[['edu', 'gdp_growth']].mean())


# OLS regression: edu as a predictor of gdp_growth
print("\n"+ "=" * 78)
model = smf.ols('gdp_growth ~ edu', data=df).fit()
print(model.summary())
