# SCOPE-LOCK.md, adaptive-stat-arb-commodities

Locked 18 August 2026. This file is the current authoritative state of this repo's scope
and data sources. Read this before CLAUDE.md's history sections. If this file and an older
CLAUDE.md section disagree, this file is correct and the older section should be treated as
superseded narrative, not reopened.

## Permanently closed, do not re-investigate

| What | Checked | Reason closed | What would reopen it |
|---|---|---|---|
| CME web pages and settlements web service, as an access path for anything | 17 August 2026 | HTTP 403 with a body stating automated retrieval is prohibited by CME's Data Terms of Use, quoted verbatim in `docs/D1-data-audit.md` section 10.1. Applies to this repo through the DME Oman route below. DataMine, the paid route, was checked and declined on budget on 18 August 2026 | Only if Brian requests, and receives, written permission from CME, or secures budget for DataMine. Neither has happened |
| DME Oman as the crude third leg | 17 August 2026 | Now sits with Gulf Mercantile Exchange under a CME Group partnership, behind the same access position as CME above. No free daily path | Only if a free daily path is found independent of the CME partnership, or the CME position above reopens |
| Baltic indices, as a freight leg | 17 August 2026 | Confirmed CUT per spec amendment C10. No sustainable free path exists. This was a spec level decision, not just a data gap | Not expected to reopen; C10 is a spec amendment, not a data finding |
| Euronext, as a possible European crush source (rapeseed, milling wheat, corn futures) | 18 August 2026 | Euronext's Terms of Use prohibit automated retrieval in language structurally identical to CME's, with no research exception, quoted verbatim in `docs/D1-data-audit.md` sections 9 and 10.2 | Only if Brian requests written permission from Euronext's Legal Department, Copyright Agent, the address the terms page itself names. Not requested. This was a flagged possibility for the crush gap, not a planned build, and it is now closed the same way CME is |

## Currently verified and in use

| Source | Covers | License, 1 line | Local or imported |
|---|---|---|---|
| EIA daily spot: WTI Cushing, Brent Europe, NY Harbor gasoline, NY Harbor No 2 heating oil, Henry Hub | Crack basket (CL, RB substitute, HO) and the Brent WTI parity anchor. Spot assessments, not futures settlements, documented substitute legs | US government, public domain, redistribution with attribution | **Project local.** Verified here directly, 17 August 2026, `docs/D1-data-audit.md` section 1. Also used by `commodity-volatility-trading`, which holds its own copy of this same finding independently |

**2 caveats that travel with every use of this source, not optional context:**

1. Publication lags roughly 4 business days. All 5 series ended 2026-08-11 when queried on
   2026-08-17. This is a history and estimation source, never a live daily source, and a
   backtest treating a print as available on its observation date is lookahead that voids
   the run.
2. The NY Harbor gasoline leg is conventional gasoline, not RBOB; the RBOB daily file
   returns HTTP 404. The crack basket runs on this documented substitute, stated in the D6
   crack note rather than absorbed silently.

## Open, not blocking anything today

| Item | Status | Who resolves it, and how | Blocking date |
|---|---|---|---|
| Crush legs, ZS, ZM, ZL | Unverified. No free daily source found, no US government equivalent exists | Retry the Yahoo Finance chart endpoint from the actual collection machine (returned Too Many Requests on 8 of 8 symbols from this environment, unverified rather than disproven); otherwise an unidentified source would need to appear | **Blocking D4 on the crush basket specifically**, currently scheduled to start 31 October 2026 per SPEC Part F. D4 may proceed on crack and Brent WTI without this resolving |
| TTF, gas hubs basket | Unverified. EEX's free window is 45 to 60 days and republication of its indices requires express EEX permission | Shared need with the power project's D4 fuel cost input, same instrument, same hub, same unit. If either project finds a path, check that project's own `SCOPE-LOCK.md` before re-investigating independently. See `docs/D1-data-audit.md` section 10.3 | Blocks D4 on the gas hubs basket only. Not blocking crack or Brent WTI |
| NBP, gas hubs basket third leg | Unverified. Same EEX position as TTF | Single consumer, this project only. The power project does not use NBP | Blocks D4 on the gas hubs basket only |
| CL futures, continuous, as distinct from the EIA spot substitute | Unverified. Shared need with `commodity-volatility-trading`'s WTI volatility work, neither side verified as of 18 August 2026. See `docs/D1-data-audit.md` section 10.3 | Whichever project resolves this first, the other should read that project's own D1 note before re-investigating | **Blocking D2, the continuous futures builder, 20 September 2026.** D2's acceptance gate needs both an adjusted and unadjusted continuous series; the EIA spot substitute does not satisfy this gate on its own |
| WRDS Datastream | Conditional, unresolved. EPFL subscribes to WRDS but names Compustat, CRSP, and IBES; Datastream is not among them | A signed in check of the subscribed products list on the WRDS site. Action on Brian; cannot be completed from an agent session | Not currently blocking. Base case if unresolved: no licensed history block, free feed is the only source |
| stooq CSV endpoint | Unverified. Returns a JavaScript proof of work challenge in place of the file | 2 open questions: whether solving the challenge is consistent with stooq's terms, and whether a source with an anti automation control is sound as a daily dependency | Not currently blocking; a candidate, not a plan |

## What this project can currently claim

As of 18 August 2026, this project can build and estimate 2 of its 4 baskets, crack and the
Brent WTI parity anchor, on verified EIA spot data with a documented substitute basis and a
stated publication lag. It cannot yet proceed on the crush basket, which the spec designates
as its near certain anchor and the fallback for a failing basket, because crush has 0 of 3
verified legs; nor on the gas hubs basket, which has 1 of 3. No science code exists yet and
no number is quotable: the parity gate, D3, has not run, and nothing here is BUILT under the
claims discipline this project follows. Any external description of this project's current
state should say it is scoped to 2 of 4 baskets pending further data verification, not that
the strategy is built, backtested, or trading.

## Next deliverable

**D1, the data audit note, is delivered** (`docs/D1-data-audit.md`, 17 August 2026, revised
18 August 2026). The next deliverable is **D2, the continuous futures builder, due 20
September 2026**, built in this repo's own `statarb/data/` and currently blocked on the CL
futures gap above. D3, the refactored package and the parity gate, follows on the
September weekends per SPEC Part F and does not require D2 or D4 to complete first for the
Brent WTI parity work specifically, since parity runs on the legacy pairwise design already
archived in `docs/legacy/`.
