"""Public-interface state sampling for the E2 experiment harness."""

from __future__ import annotations

from dataclasses import replace

from core.mapping.planning_state import PlanningAgentView, PlanningStateView, extract_planning_state


class OnlinePlanningStateProvider:
    def __init__(self, env, refresh_interval: int = 20):
        self.env = env
        self.refresh_interval = int(refresh_interval)
        self.cached: PlanningStateView | None = None

    def initialize(self) -> PlanningStateView:
        self.cached = extract_planning_state(self.env)
        return self.cached

    def snapshot(self, *, force: bool = False) -> PlanningStateView:
        if self.cached is None:
            return self.initialize()
        task = self.env.get_task_state()
        transition = bool(task.target_found) != bool(self.cached.target_found)
        refresh = force or transition or (self.refresh_interval > 0 and task.step % self.refresh_interval == 0)
        if refresh:
            self.cached = extract_planning_state(self.env)
            return self.cached
        public = self.env.get_agent_state()
        agents = tuple(
            replace(
                old,
                position=tuple(public.positions[old.agent_id]),
                velocity=tuple(public.velocities[old.agent_id]),
                current_navigation_target=tuple(public.navigation_targets[old.agent_id]),
            )
            for old in self.cached.agents
        )
        self.cached = replace(
            self.cached,
            step=int(task.step),
            target_found=bool(task.target_found),
            mission_complete=bool(task.mission_complete),
            agents=agents,
        )
        return self.cached
