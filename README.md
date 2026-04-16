# 🔁 T Algorithm (Plain Changes)

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)
![Experiment](https://img.shields.io/badge/Experiment-n%3D3..10-0F7B6C?style=flat-square)
![Output](https://img.shields.io/badge/Output-JSON%20%2B%20Web-FF6B35?style=flat-square)

Minimal and practical implementation of Knuth's T Algorithm for permutation generation with two separated phases:

- Offline phase: precompute adjacent-swap plan indexes ⚙️
- Online phase: apply the swap plan to generate all permutations 🚀
- Measured metrics: comparisons, local assignments, vector assignments, and runtime 📊

## 👥 Authors

- Nilson Sangy
- Flavio Souza

## ⚡ Quick Start

1. Generate experiment data.

```powershell
py run_experiment.py
```

2. Open the visual hub.

- Direct file mode: open `index.html`.
- Local server mode:

```powershell
py -m http.server 8000
```

Open `http://localhost:8000`.

## 🧩 Project Structure

| File | Purpose |
| --- | --- |
| `algorithm_t.py` | Algorithm T backend logic, metrics, and experiment generation |
| `run_experiment.py` | Thin wrapper that runs experiments and exports results |
| `results.json` | Raw experiment data for analysis |
| `results.js` | Browser-friendly data for local file mode |
| `index.html` | Hub page that links to all HTML demos |
| `algorithm_t.html` | Visual dashboard for Algorithm T (table + chart + animated sample) |
| `propriedades-de-grupos.html` | Interactive group-properties demo for permutations |

## 🔬 Experiment Scope

- Default range: `n = 3..10`
- Model: adjacent swaps (plain changes)
- Sample animation default: `n = 5`

Optional parameters:

```powershell
py run_experiment.py --start 3 --end 10 --sample 5 --output results.json
```

## 📝 Exercise Statement (Exercise 12)

> Implement the T algorithm (plain changes) and count and plot the number of comparisons, attributions, and exchanges to generate the table, separated from the counts needed to apply the table and generate effectively all permutations. Write a table to demonstrate how it works and explain how it works in general terms. For which range of values of n is it worth to precompute the sequence instead of running the P algorithm? (You may work with, exchange code, or request data from the student which is implementing the P algorithm).

## 📚 Theoretical Background

### Algorithm P (Plain Changes)

Algorithm P is a method for generating all permutations of a set where each new sequence is reached through a single exchange of adjacent elements.

- Mechanism: It operates similarly to Gray Codes, where each transition increases or decreases the total number of inversions by exactly one unit. The algorithm generates permutations by taking a sequence of `n-1` elements and inserting the number `n` into every possible position, moving it back and forth (scanning "up" and "down" the vector).
- Hamiltonian Path: Knuth notes that this algorithm guarantees the existence of a closed Hamiltonian path in the graph of all possible permutations, where the edges represent these single adjacent swaps.
- Inversion Tracking: The algorithm explicitly maintains an inversion vector to control the generation process.
- Improved Version: An Improved P Algorithm (detailed as Algorithm 4) optimizes the process by streamlining outputs and updating control variables and vectors only when the largest value reaches the extreme ends of the vector.
- Formal Reference: This algorithm is found in Donald E. Knuth's The Art of Computer Programming, Volume 4A: Combinatorial Algorithms, Part 1, Section 7.2.1.2 ("Generating all permutations").

### Algorithm T (Plain Changes Transitions)

Algorithm T is an optimized variation of the plain changes method that enhances performance by dividing the generation process into two distinct stages: offline and online.

- Offline Phase: The algorithm pre-computes a transition table of indices based on inversions and stores this table in the computer's memory.
- Online Phase: Using the pre-calculated table as a roadmap, the algorithm can generate all permutations very rapidly by performing only the indicated swaps.
- Computational Trade-off: The primary goal of Algorithm T is to achieve higher speeds during the actual generation (online) by investing time and memory in the setup phase (offline). A central part of the studies involves determining the range of `n` for which it is more efficient to pre-compute this table rather than running the dynamic calculations of Algorithm P directly.
- Performance Note: In its online phase, the number of comparisons often drops to zero because the algorithm simply follows the fixed instructions stored in the table.
- Formal Reference: This algorithm is treated as an advanced exercise and variation within the framework of Knuth's The Art of Computer Programming, Volume 4A, related to the combinatorial search and generation techniques discussed in Section 7.2.2.

## 💡 Notes

- For fair timing, avoid printing permutations during measurement runs.
- Use printing only for correctness checks (no repetition, full permutation coverage).

## 📈 Required Comparisons and Charts (Exercise 12)

The requested analysis is a trade-off study between Algorithm T and Algorithm P Improved.

Comparisons to perform:

- Break-even point by `n`: determine for which `n` values precomputing with T becomes worth it.
- Cost model comparison: `T Offline + T Online` versus `P Total`.
- Online efficiency: compare the very low-cost online execution of T against P's on-the-fly control work.
- Reuse scenario: evaluate repeated full generations where T pays offline once and reuses it.

Charts to generate for `n = 3..10`:

- Comparisons (`C`): T total vs P total.
- Local assignments (`A local vars`): T total vs P total.
- Vector assignments (`A to/from V`): T total vs P total.
- Execution time (`T` seconds): T total vs P total, used to visualize crossing behavior.

This project dashboard includes all four comparison charts plus a break-even runs table based on time.
