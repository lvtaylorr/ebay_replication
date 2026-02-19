import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Load data
df = pd.read_csv("input/PaidSearch.csv")
df["date"] = pd.to_datetime(df["date"])
df["log_revenue"] = np.log(df["revenue"])

os.makedirs("temp", exist_ok=True)
os.makedirs("output/figures", exist_ok=True)

# Step 2 — Treated pivot
treated_units = df[df["search_stays_on"] == 0]
treated_pivot = treated_units.pivot_table(
    index="dma",
    columns="treatment_period",
    values="log_revenue"
)
treated_pivot.columns = ["log_revenue_pre", "log_revenue_post"]
treated_pivot["log_revenue_diff"] = treated_pivot["log_revenue_post"] - treated_pivot["log_revenue_pre"]

# Save treated pivot
treated_pivot.to_csv("temp/treated_pivot.csv")

# Step 2 — Untreated pivot
untreated_units = df[df["search_stays_on"] == 1]
untreated_pivot = untreated_units.pivot_table(
    index="dma",
    columns="treatment_period",
    values="log_revenue"
)
untreated_pivot.columns = ["log_revenue_pre", "log_revenue_post"]
untreated_pivot["log_revenue_diff"] = untreated_pivot["log_revenue_post"] - untreated_pivot["log_revenue_pre"]

# Save untreated pivot
untreated_pivot.to_csv("temp/untreated_pivot.csv")

# Step 3 — Print summary stats
print(f"Treated DMAs: {treated_units['dma'].nunique()}")
print(f"Untreated DMAs: {untreated_units['dma'].nunique()}")
print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")


# Step 4 — Figure 5.2
# avg revenue per day for treatment/control
daily_rev = (
    df.groupby(["date", "search_stays_on"], as_index=False)["revenue"]
      .mean()
      .sort_values("date")
)

rev_pivot = daily_rev.pivot(index="date", columns="search_stays_on", values="revenue")

plt.figure()
plt.plot(rev_pivot.index, rev_pivot[1], label="Control (search stays on)")
plt.plot(rev_pivot.index, rev_pivot[0], label="Treatment (search goes off)")
plt.axvline(pd.Timestamp("2012-05-22"), linestyle="--")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.title("Figure 5.2: Average revenue over time")
plt.legend()
plt.tight_layout()
plt.savefig("output/figures/figure_5_2.png")
plt.close()

# Step 5 — Figure 5.3
# log(avg control revenue) - log(avg treatment revenue)
log_gap = np.log(rev_pivot[1]) - np.log(rev_pivot[0])

plt.figure()
plt.plot(log_gap.index, log_gap.values)
plt.axvline(pd.Timestamp("2012-05-22"), linestyle="--")
plt.xlabel("Date")
plt.ylabel("log(rev_control) - log(rev_treat)")
plt.title("Figure 5.3: Log-scale revenue gap over time")
plt.tight_layout()
plt.savefig("output/figures/figure_5_3.png")
plt.close()
