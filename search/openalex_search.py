#!/usr/bin/env python3
"""Documented, reproducible literature search in OpenAlex (Method, first stage).

Open-access equivalent of the four Scopus strings (Q1-Q4). OpenAlex does not support truncation
(*): the truncated Scopus terms are expanded here into their explicit forms.
Saves the raw records (JSON) and one CSV per query in this folder.

    python3 -I openalex_search.py

Run on 13 October 2026: Q1 41, Q2 327, Q3 115, Q4 162 records (645 in total).
"""
import csv, datetime, json, os, time, urllib.parse, urllib.request

OUT = os.path.dirname(os.path.abspath(__file__))
YEARS = "2014-2026"
MAR = '("sea power" OR "maritime power" OR "naval power" OR "poder marítimo" OR "poder maritimo" OR "poder naval")'
CYB = '(cyber OR cyberspace OR cybersecurity OR "cyber security" OR cyberdefense OR cyberdefence OR "cyber defense" OR "cyber defence" OR "cyber power" OR cyberpower OR cyberattack OR "cyber attack")'
MEA = '(index OR indicator OR indicators OR measurement OR measure OR measuring OR quantification OR quantitative OR "composite indicator" OR formula OR formulation)'
Q = {
    "Q1": f"{MAR} AND {CYB}",
    "Q2": f'("sea power" OR "maritime power" OR "naval power" OR "poder marítimo" OR "poder maritimo") AND {MEA}',
    "Q3": f'("cyber power" OR cyberpower OR "national cyber capability" OR "national cyber capabilities") AND (index OR indicator OR indicators OR measurement OR measure OR measuring OR quantification)',
    "Q4": '("maritime cyber" OR "maritime cybersecurity" OR "maritime cyber security" OR "naval cyber" OR "maritime cyberdefense" OR "maritime cyber defense" OR "maritime cyber defence") AND (strategy OR strategic OR national OR power OR sovereignty)',
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "cyber-power-maritime-power-literature-search"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def abstract(w):
    inv = w.get("abstract_inverted_index") or {}
    pos = sorted((p, t) for t, ps in inv.items() for p in ps)
    return " ".join(t for _, t in pos)


def run(name, q):
    flt = f"title_and_abstract.search:{q},publication_year:{YEARS}"
    recs, cursor = [], "*"
    while cursor:
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode(
            {"filter": flt, "per-page": "200", "cursor": cursor})
        d = get(url); recs += d["results"]; cursor = d["meta"].get("next_cursor")
        if not d["results"]: break
        time.sleep(0.2)
    json.dump({"query": q, "filter": flt, "date": str(datetime.date.today()), "n": len(recs), "results": recs},
              open(os.path.join(OUT, f"OpenAlex_{name}.json"), "w", encoding="utf-8"), ensure_ascii=False)
    with open(os.path.join(OUT, f"OpenAlex_{name}.csv"), "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f); wr.writerow(["id", "doi", "year", "type", "title", "venue", "authors", "abstract"])
        for w in recs:
            src = ((w.get("primary_location") or {}).get("source") or {}).get("display_name", "")
            au = "; ".join(a["author"]["display_name"] for a in w.get("authorships", [])[:6])
            wr.writerow([w["id"], w.get("doi") or "", w.get("publication_year"), w.get("type"),
                         w.get("display_name") or "", src, au, abstract(w)])
    return len(recs)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, q in Q.items():
        print(k, run(k, q), "records")
