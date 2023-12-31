# Formula 1 Racing Analytics

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/downloads/release)

## Overview

Formula 1 Racing Analytics is a Python package that provides tools for analyzing Formula 1 racing data and generating insightful reports. The package parses racing log files, extracts relevant information, and offers functionalities to view driver statistics and race results.

## Features

- Parse Formula 1 racing log files
- Extract racer information and lap times
- View top 15 racers and remaining racers
- Generate reports based on different criteria

## Installation

```bash
py -m pip install --index-url https://test.pypi.org/simple --no-deps f1_racing_reports
```

## Examples of usage

```bash
python src/f1_racing_reports/report.py --drivers --order desc
```
