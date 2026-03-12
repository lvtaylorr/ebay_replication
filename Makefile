.PHONY: all clean

all: paper/paper.pdf

# Preprocessing: data wrangling and figures
output/figures/figure_5_2.png output/figures/figure_5_3.png: input/PaidSearch.csv code/preprocess.py
	python code/preprocess.py

# DID estimation
output/tables/did_table.tex: input/PaidSearch.csv code/did_analysis.py
	python code/did_analysis.py

# Paper compilation
paper/paper.pdf: paper/paper.tex output/figures/figure_5_2.png output/figures/figure_5_3.png output/tables/did_table.tex
	cd paper && pdflatex paper.tex && pdflatex paper.tex

clean:
	rm -f output/figures/*.png output/tables/*.tex paper/paper.pdf paper/paper.aux paper/paper.log	
# Dependency Answers

# 1. If code/preprocess.py changes:
# Make rebuilds the figures (figure_5_2.png and figure_5_3.png) and then recompiles paper.pdf.
# It skips did_analysis.py because its inputs did not change.

# 2. If code/did_analysis.py changes:
# Make rebuilds did_table.tex and then recompiles paper.pdf.
# It skips preprocess.py and the figures.

# 3. If paper/paper.tex changes:
# Make only recompiles paper.pdf.
# No Python scripts are rerun.


# Reflection
# Unlike run_all.sh, which blindly runs every step, Make tracks which files depend
# on others and rebuilds only what changed. This saves time and makes the workflow
# clearer for collaborators because the relationships between data, code, figures,
# tables, and the final paper are documented directly in the build rules.
