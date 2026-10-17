<div align="center">

# Cyber Power as a Structural Variable of Maritime Power

### *A Normalized Multiplicative Model for Multidomain Assessment of Maritime Power*

**Diego E. Cabuya-Padilla** · **Sergio Uribe-Cáceres** · **Carlos A. Castaneda-Marroquin**

Naval Academy of Strategic Studies, Colombian Navy · Colombian War College “General Rafael Reyes Prieto” · Naval School “Admiral Padilla” (NAVTEG)

*Manuscript under review — IEEE Access*

[![Simulator](https://img.shields.io/badge/▶_Simulator-interactive-185FA5?style=for-the-badge)](https://diegocabuya.github.io/Cyber_Power_and_Maritime_Power/simulator/simulator.html)
[![Site](https://img.shields.io/badge/🌐_Project-site-0D2A42?style=for-the-badge)](https://diegocabuya.github.io/Cyber_Power_and_Maritime_Power/)
[![Verification](https://img.shields.io/badge/🧪_Verification-script-0F6E56?style=for-the-badge)](verification/verify_model.py)

</div>

---

## Abstract

The classical formulation of maritime power—the product of maritime interests and naval power—has become insufficient to explain digitalized maritime environments, whose navigation, communications, port, and surveillance functions depend on interconnected digital infrastructures. Starting from a theory of power in which naval power expresses military power at sea and maritime power adds economic, social, and political interests, this article argues that cyber power cuts across both components and, unlike naval power, does not decay with distance. It proposes an extended formulation that incorporates cyber power, strategic will, and maritime security as structural variables, in a normalized multiplicative structure in which the collapse of any dimension constrains the aggregate and whose output lies within (0, 1], enabling a five-level interpretation scale. The formulation is verified through its logical-mathematical properties, sensitivity analysis, and constructed profiles; calibration and external validation are left to future work, and a global sensitivity analysis identifies maritime security as the main source of uncertainty. In an illustrative application to Colombia, with only maritime security taken from an external index, the model places the country at the Moderate level and shows which components concentrate the largest gaps; a corollary states the relative-cost condition under which cyber power would be the most efficient investment vector. Colombia's national ocean policy, which frames its development plans, does not address the cyber dimension. A National Maritime Power Index is proposed as a research agenda, supported by an open-access interactive simulator.

## Theoretical framework

Power is the ability to affect others to obtain the outcomes one wants (Nye, 2010). National power is exercised through four instruments—diplomatic, information, military, and economic (NATO, 2023). **Naval power** is the expression of military power at sea, whose functions Booth (1977) conceives as a trinity—military, diplomatic, and policing—unified by the use of the sea. **Maritime power** is broader: the capacity to create, develop, exploit, and defend a country's maritime interests (Colombian Ocean Commission, 2018), so it combines naval power with interests of an economic, social, and political nature. **Cyber power** obtains outcomes within and beyond cyberspace (Nye, 2010) and therefore cuts across both components; unlike naval power, whose effectiveness decays with distance (Booth's loss-of-power gradient), it acts with instantaneous global reach (NATO, 2025). This is why it enters the model as a factor of the whole system.

In Colombia, the National Ocean and Coastal Areas Policy (PNOEC), the state policy that frames the national and sectoral development plans, aims at a Medium Oceanic Power and associates that goal with position, political will, and maritime interests; the Naval Development Plan 2042 protects those interests through naval power. Neither the policy nor the documents that define the eighteen maritime interests mention the cyber dimension.

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
- **[🌐 Project site](https://diegocabuya.github.io/Cyber_Power_and_Maritime_Power/)** — theoretical framework, equation plates, model architecture, and bibliographic synthesis.
- **[🎞️ Presentation](presentation/presentation.pdf)** — 24 slides structured for an academic presentation: problem, general and specific objectives, theoretical framework, method, results, discussion, and conclusions. Also the **[simulator guide](presentation/simulator_guide.pdf)** and the **[infographic](infographic/Infographic.pdf)**.
- **Español** — the site and the simulator are bilingual (EN/ES); the Spanish view uses the notation of the Spanish version of the article (PM, IM, PN, VE, SM, CP). The Spanish article, its figures and the Spanish presentation and infographic are in [Ciberpoder-y-Poder-Maritimo](https://github.com/diegocabuya/Ciberpoder-y-Poder-Maritimo).

## Repository contents

```
.
├── index.html                           ← Project site (GitHub Pages)
├── simulator/
│   └── simulator.html                   ← Interactive model simulator (bilingual EN/ES)
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
├── presentation/
│   ├── presentation.pdf                 ← 24 slides: problem, objectives, framework, method, results, discussion, conclusions
│   └── simulator_guide.pdf              ← 3 slides: simulator architecture, its 31 controls, and use
├── infographic/
│   └── Infographic.{pdf,png}            ← The model on one page
├── docs/                                ← Manuscript PDF (posted when the editorial process allows it)
├── archive/                            ← Earlier versions of the materials, kept for the record
├── LICENSE
└── README.md
```

## Citation

> Cabuya-Padilla, D. E., Uribe-Cáceres, S., & Castaneda-Marroquin, C. A. (2026). *Cyber power as a structural variable of maritime power: A normalized multiplicative model for multidomain assessment of maritime power.* Manuscript under review, IEEE Access. Supporting materials: https://github.com/diegocabuya/Cyber_Power_and_Maritime_Power

## License

Released under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license. You are free to share and adapt the material for any purpose, provided appropriate credit is given. See [`LICENSE`](LICENSE).

---

<div align="center">

**Naval Academy of Strategic Studies (ANEES)** · Bogota, Colombia · 2026

</div>
