# tests/test_report.py
from datetime import datetime
from src.f1_racing_reports.report import parse_logs, load_abbreviations, RacerData


def test_load_abbreviations():
    abbreviations_file_path = "abbreviations.txt"
    # Assuming you have a test abbreviations file
    abbreviations = load_abbreviations(abbreviations_file_path)

    assert abbreviations is not None
    assert len(abbreviations) > 0


def test_parse_logs():
    start_file = "start.log"
    end_file = "end.log"
    abbreviations_file_path = "abbreviations.txt"

    abbreviations = load_abbreviations(abbreviations_file_path)
    top_racers, remaining_racers = parse_logs(start_file, end_file, abbreviations)

    assert top_racers is not None
    assert remaining_racers is not None

    # Add more specific assertions based on your test data and expectations
    assert len(top_racers) == 15
    assert len(remaining_racers) > 0


def test_racer_data():
    racer_data = RacerData(name="Test Driver", team="Test Team", lap_time="0:01:30.000", driver_id="")

    assert racer_data.name == "Test Driver"
    assert racer_data.team == "Test Team"
    assert racer_data.lap_time == "0:01:30.000"

    # Add more specific assertions based on your RacerData class definition

# Add more tests as needed for other functionalities

# If you are using pytest, you can run the tests using the following command:
# pytest tests/
