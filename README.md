# T Algorithm (Plain Changes Transitions)

## Authors

- Nilson Sangy
- Flavio Souza

## Exercise Question (Exercise 12)

"Implement the T algorithm (plain changes transitions) and count and plot the number of comparisons, attributions, and exchanges to generate the table, separated from the counts needed to apply the table and generate effectively all n! permutations. Write a table to demonstrate how it works and explain how it works in general terms. For which range of values of n is it worth to precompute the sequence instead of running the P algorithm? (You may work with, exchange code, or request data from the student which is implementing the P algorithm)."

Project for Exercise 12:

- Offline phase: precomputes the transition table (adjacent swap indexes).
- Online phase: applies the table and generates permutations efficiently.
- Metrics collected: comparisons, local assignments, vector assignments, execution time.

## Files

- `run_experiment.py`: runs the experiment from n=3 to n=10 and generates `results.json` and `results.js`.
- `index.html`: visual page with table, chart, and animated didactic sample.

## How to Run

1. Generate results:

```powershell
py run_experiment.py
```

2. Open the web page:

- Simple option: open `index.html` in the browser (works locally using `results.js`).
- Alternative option: use a local server:

```powershell
py -m http.server 8000
```

Then open: http://localhost:8000

## Optional Parameters

```powershell
py run_experiment.py --start 3 --end 10 --sample 5 --output results.json
```
