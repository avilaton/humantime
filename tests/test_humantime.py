"""Comprehensive tests for the humantime Python bindings."""

from __future__ import annotations

import datetime

import pytest

import humantime


class TestParseDuration:
    def test_hours_and_minutes(self):
        td = humantime.parse_duration("2h 37min")
        assert td == datetime.timedelta(hours=2, minutes=37)

    def test_single_second(self):
        td = humantime.parse_duration("1s")
        assert td == datetime.timedelta(seconds=1)

    def test_minutes_and_seconds(self):
        td = humantime.parse_duration("5m 30s")
        assert td == datetime.timedelta(minutes=5, seconds=30)

    def test_day_and_hours(self):
        td = humantime.parse_duration("1day 2hours")
        assert td == datetime.timedelta(days=1, hours=2)

    def test_milliseconds(self):
        td = humantime.parse_duration("500ms")
        assert td == datetime.timedelta(milliseconds=500)

    def test_nanoseconds(self):
        td = humantime.parse_duration("100ns")
        assert td == datetime.timedelta(microseconds=0.1)

    def test_weeks(self):
        td = humantime.parse_duration("2w")
        assert td == datetime.timedelta(weeks=2)

    def test_returns_timedelta(self):
        result = humantime.parse_duration("1h")
        assert isinstance(result, datetime.timedelta)

    def test_invalid_duration_raises(self):
        with pytest.raises(ValueError):
            humantime.parse_duration("not-a-duration")

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            humantime.parse_duration("")


class TestFormatDuration:
    def test_timedelta_input(self):
        result = humantime.format_duration(datetime.timedelta(hours=1))
        assert "1h" in result or "1hour" in result or "60m" in result or "3600s" in result

    def test_float_input(self):
        result = humantime.format_duration(3600.0)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_int_input(self):
        result = humantime.format_duration(60)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_zero(self):
        result = humantime.format_duration(0)
        assert isinstance(result, str)

    def test_complex_timedelta(self):
        td = datetime.timedelta(days=1, hours=2, minutes=30)
        result = humantime.format_duration(td)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            humantime.format_duration(-1.0)


class TestParseRfc3339:
    def test_basic_utc(self):
        dt = humantime.parse_rfc3339("2018-02-16T00:31:37Z")
        assert dt == datetime.datetime(2018, 2, 16, 0, 31, 37, tzinfo=datetime.timezone.utc)

    def test_returns_datetime(self):
        result = humantime.parse_rfc3339("2018-02-16T00:31:37Z")
        assert isinstance(result, datetime.datetime)

    def test_timezone_aware(self):
        result = humantime.parse_rfc3339("2018-02-16T00:31:37Z")
        assert result.tzinfo is not None

    def test_is_utc(self):
        result = humantime.parse_rfc3339("2020-01-01T00:00:00Z")
        assert result.tzinfo == datetime.timezone.utc

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            humantime.parse_rfc3339("not-a-timestamp")

    def test_invalid_date_raises(self):
        with pytest.raises(ValueError):
            humantime.parse_rfc3339("2018-13-01T00:00:00Z")


class TestParseRfc3339Weak:
    def test_space_instead_of_t(self):
        dt = humantime.parse_rfc3339_weak("2018-01-01 12:53:00")
        assert isinstance(dt, datetime.datetime)
        assert dt.year == 2018
        assert dt.month == 1
        assert dt.day == 1
        assert dt.hour == 12
        assert dt.minute == 53

    def test_basic_utc(self):
        dt = humantime.parse_rfc3339_weak("2018-02-16T00:31:37Z")
        assert dt == datetime.datetime(2018, 2, 16, 0, 31, 37, tzinfo=datetime.timezone.utc)

    def test_returns_datetime(self):
        result = humantime.parse_rfc3339_weak("2018-02-16T00:31:37Z")
        assert isinstance(result, datetime.datetime)

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            humantime.parse_rfc3339_weak("not-a-timestamp")


class TestFormatRfc3339:
    _ref = datetime.datetime(2018, 2, 16, 0, 31, 37, tzinfo=datetime.timezone.utc)

    def test_datetime_input(self):
        result = humantime.format_rfc3339(self._ref)
        assert result == "2018-02-16T00:31:37Z"

    def test_float_input(self):
        ts = self._ref.timestamp()
        result = humantime.format_rfc3339(ts)
        assert result == "2018-02-16T00:31:37Z"

    def test_int_input(self):
        ts = int(self._ref.timestamp())
        result = humantime.format_rfc3339(ts)
        assert isinstance(result, str)

    def test_returns_string(self):
        result = humantime.format_rfc3339(self._ref)
        assert isinstance(result, str)


class TestFormatRfc3339Seconds:
    _ref = datetime.datetime(2020, 6, 15, 12, 0, 0, tzinfo=datetime.timezone.utc)

    def test_basic(self):
        result = humantime.format_rfc3339_seconds(self._ref)
        assert result == "2020-06-15T12:00:00Z"

    def test_no_subseconds(self):
        result = humantime.format_rfc3339_seconds(self._ref)
        assert "." not in result


class TestFormatRfc3339Millis:
    _ref = datetime.datetime(2020, 6, 15, 12, 0, 0, tzinfo=datetime.timezone.utc)

    def test_basic(self):
        result = humantime.format_rfc3339_millis(self._ref)
        assert result == "2020-06-15T12:00:00.000Z"

    def test_has_millis(self):
        result = humantime.format_rfc3339_millis(self._ref)
        assert "." in result


class TestFormatRfc3339Micros:
    _ref = datetime.datetime(2020, 6, 15, 12, 0, 0, tzinfo=datetime.timezone.utc)

    def test_basic(self):
        result = humantime.format_rfc3339_micros(self._ref)
        assert result == "2020-06-15T12:00:00.000000Z"

    def test_has_micros(self):
        result = humantime.format_rfc3339_micros(self._ref)
        parts = result.split(".")
        assert len(parts) == 2
        frac = parts[1].rstrip("Z")
        assert len(frac) == 6


class TestFormatRfc3339Nanos:
    _ref = datetime.datetime(2020, 6, 15, 12, 0, 0, tzinfo=datetime.timezone.utc)

    def test_basic(self):
        result = humantime.format_rfc3339_nanos(self._ref)
        assert result == "2020-06-15T12:00:00.000000000Z"

    def test_has_nanos(self):
        result = humantime.format_rfc3339_nanos(self._ref)
        parts = result.split(".")
        assert len(parts) == 2
        frac = parts[1].rstrip("Z")
        assert len(frac) == 9


class TestRoundTrip:
    def test_duration_round_trip(self):
        original = datetime.timedelta(hours=2, minutes=30)
        formatted = humantime.format_duration(original)
        parsed = humantime.parse_duration(formatted)
        assert parsed == original

    def test_rfc3339_round_trip(self):
        original = datetime.datetime(2021, 5, 20, 10, 30, 0, tzinfo=datetime.timezone.utc)
        formatted = humantime.format_rfc3339(original)
        parsed = humantime.parse_rfc3339(formatted)
        assert parsed == original

    def test_parse_format_seconds(self):
        s = "2021-05-20T10:30:00Z"
        dt = humantime.parse_rfc3339(s)
        result = humantime.format_rfc3339_seconds(dt)
        assert result == s
