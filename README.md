<div align="center">

# Cyber Power as a Structural Variable of Maritime Power

### *A Normalized Multiplicative Model for Multidomain Assessment of Maritime Power*

**Diego E. Cabuya-Padilla** · **Sergio Uribe-Cáceres** · **Carlos A. Castaneda-Marroquin**

Naval Academy of Strategic Studies, Colombian Navy · Colombian War College “General Rafael Reyes Prieto” · Naval School “Admiral Padilla” (NAVTEG)

*Manuscript under review — IEEE Access (revised version, October 2026)*

[![Simulator](https://img.shields.io/badge/▶_Simulator-interactive-185FA5?style=for-the-badge)](https://diegocabuya.github.io/Cyber_Power_and_Maritime_Power/simulator/simulator.html)
[![Site](https://img.shields.io/badge/🌐_Project-site-0D2A42?style=for-the-badge)](https://diegocabuya.github.io/Cyber_Power_and_Maritime_Power/)
[![Verification](https://img.shields.io/badge/🧪_Verification-script-0F6E56?style=for-the-badge)](verification/verify_model.py)

</div>

---

## Abstract

The classical formulation of maritime power—the product of **maritime interests** and **naval power**—has become insufficient to explain the dynamics of digitalized maritime environments. This article proposes an extended formulation that incorporates **cyber power**, **strategic will**, and **maritime security** as structural variables of maritime power. The model adopts a normalized multiplicative structure in which the collapse of any dimension constrains the aggregate, and whose output lies within (0, 1], enabling a directly interpretable five-level scale.

The formulation is **verified** in three stages—logical-mathematical properties, sensitivity analysis, and constructed profiles—and a global sensitivity analysis identifies maritime security (its value and its weight) as the main source of uncertainty; **calibration and external validation are distinguished from verification and left to future work**. Colombia is used as an illustrative case: taking its maritime security rank from the most systematic maritime power index currently available and illustrative values for the other components, the model places the country at the Moderate level and decomposes the result to show which components concentrate the largest gaps; a corollary states the relative-cost condition under which cyber power would be the most efficient investment vector.

## The model

**Level 1 — general normalized expression (Eqs. 1–3):**

```
MP_norm = [ (MI × NP) × SW × MS^γ × CP^α ]^(1/n_eff)        with  n_eff = 3 + γ + α
```

| Symbol | Variable | Role |
|:------:|----------|------|
| **MI** | Maritime Interests | The purpose that gives meaning to maritime power (Eq. 4: weighted sub-index) |
| **NP** | Naval Power | The instrument: Force × Position × MDA^μ (Eq. 5) |
| **SW** | Strategic Will | Multiplier of the whole system: political · institutional · social (Eq. 6) |
| **MS** | Maritime Security | Condition of the environment — incidence of threats, not capabilities (Eq. 7); γ is its weight |
| **CP** | Cyber Power | Structural variable: cybersecurity, strategic cyberdefense, recovery capacity, amplified by cyber diplomacy (Eq. 8); α is **the weight of cyber dependence**, not a measure of capability |

The normalization is a weighted geometric mean with weights ω<sub>MI</sub> = ω<sub>NP</sub> = ω<sub>SW</sub> = 1/n<sub>eff</sub>, ω<sub>MS</sub> = γ/n<sub>eff</sub>, ω<sub>CP</sub> = α/n<sub>eff</sub>. **Proposition 1:** MP<sub>norm</sub> = G<sup>1−w</sup> · CP<sup>w</sup>, where G is the geometric mean of the rest of the system and w = α/n<sub>eff</sub>; hence raising CP always raises the index, whereas raising α raises it only if CP > G, and the index is strictly concave in every component for any α > 0. **Corollary 1:** cyber power is the most efficient investment vector if and only if c<sub>k</sub>/c<sub>CP</sub> > (ω<sub>k</sub>/X<sub>k</sub>)/(ω<sub>CP</sub>/CP) for every other component k — a testable condition on relative unit costs, not a result.

Interpretation scale: **Critical** (0.00–0.20), **Low** (0.21–0.40), **Moderate** (0.41–0.60), **Significant** (0.61–0.80), **High** (0.81–1.00).

## Colombian reference case

| | MI | NP | SW | MS | CP | α | γ | MP<sub>norm</sub> |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Value | 0.60 | 0.55 | 0.48 | **0.24** | 0.40 | 0.55 | 0.70 | **0.455** (Moderate) |

Only **MS** derives from an external source: Colombia's 75th rank among 99 states in the maritime security index of Vargas-Suárez et al. (2021), converted into a position percentile, (99 − 75)/98 ≈ 0.24. The other values and the parameters are illustrative choices of the authors, all set directly at Level 1. G = 0.464 > CP, so a larger α lowers the index (0.464 as α → 0, 0.450 at α = 1). Break-even cost ratios of Corollary 1: 1.21 (MI), 1.32 (NP), 1.52 (SW), 2.12 (MS). The result is robust to moderate (±0.10) but not to large (±0.20) uncertainty in the inputs.

## Start here

- **[▶ Interactive simulator](https://diegocabuya.github.io/Cyber_Power_and_Maritime_Power/simulator/simulator.html)** — Level-1 inputs and parameters, optional Level-2 disaggregation, elasticities, marginal returns, the cost condition of Corollary 1, a Monte Carlo uncertainty band, and comparison charts. Preloaded with the Colombian reference case and the constructed profiles of the article.
- **[🧪 Verification script](verification/verify_model.py)** — regenerates every number of the verification and case-study sections (Tables 4–7, Proposition 1, Corollary 1). Standard library only:

  ```bash
  python3 verification/verify_model.py 300000   # canonical run quoted in the article (~1 min)
  ```

  Reference output: [`verification/verification_output.txt`](verification/verification_output.txt).
- **[🔎 Documented literature search](search/README.md)** — query strings, raw records (OpenAlex and Scopus, 13 October 2026, 2014–2026) and the screening log of the 812 unique records.
- **[🌐 Project site](https://diegocabuya.github.io/Cyber_Power_and_Maritime_Power/)** — equation plates, model architecture, bibliographic synthesis, and revision notes.

## Repository contents

```
.
├── index.html                           ← Project site (GitHub Pages)
├── simulator/
│   └── simulator.html                   ← Interactive model simulator (revised model)
├── verification/
│   ├── verify_model.py                  ← Numerical verification; regenerates Tables 4–7
│   └── verification_output.txt          ← Reference output of the canonical run (300,000 draws)
├── search/
│   ├── README.md                        ← Queries, databases, criteria, counts
│   ├── OpenAlex_Q1..Q4.{json,csv}       ← Raw OpenAlex records
│   ├── Scopus_Q1..Q4_2026-10-13.csv     ← Raw Scopus records
│   ├── screening_merged_2026-10-13.csv  ← Screening log of the 812 unique records
│   └── openalex_search.py               ← Reproduces the OpenAlex queries
├── figures/
│   ├── equations/                       ← The 8 equation plates (PDF + PNG)
│   └── schemes/                         ← Two-level architecture (Fig. 1) + bibliographic synthesis (Table 8)
├── docs/                                ← Manuscript PDF (posted when the editorial process allows it)
├── archive/2026-08_pre-revision/        ← Presentation, infographic and submitted version (superseded)
├── LICENSE
└── README.md
```

## What changed in the October 2026 revision

| Topic | Submitted version | Revised version |
|---|---|---|
| α | Cyber-maturity index and exponent at once | **Weight of cyber dependence**; maturity is read on CP in five bands (Proposition 1) |
| Concavity | Attributed to α < 1 | Holds for every α > 0: the normalized exponent is always below one, for every component |
| Investment efficiency | "Cyber power is the most efficient investment vector" | **Removed**; replaced by the cost condition of Corollary 1 |
| Colombia | MS = 0.59 (a percentage share), MP<sub>norm</sub> = 0.53, "same scale" as the reference index | MS = 0.24 (rank percentile), MP<sub>norm</sub> = 0.455; no common scale, no calibration, no validation claimed |
| Verification | "Validation" | Verification, calibration and external validation distinguished (Sargent, 2011); uncertainty analysis with Sobol' indices; protocol for calibration and external validation; operationalization table |
| Components | Cyber resilience (CR<sub>m</sub>); cyber diplomacy in CP and in political will; Σβ = 0.90 in the simulator | **Maritime recovery capacity (RC<sub>m</sub>)**; cyber diplomacy only in CP; explicit operational boundaries; Σβ = 1 |
| Literature | Search not recorded | Documented search in OpenAlex and Scopus; existing composite measures discussed (all additive, none with cyber power) |

The materials in `archive/` predate these changes and are kept for the record only.

## Citation

> Cabuya-Padilla, D. E., Uribe-Cáceres, S., & Castaneda-Marroquin, C. A. (2026). *Cyber power as a structural variable of maritime power: A normalized multiplicative model for multidomain assessment of maritime power.* Manuscript under review, IEEE Access. Supporting materials: https://github.com/diegocabuya/Cyber_Power_and_Maritime_Power

## License

Released under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license. You are free to share and adapt the material for any purpose, provided appropriate credit is given. See [`LICENSE`](LICENSE).

---

<div align="center">

**Naval Academy of Strategic Studies (ANEES)** · Bogota, Colombia · 2026

</div>
