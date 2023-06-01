import pytest
from datetime import datetime, timedelta
from get_events import GitHubEvents


def test_init():
    desired_events = ["ABC", "DEF"]
    offset_minutes = 20
    ghe_1 = GitHubEvents(desired_events, offset_minutes)
    ghe_2 = GitHubEvents(desired_events)

    assert ghe_1.events == []
    assert ghe_1.count_events == []
    assert ghe_1.url == "https://api.github.com/events"
    assert ghe_1.desired_events == desired_events
    assert ghe_1.offset_minutes == offset_minutes

    assert ghe_2.events == []
    assert ghe_2.count_events == []
    assert ghe_2.url == "https://api.github.com/events"
    assert ghe_2.desired_events == desired_events
    assert ghe_2.offset_minutes == 10
