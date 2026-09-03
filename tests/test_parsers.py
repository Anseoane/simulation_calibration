import json
from datetime import datetime, timedelta

import pytest

from simulation_calibration.parsers import GroundTruth, Metadata


@pytest.fixture
def gt(tmp_path):
    """Two segments sampled every 5 min over one hour."""
    path = tmp_path / "interpolated_data.csv"
    lines = ["datetime,avg_ttime,avg_speed,location_id"]
    start = datetime(2025, 10, 6, 6, 0)
    for location_id, base in (("17", 100.0), ("31", 200.0)):
        for i in range(12):
            t = start + i * timedelta(minutes=5)
            lines.append(f"{t},{base + i},15.0,{location_id}")
    path.write_text("\n".join(lines))
    return GroundTruth(path, "datetime", "location_id")


def test_splits_into_segments(gt):
    assert gt.segment_ids == ["17", "31"]
    assert len(gt.segments["17"]) == 12
    assert gt.segments["17"][0] == (
        datetime(2025, 10, 6, 6, 0),
        {"avg_ttime": 100.0, "avg_speed": 15.0},
    )


def test_time_interval_is_half_open(gt):
    records = gt.get_time_interval("17", "2025-10-06 06:05:00", "2025-10-06 06:25:00")

    assert [t for t, _ in records] == [
        datetime(2025, 10, 6, 6, 5) + i * timedelta(minutes=5) for i in range(4)
    ]


def test_time_interval_defaults_to_all_the_data(gt):
    assert len(gt.get_time_interval(17)) == 12
    assert gt.get_time_interval("17", t_start="2030-01-01") == {}


@pytest.fixture
def metadata(tmp_path):
    """17 and 31 are sources, 60 and 72 sinks, 111 a through segment."""
    path = tmp_path / "edges_map.json"
    path.write_text(json.dumps({
        "metadata": {"network_file": "praza_america.net.xml"},
        "segments": {
            "17": {"edges": ["E1"], "sink_source_role": "source"},
            "31": {"edges": ["E2"], "sink_source_role": "source"},
            "60": {"edges": ["E3"], "sink_source_role": "sink"},
            "72": {"edges": ["E4"], "sink_source_role": "sink"},
            "111": {"edges": ["E5"], "sink_source_role": "through"},
        },
    }))
    return Metadata(path)


@pytest.fixture
def gt_od(tmp_path):
    """One hour of data; sink 60 carries 3x the volume of sink 72."""
    path = tmp_path / "od_data.csv"
    lines = ["datetime,avg_flow,location_id"]
    start = datetime(2025, 10, 6, 6, 0)
    for location_id, flow in (("17", 50.0), ("31", 50.0), ("60", 300.0),
                              ("72", 100.0), ("111", 999.0)):
        for i in range(12):
            lines.append(f"{start + i * timedelta(minutes=5)},{flow},{location_id}")
    path.write_text("\n".join(lines))
    return GroundTruth(path, "datetime", "location_id")


def test_od_matrix_splits_sources_by_sink_share(gt_od, metadata):
    od = gt_od.get_od_matrix(
        metadata, "2025-10-06 06:00:00", "2025-10-06 07:00:00", "avg_flow"
    )

    # through segments are left out entirely
    assert set(od) == {"17", "31", "60", "72"}
    # sources split over the sinks in proportion to sink volume
    assert od["17"] == {"60": 0.75, "72": 0.25, "17": 0.0, "31": 0.0}
    assert od["31"] == od["17"]
    # sink rows are all zero
    assert set(od["60"].values()) == {0.0}
    assert sum(od["72"].values()) == 0.0


def test_od_matrix_follows_the_interval(gt_od, metadata):
    """Dropping 60's volume in the second half hour reweights the split."""
    for _, magnitudes in gt_od.segments["60"][6:]:
        magnitudes["avg_flow"] = 100.0

    od = gt_od.get_od_matrix(
        metadata, "2025-10-06 06:30:00", "2025-10-06 07:00:00", "avg_flow"
    )

    assert od["17"]["60"] == pytest.approx(0.5)
    assert od["17"]["72"] == pytest.approx(0.5)


def test_od_matrix_without_measurements_raises(gt_od, metadata):
    with pytest.raises(ValueError, match="undefined"):
        gt_od.get_od_matrix(metadata, "2030-01-01", "2030-01-02", "avg_flow")
