# CRK-Thesis-v2

Self-contained research code for the three algorithm chapters of the multi-agent
AUV thesis. Phase 0B-2 is complete; Phase 0B-2.1 closes and independently
verifies the remote repository.

## Repository boundaries

- `core` is the sole shared executable production implementation.
- `chapter3_bser` is reserved for Chapter 3 BSER.
- `chapter4_rcag` is reserved for Chapter 4 RCAG.
- `chapter5_vsgc` is reserved for Chapter 5 VSGC.

BSER, RCAG, and VSGC are not implemented yet. The next permitted algorithm
phase after the remote-closure gate is BSER Phase 1A.

## Implemented shared core

The core currently contains the mission environment, moving target, unknown
obstacles, belief and occupancy updates, online A*, fixed reliable handoff,
MADDPG, replay buffer, deterministic scenarios, and training/evaluation
infrastructure. It has no runtime dependency on historical adapters or sibling
CH3/CH4/CH5 repositories.

## Frozen environment contract

- Agents: 4
- Role order: `search_fast`, `search_balanced`, `search_precise`, `executor`
- Observation dimensions: `[28, 28, 28, 28]`
- Action dimensions: `[3, 3, 3, 3]`
- Canonical profile: `M20_MOVING_UNKNOWN_MULTI`

## Quick verification

```powershell
conda run -n AUV python -B -m unittest discover -s tests -p "test_*.py" -v
conda run -n AUV python -B -m tools.run_core_training_smoke --output-dir "$env:TEMP\phase0b2_smoke"
conda run -n AUV python -B -m tools.run_core_golden_e0
```

Phase 0B-2 acceptance: 17/17 tests, both E0 rounds 60/60, maximum
absolute difference 0.0, zero task-event mismatches, and bounded training smoke
with checkpoint roundtrip passed.

Do not commit checkpoints, models, raw long-run data, or generated training
outputs. Formal compact manifests, summaries, tests, and acceptance evidence may
be committed.
