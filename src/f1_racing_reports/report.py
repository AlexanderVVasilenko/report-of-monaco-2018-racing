from dataclasses import dataclass
from datetime import datetime
from argparse import ArgumentParser
from operator import add


@dataclass
class RacerData:
    name: str
    team: str
    lap_time: str


# Load abbreviations from the file
def load_abbreviations(file_path: str) -> list[list[str]]:
    with open(file_path, "r") as abbreviations_file:
        return [row.strip().split("|") for row in abbreviations_file]


# Function to parse the log files and extract relevant information
def parse_logs(start_file: str, end_file: str, abbreviations_ls: list[list[str]]) -> \
        tuple[list[RacerData], list[RacerData]]:
    racers: dict[str, RacerData] = {}

    with open(start_file, 'r') as start_log, open(end_file, 'r') as end_log:
        for start_line, end_line in zip(start_log, end_log):
            start_data = parse_log_line(start_line)
            end_data = parse_log_line(end_line)

            if start_data and end_data:
                racer_code = start_data[0].strip()
                racer_info = get_racer_info(racer_code, abbreviations_ls)
                start_time = datetime.strptime(start_data[1].strip(), "%Y-%m-%d_%H:%M:%S.%f")
                end_time = datetime.strptime(end_data[1].strip(), "%Y-%m-%d_%H:%M:%S.%f")
                lap_time = str(end_time - start_time)

                racers[racer_code] = RacerData(
                    name=racer_info[0],
                    team=racer_info[1],
                    lap_time=lap_time
                )

    # Sort racers by lap time in ascending order
    sorted_racers = sorted(racers.items(), key=lambda x: x[1].lap_time)

    return [racer[1] for racer in sorted_racers[:15]], [racer[1] for racer in sorted_racers[15:]]


# Function to parse a log line into code and time
def parse_log_line(log_line: str) -> list[str]:
    code, time = log_line[:3], log_line[3:].strip()
    return [code, time] if len(code) == 3 and time else []


# Function to decode racer abbreviation
def get_racer_info(abbreviation: str, racers: list[list[str]]) -> list[str]:
    for racer in racers:
        if racer[0].strip() == abbreviation:
            return [racer[1].strip(), racer[2].strip()]


# Function to print the report
def print_report(fastest_racers: list[RacerData], bottom_racers: list[RacerData], is_reversed=False) -> None:
    if not is_reversed:
        print("Top 15 Racers:")
        for i, racer_data in enumerate(fastest_racers, start=1):
            print(f"{i}. {racer_data.name} | {racer_data.team} | {racer_data.lap_time}")

        print("\n" + '-' * 70 + "\n")

        print("Remaining Racers:")
        for i, racer_data in enumerate(bottom_racers, start=16):
            print(f"{i}. {racer_data.name} | {racer_data.team} | {racer_data.lap_time}")
    else:
        print("Remaining Racers:")
        for i in range(len(bottom_racers), 0, -1):
            print(
                f"{i + 15}. {bottom_racers[i - 1].name} | {bottom_racers[i - 1].team} | {bottom_racers[i - 1].lap_time}"
            )

        print("\n" + "-" * 70 + "\n")

        print("Top 15 Racers:")
        for i in range(len(fastest_racers), 0, -1):
            print(
                f"{i}. {fastest_racers[i - 1].name} | {fastest_racers[i - 1].team} | {fastest_racers[i - 1].lap_time}")


# Function to handle command-line arguments
def handle_arguments():
    arg_parser = ArgumentParser(description="Formula 1 Racing Report")
    arg_parser.add_argument("--drivers", action="store_true", help="Show list of drivers")
    arg_parser.add_argument("--order", choices=["asc", "desc"], help="Specify order for driver list")
    arg_parser.add_argument("--driver", help="Show statistics about a specific driver")

    return arg_parser


def main() -> tuple[list[RacerData], list[RacerData]]:
    abbreviations_file_path = "abbreviations.txt"
    start_log_file = "start.log"
    end_log_file = "end.log"

    abbreviations = load_abbreviations(abbreviations_file_path)
    return parse_logs(start_log_file, end_log_file, abbreviations)


def show_driver_list(ls_order: str | None) -> None:
    top_racers, remaining_racers = main()
    print_report(top_racers, remaining_racers, is_reversed=True if ls_order == "desc" else False)


def show_driver_statistics(name: str) -> None:
    racers = add(*main())
    for i, racer_data in enumerate(racers):
        if racer_data.name == name:
            print(f"{i + 1}. {racer_data.name} | {racer_data.team} | {racer_data.lap_time}")


# Main script
if __name__ == "__main__":
    parser = handle_arguments()
    args = parser.parse_args()

    if args.drivers:
        order = args.order if args.order else "asc"
        # Call the function to show the list of drivers with the specified order
        show_driver_list(order)

    elif args.driver:
        # Call the function to show statistics about the specified driver
        show_driver_statistics(args.driver)

    else:
        # If no arguments are provided, print the help message
        parser.print_help()
