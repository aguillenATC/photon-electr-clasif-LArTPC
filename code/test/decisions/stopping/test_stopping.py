import pytest
import unittest.mock
from tabu_search.decisions.stopping.criteria import IterationLimit
from tabu_search.base.tracker_user import TrackerUser
import tabu_search.tracking.trackers

@unittest.mock.patch("tabu_search.tracking.trackers.SolutionHistoryTracker", spec = tabu_search.tracking.trackers.SolutionHistoryTracker)
@pytest.mark.parametrize("steps, should_stop",
                         [(9, False), (10, True), (20, True)])
def test_stopping_after_iteration_limit(mocker, steps, should_stop):

    mock_tracker = tabu_search.tracking.trackers.SolutionHistoryTracker()
    mock_tracker.get_step_count.return_value = steps
    TrackerUser.create_tracker_group("progress")
    TrackerUser.add_tracker_to_group("progress", "solution_history", mock_tracker)
    stopping_criterion = IterationLimit(10)

    assert stopping_criterion.should_stop() == should_stop

@pytest.mark.parametrize("steps", [0, -1])
def test_stopping_after_iteration_limit_rejects_invalid_limit(steps):

    with pytest.raises(ValueError):

        IterationLimit(steps)
