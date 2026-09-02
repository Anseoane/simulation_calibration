import argparse

from . import demand



def main():
    print("\nThe PhD was a mistake\n")
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

if __name__ == "__main__":
    main()