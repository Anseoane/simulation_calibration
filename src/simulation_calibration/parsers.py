import csv
from datetime import datetime, timedelta
import json
from statistics import fmean

def _as_datetime(value):
    return datetime.fromisoformat(value) if isinstance(value, str) else value

class GroundTruth:
    def __init__(self, raw_data_file, datetime_col, segment_col):
        self.raw_data_file = raw_data_file
        self.segments = {}
        self.time_intervals = {}
        with open(raw_data_file, newline="") as f:
            for row in csv.DictReader(f):
                dt = datetime.fromisoformat(row.pop(datetime_col))
                segment_id = row.pop(segment_col)
                magnitudes = {
                    name: float(v) if v else None
                    for name, v in row.items()
                }
                self.segments.setdefault(segment_id, [])
                self.segments[segment_id].append((dt, magnitudes))
                self.time_intervals.setdefault(dt, {})
                self.time_intervals[dt][segment_id] = magnitudes["avg_speed"]

        for segm_records in self.segments.values():
            segm_records.sort(key=lambda record: record[0])

        self.time_intervals = dict(sorted(self.time_intervals.items()))


    @property
    def segment_ids(self):
        return sorted(self.segments, key=int)

    def get_time_interval(self, segment_id, t_start=None, t_end=None):
        t_start = _as_datetime(t_start)
        t_end = _as_datetime(t_end)

        selected_records = [
            (dt, magnitudes)
            for dt, magnitudes in self.segments[str(segment_id)]
            if (t_start is None or dt >= t_start)
            and (t_end is None or dt < t_end)
        ]

        if not selected_records:
            return {}

        return selected_records

    def build_od_matrix(self, sinks_sources, t_start=None, t_end=None):
        t_start = _as_datetime(t_start)
        t_end = _as_datetime(t_end)

        selected_records = [
            speeds
            for dt, speeds in self.time_intervals.items()
            if (t_start is None or dt >= t_start)
            and (t_end is None or dt < t_end)
        ]
        print(selected_records)


class Metadata:
    def __init__(self, metadata_file):
        self.metadata_file = metadata_file
        with open(self.metadata_file) as f:
            metadata = json.load(f)
        self.assoc_network = metadata["metadata"]["network_file"]
        self.segments = metadata["segments"]

    def get_sinks_sources(self):
        sumo_sinks = []
        sumo_sources = []
        for segm_info in self.segments.values():
            if segm_info["sink_source_role"] == "sink":
                sumo_sink = segm_info["edges"][-1]
                sumo_sinks.append(sumo_sink)
            elif segm_info["sink_source_role"] == "source":
                sumo_source = segm_info["edges"][0]
                sumo_sources.append(sumo_source)
            else:
                continue

        return {"sinks": sumo_sinks, "sources": sumo_sources}
