"""Immutable event types and diagnostics for online BSER."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class BSEREvent(str, Enum):
    BELIEF_SHIFT = "BELIEF_SHIFT"
    OBSTACLE_DISCOVERED = "OBSTACLE_DISCOVERED"
    TARGET_FOUND = "TARGET_FOUND"
    EXECUTOR_TARGET_RECEIVED = "EXECUTOR_TARGET_RECEIVED"
    TARGET_LOST = "TARGET_LOST"
    EXECUTOR_INVALID = "EXECUTOR_INVALID"
    WAYPOINT_STALE = "WAYPOINT_STALE"
    PERIODIC_REFRESH = "PERIODIC_REFRESH"


@dataclass(frozen=True)
class EventDetection:
    events: Tuple[BSEREvent, ...]
    previous_entropy: float
    current_entropy: float
    belief_distance: float
    belief_shift_score: float
    new_obstacle_cells: int
    new_obstacle_probability_mass: float
    risk_change: float
    executor_reachable: bool
    stale_searcher_ids: Tuple[int, ...]
    executor_target_received: bool = False
    executor_planning_cost_relative_change: float = 0.0
    assignment_waypoints: Tuple[Tuple[int, Tuple[float, float, float]], ...] = ()

    def has(self, event: BSEREvent) -> bool:
        return event in self.events
