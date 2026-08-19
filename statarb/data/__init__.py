"""Data layer. SPEC Part D deliverables D1 and D2.

D1  Data audit note. Every series in the universe with its verified source, access
    method, history depth, license, and a PASS or CUT verdict. Includes the DME Oman
    check as the crude third leg candidate, and confirms the Baltic indices CUT.
    Gate: the universe is locked and no downstream work runs on an unverified series.

D2  Continuous futures builder, built here. Per contract series where free sources allow,
    otherwise documented source rolls. Own rolls at N = 5 business days before expiry, back
    adjusted additive, with the unadjusted series retained rather than discarded. Roll
    calendars per market.
    Gate: cointegration robustness later runs on BOTH the adjusted and the unadjusted
    series. That is why the unadjusted one is kept.
    This deliverable originally lived in a shared platform repo, retired 18 August 2026 in
    favor of each project owning its own ingestion. See SCOPE-LOCK.md and
    docs/D1-data-audit.md section 10 for what that repo had recorded before deletion.

Unit conventions that must not be re derived anywhere else: Henry Hub converts at
1 MMBtu = 0.293071 MWh, and that factor lives in config/baskets.yaml. TTF is native
EUR/MWh. FX comes from ECB reference rates.

WRDS Datastream is a spliced history block only: academic use, never republished, never a
daily dependency, splice dates recorded in the manifest. The free feed stays the living
source.
"""
