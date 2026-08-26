from dataclasses import dataclass, field
from typing import List, Optional
from statistics import mean

# -----------------------------
# Instrument Model
# -----------------------------

@dataclass
class Instrument:
    id: Optional[int]
    serial: str
    model: str
    range_min: float
    range_max: float
    resolution: float
    notes: str = ""

    def in_range(self, value: float) -> bool:
        return self.range_min <= value <= self.range_max


# -----------------------------
# Reading Model
# -----------------------------

@dataclass
class Reading:
    applied: float
    indicated: float

    @property
    def error(self) -> float:
        return self.indicated - self.applied


# -----------------------------
# Certificate Model
# -----------------------------

@dataclass
class Certificate:
    id: Optional[int]
    instrument_id: int
    date: str
    technician: str
    environment_temp: float
    environment_humidity: float
    readings: List[Reading] = field(default_factory=list)
    pass_fail: Optional[str] = None

    # -------------------------
    # Core calibration maths
    # -------------------------

    @property
    def mean_error(self) -> float:
        if not self.readings:
            return 0.0
        return mean(r.error for r in self.readings)

    @property
    def max_error(self) -> float:
        if not self.readings:
            return 0.0
        return max(abs(r.error) for r in self.readings)

    @property
    def linearity(self) -> float:
        """Simple linearity metric: max deviation from mean error."""
        if not self.readings:
            return 0.0
        m = self.mean_error
        return max(abs(r.error - m) for r in self.readings)

    def evaluate(self, tolerance: float) -> str:
        """
        Evaluate pass/fail based on:
        - max error
        - environmental window
        """
        env_ok = (18 <= self.environment_temp <= 22) and (30 <= self.environment_humidity <= 60)
        tol_ok = self.max_error <= tolerance

        if env_ok and tol_ok:
            self.pass_fail = "PASS"
        else:
            self.pass_fail = "FAIL"

        return self.pass_fail


# -----------------------------
# Reference Equipment Model
# -----------------------------

@dataclass
class Equipment:
    id: Optional[int]
    name: str
    serial: str
    expiry: str
    uncertainty: float

    def is_valid(self, today: str) -> bool:
        """Simple expiry check (string compare assumes YYYY-MM-DD)."""
        return today <= self.expiry
