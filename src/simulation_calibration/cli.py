import argparse

from . import demand
from . import parsers

def main():

    DATETIME_COL = "datetime"
    SEGMENT_COL = "location_id"



    print("The PhD was a mistake\n")
    print("Starting calibration process\n")

    parser = argparse.ArgumentParser(
        prog="SimCal",
        description="CLI utility that acts as the face for the" \
        " utility for the calibration of microscopic simulations"
    )
    parser.add_argument("gt_data", type=str)
    parser.add_argument("network", type=str)
    parser.add_argument("metadata", type=str)
    args = parser.parse_args()

    gt_source_file = args.gt_data
    sumo_network_file = args.network
    metadata_file = args.metadata

    gt_source = parsers.GroundTruth(
        raw_data_file=gt_source_file,
        datetime_col=DATETIME_COL,
        segment_col=SEGMENT_COL
        )

    metadata = parsers.Metadata(metadata_file=metadata_file)
    sinks_sources = metadata.get_sinks_sources()


    od_matrix = gt_source.build_od_matrix(
        sinks_sources=sinks_sources,
        t_start="2025-10-06 06:00:00",
        t_end="2025-10-06 11:00:00"
    )

    gt_selection = gt_source.get_time_interval(
        segment_id="17",
        t_start="2025-10-06 06:00:00",
        t_end="2025-10-06 11:00:00"
    )




if __name__ == "__main__":
    main()