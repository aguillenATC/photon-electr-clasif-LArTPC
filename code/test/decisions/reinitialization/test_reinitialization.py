import pytest
import unittest.mock
from tabu_search.decisions.reinitialization.criteria import ReinitializeIfStagnant
from tabu_search.base.tracker_user import TrackerUser
import tabu_search.tracking.trackers

@unittest.mock.patch("tabu_search.tracking.trackers.FitnessHistoryTracker", spec = tabu_search.tracking.trackers.FitnessHistoryTracker)
@pytest.mark.parametrize("variation, threshold, should_reinitialize",
                         [(0.3, 0.5, True), (0.5, 0.5, False), (0.7, 0.5, False)])
def test_reinitialization_if_progress_is_stagnant(mocker, variation, threshold, should_reinitialize):

    mock_tracker = tabu_search.tracking.trackers.FitnessHistoryTracker()
    mock_tracker.variation_last_n.return_value = variation
    TrackerUser.create_tracker_group("progress")
    TrackerUser.add_tracker_to_group("progress", "fitness_history", mock_tracker)
    reinitialization_criterion = ReinitializeIfStagnant(progress_threshold = threshold, steps_back = 1)

    assert reinitialization_criterion.should_reinitialize() == should_reinitialize

@unittest.mock.patch("tabu_search.tracking.trackers.FitnessHistoryTracker", spec = tabu_search.tracking.trackers.FitnessHistoryTracker)
@pytest.mark.parametrize("steps, should_reinitialize",
                         [(2, True), (1, False)])
def test_reinitialization_only_after_streak_longer_than_n_steps(mocker, steps, should_reinitialize):

    mock_tracker = tabu_search.tracking.trackers.FitnessHistoryTracker()
    mock_tracker.variation_last_n.return_value = 0.3
    TrackerUser.create_tracker_group("progress")
    TrackerUser.add_tracker_to_group("progress", "fitness_history", mock_tracker)
    reinitialization_criterion = ReinitializeIfStagnant(progress_threshold = 0.5, steps_back = 3)

    for _ in range(steps):

        reinitialization_criterion.should_reinitialize()

    assert reinitialization_criterion.should_reinitialize() == should_reinitialize
