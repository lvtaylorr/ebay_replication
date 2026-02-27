<<<<<<< HEAD

# did_analysis.py — DID Analysis Script
# Estimates the average treatment effect of turning off eBay's paid search.
# Method: Compare pre-post log revenue changes between treatment and control DMAs. # Uses preprocessed pivot tables from preprocess.py.
# Output: LaTeX table in output/tables/did_table.tex
# Reference: Blake et al. (2014), Taddy Ch. 5

import pandas as pd
import numpy as np

# Load pivot tables saved by preprocess.py
treated_pivot = pd.read_csv('temp/treated_pivot.csv', index_col='dma')
untreated_pivot = pd.read_csv('temp/untreated_pivot.csv', index_col='dma')

# Compute group means of the pre-post log revenue differences
r1_bar = treated_pivot["log_revenue_diff"].mean()
r0_bar = untreated_pivot["log_revenue_diff"].mean()

# DID estimate
gamma_hat = r1_bar - r0_bar

# Standard error for difference in means
n1 = treated_pivot.shape[0]
n0 = untreated_pivot.shape[0]
var1 = treated_pivot["log_revenue_diff"].var()   # sample variance (Bessel correction)
var0 = untreated_pivot["log_revenue_diff"].var()
se = np.sqrt(var1 / n1 + var0 / n0)

# 95% CI
ci_lower = gamma_hat - 1.96 * se
ci_upper = gamma_hat + 1.96 * se

# Print results to console
print("DID Results (Log Scale)")
print("=======================")
print(f"Gamma hat: {gamma_hat:.4f}")
print(f"Std Error: {se:.4f}")
print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")

# Write LaTeX table fragment
latex = r"""\begin{table}[h]
\centering
\caption{Difference-in-Differences Estimate of the Effect of Paid Search on Revenue}
\begin{tabular}{lc}
\hline
& Log Scale \\
\hline
Point Estimate ($\hat{\gamma}$) & $%.4f$ \\
Standard Error & $%.4f$ \\
95\%% CI & $[%.4f, \; %.4f]$ \\
\hline
\end{tabular}
\label{tab:did}
\end{table}""" % (gamma_hat, se, ci_lower, ci_upper)

with open('output/tables/did_table.tex', 'w') as f:
    f.write(latex)
