# Repository role

- CRK-Thesis-v2 is the only production repository.
- `core` is the sole shared executable implementation.
- CH3, CH4, and CH5 are read-only legacy references outside this repository.
- No runtime dependency on `legacy_adapters` or sibling repositories is allowed.

# Current status

- Phase 0B-2 is complete.
- Phase 0B-2.1 is repository closure only.
- BSER Phase 1A is the next permitted algorithm phase after this gate passes.

# Hard restrictions

- Preserve reward, observation, action, target, obstacle, success, and handoff semantics.
- Do not place chapter-specific algorithms inside `core` unless they are true shared infrastructure.
- Do not reintroduce `sys.path` injection or legacy imports.
- Do not commit checkpoints, models, raw data, or long-run outputs.
- Formal tests, manifests, compact summaries, and acceptance evidence may be committed.
- Existing Phase 0B-2 golden E0 data must not be overwritten.

# Required verification

- Run the complete test suite.
- Run core-only E0 against the frozen golden manifest.
- Run bounded training smoke and checkpoint roundtrip.
- Verify all 27 source-provenance hashes.
- Verify the pushed commit from a remote clean clone.
