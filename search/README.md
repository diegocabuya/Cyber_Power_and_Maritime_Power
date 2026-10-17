# Documented literature search (Method, first stage)

Reproducible record of the search described in the Method section of the article. Four
title-and-abstract queries were run on **13 October 2026** for **2014–2026**, in English and
Spanish, in **OpenAlex** and **Scopus**. Seminal works published before 2014 were included on
the authors' judgment.

| Query | Concept | OpenAlex | Scopus |
|---|---|---:|---:|
| Q1 | sea / maritime / naval power **and** cyber terms | 41 | 17 |
| Q2 | maritime power **and** measurement terms | 327 | 170 |
| Q3 | cyber power **and** measurement terms | 115 | 98 |
| Q4 | maritime cybersecurity or cyberdefense **and** strategic terms | 162 | 115 |
| **Total** | | **645** | **400** |

1,045 records retrieved; **812 unique** after removing duplicates across queries and databases
(by DOI and normalized title; 208 records appeared in both databases); **32 without an abstract**
were screened on their title.

## Screening criteria

- **C1** — the work proposes or applies a quantitative measure of the maritime or naval power of
  states.
- **C2** — that measure includes cyber power.

Result: **13 records met C1 and none met C2.** The conceptual works that link cyberspace and sea
power (11) and those on the measurement of cyber power (8) informed the Related Work section.

## Files

| File | Content |
|---|---|
| `OpenAlex_Q1..Q4.json` | Raw OpenAlex records per query (full API response, abstracts reconstructed from the inverted index) |
| `OpenAlex_Q1..Q4.csv` | The same records, one row per work (id, DOI, year, type, title, venue, authors, abstract) |
| `Scopus_Q1..Q4_2026-10-13.csv` | Scopus records of the four queries, as identifiers: EID, DOI, title, year, source, document type, and link. Scopus terms of use do not permit redistributing complete exports; the full records can be retrieved with institutional access by running the query strings below, or by EID |
| `screening_openalex_2026-10-13.csv` | Screening decision per OpenAlex record (first pass) |
| `screening_merged_2026-10-13.csv` | **Screening log of the 812 unique records**: key, source database(s), queries, year, title, decision, note |
| `openalex_search.py` | Script that reproduces the OpenAlex queries (`python3 -I openalex_search.py`) |

Decisions in the merged log: `excluido (titulo/resumen)` = excluded on title/abstract (780);
`C1 (sin C2)` = meets C1, not C2 (13); `relacionado-conceptual` = conceptual link between
cyberspace and sea power (11); `medicion-ciberpoder` = measurement of cyber power (8).

## Query strings

**Scopus** (`TITLE-ABS-KEY`, `PUBYEAR > 2013 AND PUBYEAR < 2027`):

- Q1 `(("sea power" OR "maritime power" OR "naval power" OR "poder marítimo" OR "poder maritimo" OR "poder naval") AND (cyber* OR cyberspace OR "cyber power"))`
- Q2 `(("sea power" OR "maritime power" OR "naval power" OR "poder marítimo" OR "poder maritimo") AND (index OR indicator* OR measur* OR quantif* OR "composite indicator" OR formula*))`
- Q3 `(("cyber power" OR cyberpower OR "national cyber capabilit*") AND (index OR indicator* OR measur* OR quantif*))`
- Q4 `(("maritime cyber*" OR "naval cyber*" OR (maritime AND (cyberdefen* OR "cyber defen*"))) AND (strateg* OR national OR power OR sovereignty))`

**OpenAlex** (`title_and_abstract.search`, `publication_year:2014-2026`): the same four
queries with the truncated terms expanded into their explicit forms, as written in
`openalex_search.py`.
