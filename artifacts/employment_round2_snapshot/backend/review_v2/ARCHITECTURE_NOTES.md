# Contract Review 6.7 Architecture Notes

- Resolved Domain and Resolved Perspective must each have one source of truth.
- Machine-readable truth must never leak as machine language into the production report.
- Fact polarity must survive from structured state to user-facing language.
- Contractual absence is not identical to legal exposure.
- Coverage -> Default Law -> Effective Gap -> Residual Risk.
- A recommendation must be evaluated from the reviewed party's perspective.
- A recommendation must not silently weaken existing protection.

The 6.7 Final Freeze Patch does not make the domain smarter. It makes the already-correct domain truth survive intact through law, recommendation, and production rendering.

## Final Freeze Hotfix Invariants

- One objective contractual fact must have one canonical truth state.
- Different Reviews may ask different questions about the same Claim, but they cannot disagree about the same semantic element.
- Coverage describes the contract. Default Law describes the legal fallback. Effective Gap describes the real remaining exposure.
- If law changes the final risk judgment, its authority provenance must survive into the production report.
- A missing drafting element does not automatically justify adding that element to the contract.
- Recommendations must compare the user's current effective protection against the proposed effective protection.
- A recommendation that narrows rights, increases liability, or shifts risk to the reviewed party is not risk mitigation unless the tradeoff is explicit and justified.
- Quality 6.7 is frozen only when Fact -> Claim -> Review -> Law -> Finding -> Recommendation -> Report preserves one consistent truth.

## Final Release Hotfix Invariants

- Coverage tells us what the contract says.
- Default Law tells us what the law supplies when the contract is silent or incomplete.
- Effective Gap tells us what remains legally or operationally exposed after both are considered.
- A missing element does not automatically create a recommendation.
- Recommendation is a first-class object with explicit provenance, perspective, impact, and status.
- Every production renderer consumes the same FinalRecommendationSet and cannot generate recommendations independently.
- A citation must support the exact legal proposition for which it is displayed.
- A related statute is not necessarily a supporting statute.
- Drafting value is not the same as a statutory requirement.
- When Default Law changes the final judgment, the supporting authority provenance must survive to the production report.
- A review is complete only when Contract Truth, Legal Truth, Risk Truth, Recommendation Truth, and Report Truth are consistent.

## Freeze Closure Invariants

- Applicability precedes gap analysis.
- NOT_APPLICABLE is not MISSING.
- A legal authority and a default-law conclusion must consume the same resolved legal proposition.
- A composite legal element must not hide different legal rules behind one coverage state.
- PASS does not have one universal meaning.
- For a positive requirement, PASS means the required protection is present.
- For a negative clause check, PASS means the adverse clause was not found.
- Review polarity is part of review semantics, not presentation decoration.
- The renderer must describe what actually happened, not merely translate PASS into "the contract contains this clause".
- Quality 6.7 is frozen when Applicability Truth, Contract Truth, Legal Truth, Risk Truth, Recommendation Truth, and Narrative Truth remain consistent end to end.
