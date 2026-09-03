import csv
from datetime import datetime, timedelta
import itertools
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

    def build_od_matrix(self, segm_sinks_sources, t_start=None, t_end=None):
        t_start = _as_datetime(t_start)
        t_end = _as_datetime(t_end)

        sinks = segm_sinks_sources["segm_sinks"]
        sources = segm_sinks_sources["segm_sources"]


        selected_records = [
            (dt, speeds)
            for dt, speeds in self.time_intervals.items()
            if (t_start is None or dt >= t_start)
            and (t_end is None or dt < t_end)
        ]

        possible_od_pairs = list(itertools.product(sources, sinks))

        weights_by_time = {}
        od_matrix = {}
        for record in selected_records:
            speeds = record[1]
            sink_speeds = [speeds[sink] for sink in sinks]
            sink_weights = {
                sink: speeds[sink] / sum(sink_speeds) for sink in sinks
            }
            od_matrix.setdefault(record[0], )

            weights_by_time.setdefault(record[0], sink_weights)

        od_matrix = {}
        for record in selected_records:
            od_matrix.setdefault(record[0], {})
            for od_pair in possible_od_pairs:
                weights = weights_by_time[record[0]]
                od_matrix[record[0]].setdefault(od_pair, weights[od_pair[1]])
                                     

        print(od_matrix)

        return od_matrix


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
        segm_sinks = []
        segm_sources = []

        for segm_id, segm_info in self.segments.items():

            if segm_info["sink_source_role"] == "sink":
                sumo_sinks.append(segm_info["edges"][-1])
                segm_sinks.append(segm_id)

            elif segm_info["sink_source_role"] == "source":
                sumo_sources.append(segm_info["edges"][0])
                segm_sources.append(segm_id)

            else:
                continue
            
        return {
            "sumo_sinks": sumo_sinks,
            "sumo_sources": sumo_sources,
            "segm_sources": segm_sources,
            "segm_sinks": segm_sinks
        }