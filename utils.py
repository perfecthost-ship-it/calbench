import math
from datetime import datetime

# ---------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------

def fmt(value: float, dp: int = 3) -> str:
    """Format a float to fixed decimal places."""
    return f"{value:.{dp}f}"


def today() -> str:
    """Return today's date as YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")


# ---------------------------------------------------------
# Calibration maths helpers
# ---------------------------------------------------------

def calculate_error(applied: float, indicated: float) -> float:
    """Simple error calculation."""
    return indicated - applied


def within_tolerance(error: float, tolerance: float) -> bool:
    """Check if error is within tolerance."""
    return abs(error) <= tolerance


def linearity(readings):
    """
    Calculate linearity: max deviation from mean error.
    readings: list of Reading objects
    """
    if not readings:
        return 0.0

    errors = [r.error for r in readings]
    mean_err = sum(errors) / len(errors)
    return max(abs(e - mean_err) for e in errors)


# ---------------------------------------------------------
# Environmental window logic
# ---------------------------------------------------------

TEMP_MIN = 18
TEMP_MAX = 22
HUM_MIN = 30
HUM_MAX = 60

def environment_ok(temp: float, humidity: float) -> bool:
    """Check if environmental conditions are acceptable."""
    return TEMP_MIN <= temp <= TEMP_MAX and HUM_MIN <= humidity <= HUM_MAX


# ---------------------------------------------------------
# Code 128 barcode generator (simple subset)
# ---------------------------------------------------------

CODE128_CHARSET = {
    # Only the subset needed for serial numbers and IDs
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'A': 33, 'B': 34, 'C': 35, 'D': 36, 'E': 37,
    'F': 38, 'G': 39, 'H': 40, 'I': 41, 'J': 42,
    'K': 43, 'L': 44, 'M': 45, 'N': 46, 'O': 47,
    'P': 48, 'Q': 49, 'R': 50, 'S': 51, 'T': 52,
    'U': 53, 'V': 54, 'W': 55, 'X': 56, 'Y': 57,
    'Z': 58,
}

def code128_checksum(data: str) -> int:
    """Calculate Code 128 checksum for simple subset."""
    checksum = 104  # Start Code B
    for i, char in enumerate(data):
        checksum += CODE128_CHARSET.get(char, 0) * (i + 1)
    return checksum % 103


def make_code128(data: str) -> str:
    """
    Produce a simple Code 128 string:
    Start B + data + checksum + Stop
    (This is symbolic — your HTML renderer converts it to bars.)
    """
    checksum = code128_checksum(data)
    return f"START_B {data} {checksum} STOP"


# ---------------------------------------------------------
# Certificate helpers
# ---------------------------------------------------------

def certificate_pass_fail(max_error: float, tolerance: float, temp: float, humidity: float) -> str:
    """Combined pass/fail logic."""
    tol_ok = abs(max_error) <= tolerance
    env_ok = environment_ok(temp, humidity)

    if tol_ok and env_ok:
        return "PASS"
    return "FAIL"
