# humantime (Python)

Python bindings for the Rust [`humantime`](https://docs.rs/humantime/latest/humantime/) crate — parse and format human-friendly durations and RFC 3339 timestamps with native Rust speed.

## Installation

```bash
uv add humantime
```

### Building from source

You need a Rust toolchain (install via [rustup](https://rustup.rs/)) and [uv](https://docs.astral.sh/uv/):

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and build
git clone https://github.com/avilaton/humantime.git
cd humantime
uv sync
uv run maturin develop
```

## Quick Start

```python
import humantime
import datetime

# Parse durations
td = humantime.parse_duration("2h 37min")
# datetime.timedelta(seconds=9420)

# Format durations
humantime.format_duration(datetime.timedelta(hours=2, minutes=37))
# '2h 37m'

# Parse RFC 3339 timestamps
dt = humantime.parse_rfc3339("2018-02-16T00:31:37Z")
# datetime.datetime(2018, 2, 16, 0, 31, 37, tzinfo=datetime.timezone.utc)

# Parse relaxed timestamps
dt = humantime.parse_rfc3339_weak("2018-01-01 12:53:00")

# Format timestamps
humantime.format_rfc3339(dt)
# '2018-01-01T12:53:00Z'

# Precision variants
humantime.format_rfc3339_millis(dt)
humantime.format_rfc3339_micros(dt)
humantime.format_rfc3339_nanos(dt)
```

## Supported Duration Units

| Unit         | Accepted strings                     |
|--------------|--------------------------------------|
| Nanoseconds  | `nsec`, `ns`                         |
| Microseconds | `usec`, `us`, `µs`                   |
| Milliseconds | `msec`, `ms`                         |
| Seconds      | `second`, `sec`, `s`                 |
| Minutes      | `minute`, `min`, `m`                 |
| Hours        | `hour`, `hr`, `hrs`, `h`             |
| Days         | `day`, `d`                           |
| Weeks        | `week`, `wk`, `wks`, `w`            |
| Months       | `month`, `M` (= 30.44 days)         |
| Years        | `year`, `yr`, `yrs`, `y` (= 365.25d)|

## API Reference

### Duration

- **`parse_duration(s: str) -> datetime.timedelta`** — Parse a human-friendly duration string.
- **`format_duration(duration: timedelta | float | int) -> str`** — Format a duration as a human-readable string.

### Timestamps

- **`parse_rfc3339(s: str) -> datetime.datetime`** — Parse a strict RFC 3339 timestamp.
- **`parse_rfc3339_weak(s: str) -> datetime.datetime`** — Parse a relaxed RFC 3339 timestamp.
- **`format_rfc3339(timestamp) -> str`** — Format with second precision.
- **`format_rfc3339_seconds(timestamp) -> str`** — Format with second precision (explicit).
- **`format_rfc3339_millis(timestamp) -> str`** — Format with millisecond precision.
- **`format_rfc3339_micros(timestamp) -> str`** — Format with microsecond precision.
- **`format_rfc3339_nanos(timestamp) -> str`** — Format with nanosecond precision.

All `timestamp` parameters accept `datetime.datetime`, `float`, or `int` (UNIX timestamp).

## Development

```bash
# 1. Install Rust: https://rustup.rs/
# 2. Install uv: https://docs.astral.sh/uv/

# 3. Set up the project (creates venv, installs deps)
uv sync

# 4. Build the Rust extension in dev mode
uv run maturin develop

# 5. Run the tests
uv run pytest tests/ -v
```

## License

MIT