# Compassionate Superintelligence: companion code

Companion programs for the book **Compassionate Superintelligence: Architecture, Alignment, and the Future of Intelligence That Cares** by Dr. Sri Amit Ray ([Compassionate AI Lab](https://amitray.com/compassionate-ai-lab/), 2026; ISBN 978-81-69641-22-7 (Second Edition, 2026)). The first edition was published in 2018 as *Compassionate Artificial Superintelligence AI 5.0* (Inner Light Publishers; ISBN 978-93-82123-44-6 (First Edition, 2018)).

`code/models.py` reproduces every numerical teaching example in the book and regenerates its data figures. The models are teaching instruments: their parameters were chosen to make mechanisms visible, and their outputs are not empirical estimates of real AI systems.

## Run it

```sh
python -m pip install -r requirements.txt
python code/models.py > code/results.txt
```

The program writes `code/numerical_results.json` (all results, with versions, repetitions, standard errors and settings) and vector PDFs in `figures/`. Random generators are seeded (base seed 20261014), so the results match the book.

## What the program computes

| Model | Chapter | Main result |
|---|---|---|
| Compassion Quotient | 12 | CQ of 3.548 and 1.358; vulnerability weighting widens the preference between two actions |
| CAI aggregation | 10 | Arithmetic and geometric indices for three plans; floor vetoes on FG and VP |
| Goodhart selection | 12 | True value of the proxy-best option under light- and heavy-tailed error |
| Off-switch game | 18 | Value of deferring; effect of human error, crossover near 22 percent |
| Discounting | 25 | Present weight of future harms at four discount rates |
| Value attractor | 5 | Probability of ending in the beneficial basin, by monitoring level |
| Suffering reduction | 13 | Optimal intervention sets under two vulnerability weights and without the dignity constraint |
| Welfare aggregation | 14 | Utilitarian, Nash, prioritarian and maximin rankings of three policies |
| Reward trade-off | 16 | Choice among three responses as the price of harm varies, and under a hard constraint |
| Calibration audit | 17 | Calibration gaps and expected calibration error of 0.08 |
| Compounding errors | 19 | Probability of an error-free multi-step task |
| Racing | 21 | Gain in win probability from cutting safety |
| Nash bargaining | 21 | Effect of outside options and of a need floor on a negotiated split |
| Human and AI screening | 22 | Missed cases and false alarms under three screening rules |
| Data-center siting | 25 | Weighted, geometric and floor-based comparison of three sites |
| Scenario workshop | 27 | Expected value and minimax regret of four strategies |

Change the parameters, add stakeholders and test the conclusions: a conclusion that holds across a wide range of parameters deserves more confidence than one that depends on a particular choice.

## Get the book

- Paperback and Kindle: search Amazon for *Compassionate Superintelligence* by Sri Amit Ray
- Full-color PDF eBook: https://amitray.com/compassionate-superintelligence-ebook/

## Cite as

**Book (MLA):**
Ray, Sri Amit. *Compassionate Superintelligence: Architecture, Alignment, and the Future of Intelligence That Cares*. 2nd ed., Compassionate AI Lab, 2026. ISBN 978-81-69641-22-7.

**Book (APA):**
Ray, S. A. (2026). *Compassionate superintelligence: Architecture, alignment, and the future of intelligence that cares* (2nd ed.). Compassionate AI Lab.

**Companion code:**
Ray, S. A. (2026). *Compassionate Superintelligence: companion code* [Computer software]. Compassionate AI Lab. https://github.com/compassionate-ai-lab/compassionate-superintelligence

**BibTeX:**

```bibtex
@book{ray2026compassionate,
  author    = {Ray, Sri Amit},
  title     = {Compassionate Superintelligence: Architecture, Alignment, and the Future of Intelligence That Cares},
  edition   = {2},
  publisher = {Compassionate AI Lab},
  year      = {2026},
  isbn      = {978-81-69641-22-7},
  url       = {https://github.com/compassionate-ai-lab/compassionate-superintelligence}
}
```

GitHub's **Cite this repository** button (from `CITATION.cff`) gives the same reference in APA and BibTeX.

## Corrections

Please report errors through the repository's Issues page. Corrections to the book will be listed here.

## Licence

The code in this repository is released under the MIT License (see `LICENSE`). The text of the book is © 2026 Dr. Sri Amit Ray, all rights reserved.

About the lab: [Compassionate AI Lab](https://amitray.com/compassionate-ai-lab/) · More of the author's work: https://amitray.com
