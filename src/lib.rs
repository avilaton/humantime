use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use std::time::{Duration, SystemTime, UNIX_EPOCH};

#[pyfunction]
fn parse_duration(s: &str) -> PyResult<f64> {
    humantime::parse_duration(s)
        .map(|d| d.as_secs_f64())
        .map_err(|e| PyValueError::new_err(format!("Invalid duration '{}': {}", s, e)))
}

#[pyfunction]
fn format_duration(total_secs: f64) -> PyResult<String> {
    if total_secs < 0.0 {
        return Err(PyValueError::new_err("Duration cannot be negative"));
    }
    let duration = Duration::from_secs_f64(total_secs);
    Ok(humantime::format_duration(duration).to_string())
}

fn secs_to_system_time(timestamp: f64) -> PyResult<SystemTime> {
    if timestamp < 0.0 {
        return Err(PyValueError::new_err("Timestamp cannot be negative"));
    }
    let duration = Duration::from_secs_f64(timestamp);
    UNIX_EPOCH
        .checked_add(duration)
        .ok_or_else(|| PyValueError::new_err("Timestamp out of range"))
}

#[pyfunction]
fn parse_rfc3339(s: &str) -> PyResult<f64> {
    humantime::parse_rfc3339(s)
        .map_err(|e| PyValueError::new_err(format!("Invalid RFC 3339 timestamp '{}': {}", s, e)))
        .and_then(|t| {
            t.duration_since(UNIX_EPOCH)
                .map(|d| d.as_secs_f64())
                .map_err(|e| PyValueError::new_err(format!("Timestamp before epoch: {}", e)))
        })
}

#[pyfunction]
fn parse_rfc3339_weak(s: &str) -> PyResult<f64> {
    humantime::parse_rfc3339_weak(s)
        .map_err(|e| PyValueError::new_err(format!("Invalid timestamp '{}': {}", s, e)))
        .and_then(|t| {
            t.duration_since(UNIX_EPOCH)
                .map(|d| d.as_secs_f64())
                .map_err(|e| PyValueError::new_err(format!("Timestamp before epoch: {}", e)))
        })
}

#[pyfunction]
fn format_rfc3339(timestamp: f64) -> PyResult<String> {
    let st = secs_to_system_time(timestamp)?;
    Ok(humantime::format_rfc3339_seconds(st).to_string())
}

#[pyfunction]
fn format_rfc3339_seconds(timestamp: f64) -> PyResult<String> {
    let st = secs_to_system_time(timestamp)?;
    Ok(humantime::format_rfc3339_seconds(st).to_string())
}

#[pyfunction]
fn format_rfc3339_millis(timestamp: f64) -> PyResult<String> {
    let st = secs_to_system_time(timestamp)?;
    Ok(humantime::format_rfc3339_millis(st).to_string())
}

#[pyfunction]
fn format_rfc3339_micros(timestamp: f64) -> PyResult<String> {
    let st = secs_to_system_time(timestamp)?;
    Ok(humantime::format_rfc3339_micros(st).to_string())
}

#[pyfunction]
fn format_rfc3339_nanos(timestamp: f64) -> PyResult<String> {
    let st = secs_to_system_time(timestamp)?;
    Ok(humantime::format_rfc3339_nanos(st).to_string())
}

#[pymodule]
fn _humantime(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse_duration, m)?)?;
    m.add_function(wrap_pyfunction!(format_duration, m)?)?;
    m.add_function(wrap_pyfunction!(parse_rfc3339, m)?)?;
    m.add_function(wrap_pyfunction!(parse_rfc3339_weak, m)?)?;
    m.add_function(wrap_pyfunction!(format_rfc3339, m)?)?;
    m.add_function(wrap_pyfunction!(format_rfc3339_seconds, m)?)?;
    m.add_function(wrap_pyfunction!(format_rfc3339_millis, m)?)?;
    m.add_function(wrap_pyfunction!(format_rfc3339_micros, m)?)?;
    m.add_function(wrap_pyfunction!(format_rfc3339_nanos, m)?)?;
    Ok(())
}
