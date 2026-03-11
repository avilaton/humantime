"""Python bindings for the Rust humantime crate."""

from __future__ import annotations

import datetime
from typing import Union

from humantime._humantime import (
    format_duration as _format_duration,
    format_rfc3339 as _format_rfc3339,
    format_rfc3339_micros as _format_rfc3339_micros,
    format_rfc3339_millis as _format_rfc3339_millis,
    format_rfc3339_nanos as _format_rfc3339_nanos,
    format_rfc3339_seconds as _format_rfc3339_seconds,
    parse_duration as _parse_duration,
    parse_rfc3339 as _parse_rfc3339,
    parse_rfc3339_weak as _parse_rfc3339_weak,
)

__version__ = "0.1.0"

__all__ = [
    "parse_duration",
    "format_duration",
    "parse_rfc3339",
    "parse_rfc3339_weak",
    "format_rfc3339",
    "format_rfc3339_seconds",
    "format_rfc3339_millis",
    "format_rfc3339_micros",
    "format_rfc3339_nanos",
]

_TimestampLike = Union[datetime.datetime, float, int]
_DurationLike = Union[datetime.timedelta, float, int]


def _to_unix_timestamp(ts: _TimestampLike) -> float:
    if isinstance(ts, datetime.datetime):
        return ts.timestamp()
    return float(ts)


def _to_total_seconds(d: _DurationLike) -> float:
    if isinstance(d, datetime.timedelta):
        return d.total_seconds()
    return float(d)


def parse_duration(s: str) -> datetime.timedelta:
    """Parse a human-friendly duration string and return a timedelta."""
    secs = _parse_duration(s)
    return datetime.timedelta(seconds=secs)


def format_duration(duration: _DurationLike) -> str:
    """Format a duration as a human-readable string."""
    total_secs = _to_total_seconds(duration)
    return _format_duration(total_secs)


def parse_rfc3339(s: str) -> datetime.datetime:
    """Parse a strict RFC 3339 timestamp and return a UTC datetime."""
    ts = _parse_rfc3339(s)
    return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)


def parse_rfc3339_weak(s: str) -> datetime.datetime:
    """Parse a relaxed RFC 3339 timestamp and return a UTC datetime."""
    ts = _parse_rfc3339_weak(s)
    return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)


def format_rfc3339(timestamp: _TimestampLike) -> str:
    """Format a timestamp as RFC 3339 with second precision."""
    return _format_rfc3339(_to_unix_timestamp(timestamp))


def format_rfc3339_seconds(timestamp: _TimestampLike) -> str:
    """Format a timestamp as RFC 3339 with second precision."""
    return _format_rfc3339_seconds(_to_unix_timestamp(timestamp))


def format_rfc3339_millis(timestamp: _TimestampLike) -> str:
    """Format a timestamp as RFC 3339 with millisecond precision."""
    return _format_rfc3339_millis(_to_unix_timestamp(timestamp))


def format_rfc3339_micros(timestamp: _TimestampLike) -> str:
    """Format a timestamp as RFC 3339 with microsecond precision."""
    return _format_rfc3339_micros(_to_unix_timestamp(timestamp))


def format_rfc3339_nanos(timestamp: _TimestampLike) -> str:
    """Format a timestamp as RFC 3339 with nanosecond precision."""
    return _format_rfc3339_nanos(_to_unix_timestamp(timestamp))
