# Technology history convergence: causal limits and verified changes

Baseline is the six complete full7 JUnit files: 783 PASS / 271 FAIL, 1,054 identities.
The secondary inventory retains all 101 normalization and 50 extraction failures.
It separates assertion stages from confirmed causes; the 25 downstream-gate cases
must not be described as one proven normalization bug.

## Confirmed repaired public causes

- FactStore addresses and flat requirement identifiers were conflated. Report
  normalization replaced namespace dots, and a later generic normalization call
  could repeat the damage. Fact fields now use canonical_fact_key; registered
  requirement aliases remain separate. Original quotations/values are unchanged.
- The confidentiality trigger prefilter required a remedy immediately after an
  obligation modality. A recipient in `应向…支付/赔偿` interrupted that pattern.
  The common ontology now separates trigger, modality and remedy, retaining the
  existing exclusions for caps, negations and unrelated events.
- The party splitter treated the recipient of 向/给/对 as a new obligated party.
  Whole-role-token filtering now preserves actor/object roles (including the
  许可方 / 被许可方 overlap) in the exact source span.
- The confidentiality-remedy family was not consistently registered before the
  FactStore freeze. The registry and rule/verifier adapters now consume the same
  family definition, with separate positive evidence and per-element searches.
- Migrating that family exposed a report-projection regression: support_summary
  was lost even though exact element ownership survived. It is now derived from
  the verified, source-specific proposition, not the whole rule or another party.

## Unresolved causes: do not claim these fixed

- In the historical cooperative report, a richer specialized element set is
  replaced in an intermediate generic adapter. Some old source bindings are
  themselves too weak, so blindly retaining all specialized states is unsafe.
  Before/after transition snapshots remain in round5_cooperative_*.json.
- Generic adverse findings still sometimes mix evaluation and source facts,
  producing FACT_ELEMENT_WITHOUT_PUBLISHED_BINDING. No gate exception was added.
- Document-list obligations can live in a parent clause while the object list is
  in child clauses. A verified parent-child proof chain is needed; the absence of
  a local delivery verb is not necessarily a true absence. The source review of
  the existing entrusted consistency fixture confirmed this pending boundary.
- Several assertions require old composite element IDs, exact clause numbers or
  broad PASS despite narrower residual elements. They have not been changed or
  counted as passing. Only independently documented obsolete assertions remain
  in the outdated-expectation category of the existing triage script.

## Run bookkeeping

- full8 was exploratory and stopped after a newly failing namespace assertion;
  it is incomplete and must not be used as a full-suite result.
- full9 completed: 801 PASS / 271 FAIL, one historical recovery and one new
  support-summary regression. The latter passed its unchanged focused test
  after fixing the public projection.
- Final comparison must use all six full10 files and compare against full7.
- The final live replay is live_round5_closed/report.json, normal file endpoint,
  same source SHA256 e5463c90d88b68b07544d560894b0d0487b67aa4e163bb96e817c50206283ef5.
- No legacy fallback, altered business expectation or relaxed verifier/gate was
  used. Test additions are separate from recovered historical failures.

## Completed final results

All six full10 batches completed: **803 PASS / 270 FAIL / 0 SKIP**.
Compared with the frozen baseline: **1 historical recovery, 0 new failures,
19 added passing tests, 0 removed tests**. The recovered identity is
`test_cooperative_development_advanced_regressions::test_shared_governance_and_creator_facts_survive_final_projection`.
The 100-test local public/protection run passed; the two intermediate regressions
were fixed without changing the original assertions.

Remaining first-failure triage: normalization 100, extraction 50, evidence binding
31, polarity 28, applicability 27, rendering 24, SEARCH_AUDIT 8, documented old
assertions 2. The large historical-failure clusters are **not** resolved by this
round; this is limited convergence, not full technical-contract stability.

The real file replay on current worker PID 15912 returned HTTP 200 and
REPORT_READY with zero release failures. Its 12 modeled-rule integrity scan found
zero unrelated evidence and zero false PARTIAL; the separate 40-covered-element
semantic scan found zero mismatches. These scans are not claims that every
historical contract now passes.
