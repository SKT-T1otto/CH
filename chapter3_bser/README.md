# BSER Phase 1A

Belief-guided Submodular Search–Execution Reallocation (BSER) is implemented
here as an offline, high-level finite allocation model. Phase 1A does not alter
the environment, train RMADDPG, or perform online reallocation.

The implementation consumes only `PlanningStateView`, constructs reachable
search and executor-standby candidates, and optimizes a nonnegative monotone
submodular objective under a partition matroid. Exact, standard greedy, lazy
greedy, search-only, random, and read-only PSE-snapshot evaluation are provided.

BSER is not implemented as an online controller or trained RMADDPG variant in
Phase 1A; those capabilities remain outside this phase.
