"""
Generates synthetic industrial sensor data for the pipeline demo.

Produces data/raw/sensor_readings.csv — 4 machines, 30 days, 10-minute intervals.
Deliberately injects: missing values, duplicates, invalid ranges, anomalous readings.
Data is entirely synthetic. Field ranges are loosely modelled on light industrial plant.
"""

import argparse
import os
import random

import numpy as np
import pandas as pd

SEED = 42
MACHINES = ["M-101", "M-102", "M-103", "M-104"]
START = "2026-08-01"
PERIODS = 30 * 24 * 6  # 30 days × 10-minute ticks

# Normal operating envelopes per machine (temperature baseline varies)
MACHINE_BASELINES = {
    "M-101": {"temp": 75.0, "pressure": 5.1, "vibration": 2.1, "energy": 48.0},
    "M-102": {"temp": 68.0, "pressure": 4.8, "vibration": 1.8, "energy": 42.0},
    "M-103": {"temp": 72.0, "pressure": 5.4, "vibration": 2.4, "energy": 51.0},
    "M-104": {"temp": 80.0, "pressure": 5.9, "vibration": 3.0, "energy": 55.0},
}


def build_timestamps() -> pd.DatetimeIndex:
    return pd.date_range(START, periods=PERIODS, freq="10min")


def normal_reading(timestamps: pd.DatetimeIndex, machine: str) -> pd.DataFrame:
    rng = np.random.default_rng(SEED + ord(machine[-1]))
    base = MACHINE_BASELINES[machine]
    n = len(timestamps)

    # Smooth drift added via a low-frequency sine wave
    t = np.linspace(0, 4 * np.pi, n)
    temp_drift = 3.0 * np.sin(t + rng.uniform(0, np.pi))

    return pd.DataFrame(
        {
            "timestamp": timestamps,
            "machine_id": machine,
            "temperature_c": base["temp"] + temp_drift + rng.normal(0, 0.8, n),
            "pressure_bar": base["pressure"] + rng.normal(0, 0.15, n),
            "vibration_mm_s": base["vibration"] + np.abs(rng.normal(0, 0.4, n)),
            "energy_kwh": base["energy"] + rng.normal(0, 3.0, n),
        }
    )


def inject_anomalies(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """Inject realistic anomalous spikes (temperature runaway, pressure surge, vibration burst)."""
    idx = rng.choice(df.index, size=30, replace=False)
    df.loc[idx[:10], "temperature_c"] += rng.uniform(18, 30, 10)  # thermal spike
    df.loc[idx[10:20], "pressure_bar"] += rng.uniform(3, 5, 10)   # pressure surge
    df.loc[idx[20:], "vibration_mm_s"] += rng.uniform(8, 15, 10)  # vibration burst
    return df


def inject_quality_issues(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """Inject data-quality problems the pipeline must detect and handle."""
    n = len(df)

    # Missing values — ~1 % of cells in each sensor column
    for col in ["temperature_c", "pressure_bar", "vibration_mm_s", "energy_kwh"]:
        mask = rng.random(n) < 0.01
        df.loc[mask, col] = np.nan

    # Invalid out-of-range readings
    bad_temp_idx = rng.choice(df.index, size=15, replace=False)
    df.loc[bad_temp_idx[:8], "temperature_c"] = rng.uniform(150, 250, 8)   # implausible high
    df.loc[bad_temp_idx[8:], "temperature_c"] = rng.uniform(-60, -30, 7)   # implausible low

    bad_pressure_idx = rng.choice(df.index, size=10, replace=False)
    df.loc[bad_pressure_idx, "pressure_bar"] = rng.uniform(15, 25, 10)     # sensor saturation

    bad_vib_idx = rng.choice(df.index, size=8, replace=False)
    df.loc[bad_vib_idx, "vibration_mm_s"] = rng.uniform(25, 50, 8)        # beyond physical limits

    # Duplicate rows — 3 complete duplicates appended
    dupes = df.sample(n=3, random_state=SEED)
    df = pd.concat([df, dupes], ignore_index=True)

    # Null machine_id on a handful of rows
    null_id_idx = rng.choice(df.index, size=4, replace=False)
    df.loc[null_id_idx, "machine_id"] = np.nan

    return df


def main(output_path: str) -> None:
    rng = np.random.default_rng(SEED)
    timestamps = build_timestamps()

    frames = []
    for machine in MACHINES:
        df = normal_reading(timestamps, machine)
        df = inject_anomalies(df, np.random.default_rng(SEED + ord(machine[-1]) + 100))
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    combined = combined.sample(frac=1, random_state=SEED).reset_index(drop=True)
    combined = inject_quality_issues(combined, rng)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    combined.to_csv(output_path, index=False)
    print(f"Generated {len(combined)} rows → {output_path}")
    print(f"  Machines : {sorted(combined['machine_id'].dropna().unique())}")
    print(f"  Date range: {combined['timestamp'].min()} – {combined['timestamp'].max()}")
    print(f"  Null cells: {combined.isnull().sum().to_dict()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic sensor dataset")
    parser.add_argument(
        "--output",
        default=os.path.join(os.path.dirname(__file__), "..", "data", "raw", "sensor_readings.csv"),
        help="Output CSV path",
    )
    args = parser.parse_args()
    main(args.output)
