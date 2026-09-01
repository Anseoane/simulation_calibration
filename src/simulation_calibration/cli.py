import argparse

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
    args = parser.parse_args()


    print(args.gt_data)

if __name__ == "__main__":
    main()