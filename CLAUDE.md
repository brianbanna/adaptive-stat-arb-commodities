# CLAUDE.md, multi leg relative value with break detection

You are in a public repo. Read this file completely before your first tool call, then read
`SPEC.md`. If you are about to write code and you have not read `SPEC.md`, stop and read it.

There is a second, older `CLAUDE.md` archived at `docs/legacy/CLAUDE-legacy.md`. It is
superseded. Do not follow it.

Read `SCOPE-LOCK.md` next, before anything else in this file. It is the current state;
sections below are history that led to it.

---

## 1. SPEC.md is the build authority

`SPEC.md` at the repo root is the full standalone specification for this project. It
carries Part A the plain words, Part B the ranked goals, Part C worked data scenarios,
Part D the deliverables table with IDs and dates and acceptance gates, Part E the data
register, Part F the phase by phase plan, Part G the methods core with the actual
parameters, Part H the hard rules, Part I the risks with pre committed fallbacks, Part J
the definition of done, Part K executor notes.

Nothing outside `SPEC.md` is required to execute this project. When this file and
`SPEC.md` disagree on a fact, `SPEC.md` wins and this file is wrong and should be fixed.
When they disagree on a prohibition, the stricter reading wins.

`SPEC.md` is reproduced from the master document with 1 token level redaction, marked in a
comment at the top of the file, required by its own Part H rule 1. Nothing else is altered.

## 2. Where the build stands, and what is next

**Today the repo is at Phase 0, per SPEC Part F.** Phase 0 is the week of 11 to 17 August
2026 and it is audit only, roughly 1 hour. As of 17 August 2026 the repo holds the
skeleton, the config scaffolds, the spec, and the archived legacy material. No science
code, no result.

**D1, the data audit note. DELIVERED 17 August 2026. `docs/D1-data-audit.md`. Read it
before D2 or D4.** It did not exist before that date; the earlier scaffold never contained
one.

**THE UNIVERSE IS NOT LOCKED. 2 baskets of 4 pass.**

| Basket | Verdict |
|---|---|
| Crack, CL RB HO | **PASS**, 3 of 3 legs on verified free EIA daily spot |
| Brent WTI, the parity anchor | **PASS**, 2 of 2 legs on verified free EIA daily spot |
| Gas hubs, TTF HH NBP | **FAIL**, 1 of 3. Henry Hub verified, TTF and NBP not |
| Crush, ZS ZM ZL | **FAIL**, 0 of 3. No leg has a verified free daily source |

3 findings that change how the next deliverables are built, none of them optional:

1. **Crush, the spec's designated anchor, has no verified free data path.** Part F step 4
   orders the work crush first because it is the near certain anchor, and Part I falls back
   to crush when another basket fails. That assumption does not hold on verified sources
   today. Do not start D4 on crush.
2. **The verified series are spot assessments, not futures settlements.** A basket
   estimated on them is estimated on a documented substitute leg, and its D6 note says so.
3. **EIA spot publication lags roughly 4 business days.** All 5 verified series ended
   2026-08-11 when queried on 2026-08-17. Adequate as history, not a live daily source. A
   backtest treating an EIA print as available on its observation date is lookahead and
   voids the run.

DME Oman is CUT, so crude stays a 2 leg basket as the spec pre committed. The Baltic CUT is
confirmed. WRDS is CONDITIONAL and unresolved: EPFL subscribes to WRDS, but the modules it
names are Compustat, CRSP, and IBES, and Datastream is not among them. Confirming that
needs a signed in check of the subscribed products list. Action on Brian.

**No downstream work runs on an unverified series.** D4 may proceed on crack and on the
Brent WTI anchor. It may not proceed on crush or gas.

Then, in order:

- **D2, continuous futures builder, 20 September 2026.** Own rolls at 5 business days
  before expiry, back adjusted additive, and the unadjusted series retained because
  cointegration robustness later runs on both. Built in this repo's own `statarb/data/`,
  as of 18 August 2026: the shared platform repo that originally owned this deliverable was
  retired that day, each project now owns its own ingestion, and every finding relevant to
  this project that repo had recorded was copied into `docs/D1-data-audit.md` section 10
  before it was deleted.
- **D3, the refactored package, 21 September 2026.** 2 September weekends. Weekend 1: the
  skeleton and the configs, already scaffolded here. Weekend 2: port the pairwise science
  untouched and run the parity gate. **THE PARITY GATE: reproduce the legacy Brent WTI
  pair's hedge ratio path, signals, and equity curve to numerical tolerance. Nothing
  proceeds until it is green, and no science change rides along with the refactor.** The
  legacy design is archived in `docs/legacy/` and its parameters in `config/legacy/`
  precisely so this gate has something to check against.
- **D4 to D6, Johansen and Kalman and the 3 notes, 31 October 2026.** Crush first, then
  crack, then gas.
- **D7 to D10, the break overlay, 30 November to 14 December 2026.**
- **D11 to D14, THE ENGINE SPRINT, 1 to 20 December 2026.** The only immovable deadline in
  the project.
- **20 December 2026: API frozen, tag cut, engine note shipped, down tools.**

Phase 5, 21 December 2026 to 6 February 2027, is the frozen window: nothing. Pipelines run
themselves. Do not start work in that window. February is support only, for the power
project importing the engine. Corridors in March, the backtest in April.

## 3. Hard rules. SPEC Part H, restated in full

These are not guidelines and they are not summarized here. Apply them mechanically.

1. **Zero content from the prior employer, ever.** The employer is named in the master
   specification and is deliberately not named anywhere in this repo, which is why you will
   not find the name here or in `SPEC.md`. The same redaction applies in the other 2
   project repos. Nothing sourced from that employment enters this project in any form: no
   data, no document, no figure, no recollected number, no paraphrase. Where provenance is
   unclear, it is excluded and the exclusion is flagged. The freight content uses only the
   corridor's banded public shipping assumptions and nothing else.

2. **No conduct language about any market participant, anywhere.** Not in a note, not in a
   figure caption, not in a code comment, not in a commit message.

3. **The engine freeze, 20 December 2026, is additive only afterward.** Signatures never
   change. The harness runs as CI here and as an import check in the other 2 projects.
   **THE RE PUBLICATION RULE applies to any post freeze bug that touches a published
   number: patch the engine, run the harness green, regenerate everything affected
   downstream, publish a dated correction note. Silent fixes are prohibited.** That is 4
   steps and all 4 are required; fixing the bug without regenerating and without the note
   is the prohibited case, not a lighter version of compliance.

4. **WRDS: history block only**, academic use, never republished, never a daily dependency.
   Splice dates recorded in the manifest. If a WRDS series is the only thing making a
   number work, the number does not ship.

5. **The test set runs once.** Any rerun request requires flagging the protocol and
   getting explicit confirmation. Every execution is logged in
   `config/backtest.yaml` under `protocol.test_set.execution_log`.

6. **Honest negatives ship.** Failed cointegration, an overlay that does not add value,
   Kirk breaking down somewhere relevant: each of these is a deliverable in its own right.
   Do not engineer around them and do not quietly reframe them.

7. **Style: numerals, no hyphens in prose, no marketing language, no emojis.** Expanded in
   section 4. Presentation order, when this project is shown alongside the others: after
   the power auction project for power and gas audiences, always before curve factors.

Additional standing constraints from Part K, which have the same force:

- The parity gate is the contract for the refactor. No science changes ride along.
- Every threshold and factor lives in `config/`. Changing 1 regenerates downstream under a
  new hash. Nothing is edited inline in a result file.

## 4. Style

- Numerals, not words, for numbers. Write 3, not three.
- No hyphens in prose. Code, CLI flags, file names, and kebab case identifiers keep the
  hyphens they syntactically need.
- No emojis. Anywhere, including commit messages.
- No marketing language. Banned outright: leverage, comprehensive, robust, seamless,
  holistic, streamline, supercharge, unlock, journey, paradigm, best in class, dive in,
  delve.
- No conduct language about any market participant.
- Lead with the result. Limitations are a first class section, written before the results
  section, not appended to it.

## 5. The 3 refusal points

If a task asks for 1 of these, stop and ask the user. Do not proceed, do not find a
workaround, do not do it and mention it afterward. Say which refusal point was hit and
what confirmation you need. SPEC Part K names 2 of these as the places an executing model
must refuse and escalate rather than comply.

1. **Reimplementing or forking a shared component instead of importing it.** In this repo
   the shared component is `statarb.pricing` itself, and the direction of the risk is
   reversed: the other 2 projects import it, so a change here that breaks them is the
   failure mode. After 20 December 2026 an additive change is fine and a signature change
   is not. Before that date, do not let a caller's convenience shape the API in a way that
   forces a later break. Equally, do not vendor or copy a component from another project
   into this one.

2. **Using revised or lookahead data vintages.** Point in time only. A series as published
   on the day, not as revised later. The D16 timestamp audit exists to catch this and an
   input that fails it voids the run rather than earning a caveat.

3. **Rerunning a locked test set without explicit confirmation.** The protocol in
   `config/backtest.yaml` is the record: thresholds frozen on data through 2021 or the
   first 60 percent, exactly 1 documented validation iteration, the test set from 2025
   onward run ONCE, and the execution count logged and stated in the note. A rerun request
   is flagged, requires explicit confirmation from the user, and is appended to the log.
   Editing the recorded count back down is falsifying the record.

## 6. The engine freeze, in detail

This is the constraint that makes 2 other projects possible, so it gets its own section.

**Freeze date: 20 December 2026.** On that date the API is frozen, a tag is cut, and the
engine note ships. From then on:

- **Additive only.** A new function is fine. A new keyword argument with a default that
  preserves existing behavior exactly is fine. Renaming a parameter, reordering
  parameters, changing a type, changing a default, or changing what an existing parameter
  means is a breaking change and is prohibited, regardless of how much better the new shape
  would be.
- **The harness runs as CI here and as an import check in the other 2 projects.** A change
  that leaves the harness red does not merge.
- **Contributions from the other 2 projects** arrive as additive pull requests, logged in
  D19 with the harness green on each.

**The re publication rule, for any post freeze bug that touches a published number.** All 4
steps, in order:

1. Patch the engine.
2. Run the harness and confirm it is green.
3. Regenerate every downstream artifact the bug affected, in this project and in the
   projects that import the engine.
4. Publish a dated correction note.

A silent fix is prohibited. So is a fix plus a regeneration with no note, and so is a note
with no regeneration. If steps 3 and 4 look disproportionate to the size of the bug, that
is the rule working as intended: the cost of the correction is the price of other projects
being able to depend on the numbers.

## 7. Working habits in this repo

- Read the config before the code. `config/` holds the spec thresholds and `config/legacy/`
  holds the pre refactor parameters, which are inputs to the parity gate and not defaults
  for new work. Load through `statarb.utils.config`. A module that opens a yaml directly,
  or hardcodes a threshold, a weight, a cost, or a unit conversion, is a defect.
- A value marked `UNSET` in a config does not feed a published artifact. Setting it is part
  of the deliverable that owns it. Record the justification next to the value, especially
  for the per basket deterministic term in `config/cointegration.yaml`, which is the most
  consequential free choice in the Johansen procedure.
- Stamp generated artifacts with `statarb.utils.config.config_hash` so any number traces
  back to the configuration that produced it.
- `data/raw/` is gitignored and is the record. `data/processed/` is gitignored and always
  regenerable from raw. A fix regenerates processed from raw; it never edits raw and never
  patches a processed file in place.
- Trigger evaluations get logged whether or not they fire: T3 Kalman instability, T5 cost
  flattery, the overlay verdict. A trigger that was checked and did not fire is evidence.
- Python 3.11 or later, type hints on public functions, Polars and NumPy and statsmodels as
  the default stack. Validate inputs and fail loudly.
- Never commit or push unless the user asks. Never force push.
- Commit messages are short: 1 line, under 72 characters where possible, no body unless the
  change genuinely needs 1 sentence the subject line cannot carry. No Co-Authored-By
  trailer, ever. The diff already shows what changed; the message says what and briefly why,
  not a restatement of the diff in prose.
