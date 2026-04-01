# 🔁 T Algorithm (Plain Changes Transitions)

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)
![Experiment](https://img.shields.io/badge/Experiment-n%3D3..10-0F7B6C?style=flat-square)
![Output](https://img.shields.io/badge/Output-JSON%20%2B%20Web-FF6B35?style=flat-square)

Minimal and practical implementation of Knuth's T Algorithm for permutation generation with two separated phases:

- Offline phase: precompute transition indexes ⚙️
- Online phase: apply transitions to generate all permutations 🚀
- Measured metrics: comparisons, local assignments, vector assignments, and runtime 📊

## 👥 Authors

- Nilson Sangy
- Flavio Souza

## ⚡ Quick Start

1. Generate experiment data.

```powershell
py run_experiment.py
```

2. Open the visual dashboard.

- Direct file mode: open `index.html`.
- Local server mode:

```powershell
py -m http.server 8000
```

Open `http://localhost:8000`.

## 🧩 Project Structure

| File | Purpose |
| --- | --- |
| `run_experiment.py` | Runs Offline/Online phases and exports results |
| `results.json` | Raw experiment data for analysis |
| `results.js` | Browser-friendly data for local file mode |
| `index.html` | Visual dashboard (table + chart + animated sample) |

## 🔬 Experiment Scope

- Default range: `n = 3..10`
- Transition model: adjacent swaps (plain changes)
- Sample animation default: `n = 5`

Optional parameters:

```powershell
py run_experiment.py --start 3 --end 10 --sample 5 --output results.json
```

## 📝 Exercise Statement (Exercise 12)

> Implement the T algorithm (plain changes transitions) and count and plot the number of comparisons, attributions, and exchanges to generate the table, separated from the counts needed to apply the table and generate effectively all n! permutations. Write a table to demonstrate how it works and explain how it works in general terms. For which range of values of n is it worth to precompute the sequence instead of running the P algorithm? (You may work with, exchange code, or request data from the student which is implementing the P algorithm).

## 💡 Notes

- For fair timing, avoid printing permutations during measurement runs.
- Use printing only for correctness checks (no repetition, full `n!` coverage).
