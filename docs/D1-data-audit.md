# D1, data audit note

**Deliverable:** D1, SPEC Part D.
**Date:** 17 August 2026.
**Acceptance gate:** universe locked, no downstream work on an unverified series.
**Gate status: NOT MET. The universe is not locked.** See the verdict summary.

Every verdict below is the result of an actual request to the named endpoint on 17 August
2026, recorded with its HTTP status, row count, and observed date range. Where a source
could not be reached or could not be confirmed from this environment, the verdict is
UNVERIFIED and says so. No verdict here is inferred from documentation alone.

---

## 1. Verified free series

All 5 retrieved over plain HTTPS with no API key, no account, and no browser challenge.
US government data, public domain, redistribution permitted with attribution.

| Series | Endpoint | Rows | Range observed | Verdict |
|---|---|---|---|---|
| WTI Cushing spot | `eia.gov/dnav/pet/hist_xls/RWTCd.xls` | 10221 | 1986-01-02 to 2026-08-11 | **PASS** |
| Brent Europe spot | `eia.gov/dnav/pet/hist_xls/RBRTEd.xls` | 9953 | 1987-05-20 to 2026-08-11 | **PASS** |
| NY Harbor gasoline spot | `eia.gov/dnav/pet/hist_xls/EER_EPMRU_PF4_Y35NY_DPGd.xls` | 10097 | 1986-06-02 to 2026-08-11 | **PASS**, with substitution note |
| NY Harbor No 2 heating oil spot | `eia.gov/dnav/pet/hist_xls/EER_EPD2F_PF4_Y35NY_DPGd.xls` | 10095 | 1986-06-02 to 2026-08-11 | **PASS** |
| Henry Hub spot | `eia.gov/dnav/ng/hist_xls/RNGWHHDd.xls` | 7431 | 1997-01-07 to 2026-08-11 | **PASS** |

**2 constraints attach to all 5 and must be carried into every downstream design.**

1. **These are spot assessments, not futures settlements.** The spec's science is built on
   continuous futures with roll calendars (D2) and on cointegrating vectors estimated on
   futures. A spot series is a documented substitute for a futures leg, not the same
   series, and any basket estimated on spot is labeled as such in its D6 note.
2. **Publication lags roughly 4 business days.** Every 1 of the 5 series ended at
   2026-08-11 when queried on 2026-08-17. These are adequate as a history block and as a
   research source. They are **not** a live daily source for a point in time system without
   the lag modeled explicitly, and a backtest that treats an EIA spot print as available on
   its observation date is lookahead.

Substitution note on the gasoline leg: the retrieved column header reads *New York Harbor
Conventional Gasoline Regular Spot Price FOB*. That is conventional gasoline. It is not
RBOB. The RBOB daily file (`EER_EPMRR_PF4_Y35NY_DPGd.xls`) returns HTTP 404. The crack
basket therefore runs on conventional gasoline as a documented substitute leg, and the
substitution is stated in the D6 crack note rather than absorbed silently.

## 2. Series with no verified free path

| Series | Basket | What was checked | Verdict |
|---|---|---|---|
| ZS, ZM, ZL | Crush | No US government daily equivalent exists. stooq CSV endpoint gated, see below. Yahoo endpoint unavailable, see below. | **UNVERIFIED** |
| TTF daily | Gas hubs | EEX publishes free index files, but the free window is 45 days on the current file and 60 days on the final price file, the EGSI day ahead index for TTF is not in the free download set, and EEX states that republication of these indices requires express EEX permission | **UNVERIFIED** |
| NBP daily | Gas hubs | Same EEX position as TTF | **UNVERIFIED** |
| DME Oman | Crude third leg candidate | The contract now sits with Gulf Mercantile Exchange under a CME Group partnership, which places its settlements behind the same access position as section 3. No free daily path found. | **CUT** |
| Baltic indices | Freight | Confirmed CUT per amendment C10. No free daily path exists. Freight survives only inside the gas corridor's banded public shipping assumptions. | **CUT**, confirmed |

## 3. Access methods checked and rejected

**stooq.** `stooq.com/q/d/l/?s=cl.f&i=d` returns HTTP 200 with a JavaScript proof of work
challenge in place of the CSV, with and without a browser user agent. A scripted client
cannot retrieve the file without executing the challenge. Recorded as UNVERIFIED. Before
this is treated as an access path, 2 things need resolving: whether solving the challenge
is consistent with stooq's terms, and whether a source that added an anti automation
control is sound as a daily dependency for a system whose collection jobs must not break.

**Yahoo Finance chart endpoint.** `query1.finance.yahoo.com/v8/finance/chart/...` returned
`Too Many Requests` on every attempt across 8 symbols, both on first contact and on retry.
This may be specific to this network. **Not confirmed working and not confirmed broken.**
Recorded as UNVERIFIED FROM THIS ENVIRONMENT and flagged for a retry from the machine that
will actually run the collection jobs.

**CME Group web pages.** See project 3's D1 note. CME's response states that automated
retrieval is prohibited by its Data Terms of Use. That position applies here too and rules
CME web pages out as a source for any leg in this project.

## 4. WRDS Datastream check

EPFL subscribes to WRDS. Accounts are opened by registering on the WRDS site with an
`@epfl.ch` address, with VPN required off campus.

The financial modules EPFL names are Compustat, CRSP, and IBES. **Datastream is not among
them.** Since Datastream is the module that would carry the licensed futures history, the
history upgrade in SPEC Part E is not confirmed.

**Verdict: CONDITIONAL, unresolved.** Confirming this requires signing in to WRDS with the
EPFL account and reading the subscribed products list, which cannot be done from here.
**Action on Brian.** Until it resolves, the base case is that there is no licensed futures
history block, and the free feed is the only source. WRDS terms are unchanged regardless of
outcome: history block only, academic use, never republished, never a daily dependency.

## 5. Verdict per basket

| Basket | Legs verified | Verdict |
|---|---|---|
| **Crack** CL, RB, HO | 3 of 3, on EIA spot | **PASS**, on a spot basis, with the conventional gasoline substitution documented |
| **Brent WTI** parity anchor | 2 of 2, on EIA spot | **PASS**, on a spot basis |
| **Gas hubs** TTF, HH, NBP | 1 of 3 | **FAIL**. Henry Hub verified, TTF and NBP not |
| **Crush** ZS, ZM, ZL | 0 of 3 | **FAIL**. No leg has a verified free daily source |

## 6. What this means, stated plainly

**The crush basket has no verified free data path, and crush is the spec's designated
anchor.** SPEC Part F step 4 orders the work crush first because it is the near certain
anchor and a mechanical processing identity, and SPEC Part I names crush as the basket the
strategy falls back to when another fails. That assumption does not currently hold on
verified sources, and it is the most consequential finding in this audit.

**The crack basket and the Brent WTI parity anchor both pass**, on spot series with 39 or
more years of history. Work can proceed on those 2 without waiting, provided every note
states that the estimation ran on spot rather than futures.

**The gas basket is 1 leg short.** Henry Hub is solid. TTF and NBP are the gap.

## 7. Open items, in priority order

1. Resolve the crush legs. Retry the Yahoo endpoint from the collection machine, then
   establish whether any source gives ZS, ZM, and ZL daily under terms that permit a daily
   dependency. Until then the anchor assumption is unsupported.
2. Resolve TTF and NBP, noting that the EEX republication restriction affects what the
   project can publish, not only what it can collect.
3. Sign in to WRDS and read the subscribed products list. Confirm or rule out Datastream.
4. Retry Yahoo from the collection machine and record the outcome here.
5. Decide whether spot legs are acceptable as the base case for D4 onward, or whether the
   universe waits for a futures source. **This is a design decision, not an audit finding,
   and it is Brian's call.**

## 8. Provenance

Every result in sections 1 to 3 comes from a request issued on 17 August 2026. Rows and
date ranges were read from the retrieved files, not from documentation. The EEX, WRDS, and
Gulf Mercantile positions come from those organizations' own published pages, and each is
marked UNVERIFIED rather than CUT where a live check was not possible.

---

## 9. Flagged finding, 18 August 2026: a possible European route to the crush gap

**This is a flag, not a decision. Nothing in this section changes this project's
universe, its configs, or D4's start condition. `config/baskets.yaml` is untouched. Crush
remains FAILED per section 6, 0 of 3 verified legs, and D4 does not start on it.**

Euronext Paris lists futures on rapeseed, milling wheat, and corn, alongside options on
the same underlyings. Rapeseed crushes into rapeseed oil and rapeseed meal, the same
physical relationship the crush basket is built on, so a verified Euronext rapeseed
futures source could in principle support a crush basket built on European rather than US
underlyings. This would not fill the ZS, ZM, ZL gap directly; it would be a different
basket on different instruments, and Euronext does not appear to list rapeseed oil or
rapeseed meal futures the way CME lists ZM and ZL for soybeans, so the European crush
economics may need to be constructed differently even if the futures leg verifies.

**Checked 18 August 2026, in the commodity volatility trading project's D1 revision,
section 9: Euronext's Terms of Use prohibit automated retrieval** in terms structurally
identical to CME's, quoted there in full. That check covered Euronext's website terms
generally, which apply to the futures pages as much as the options pages. **The
verification spike stopped at the terms check and did not proceed to check the futures
data specifically**, per the same instruction that stopped it on the options side.

**Outcome: this route is closed for now, on the same terms of use grounds as every other
prohibited source recorded in this project's audits.** It is recorded here as a closed
flag rather than an open one, since the check that would have resolved it did run, even
though it ran in the other project's note. If this is revisited, it starts with a written
permission request to Euronext, the same starting point recorded in the volatility
project's note, not with a fresh reachability check under different headers.
