"""
===============================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

MODULE:
    Formatting Utilities

PURPOSE:
    Provides reusable formatting functions used throughout the platform.

    This module standardizes the presentation of:

        • Registered voters
        • Polling stations
        • Percentages
        • Large numbers
        • Codes
        • Missing values

AUTHOR:
    Julie Natasha
===============================================================================
"""

from __future__ import annotations


# =============================================================================
# LARGE NUMBER FORMATTERS
# =============================================================================

def format_number(value: int | float) -> str:
    """
    Format a number using thousands separators.

    Example
    -------
    22120458 -> 22,120,458
    """

    return f"{value:,.0f}"


def format_compact(value: int | float) -> str:
    """
    Convert large numbers into K/M/B format.

    Examples
    --------
    1540 -> 1.5K

    2540000 -> 2.5M

    1800000000 -> 1.8B
    """

    value = float(value)

    if value >= 1_000_000_000:
        return f"{value/1_000_000_000:.1f}B"

    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"

    if value >= 1_000:
        return f"{value/1_000:.1f}K"

    return f"{value:.0f}"


# =============================================================================
# PERCENTAGES
# =============================================================================

def format_percentage(value: float) -> str:
    """
    Format decimal values as percentages.

    Example
    -------
    0.8734 -> 87.34%
    """

    return f"{value:.2%}"


# =============================================================================
# VOTERS
# =============================================================================

def format_voters(value: int | float) -> str:
    """
    Format registered voter counts.
    """

    return format_number(value)


# =============================================================================
# POLLING STATIONS
# =============================================================================

def format_polling_stations(value: int | float) -> str:
    """
    Format polling station counts.
    """

    return format_number(value)


# =============================================================================
# CODES
# =============================================================================

def format_code(value) -> str:
    """
    Ensure electoral codes are treated as strings.

    Leading zeros are preserved.
    """

    return str(value).strip()


# =============================================================================
# MISSING VALUES
# =============================================================================

def safe_value(value, default: str = "N/A"):
    """
    Replace missing values with a default.

    Examples
    --------
    NaN -> N/A

    None -> N/A
    """

    if value is None:
        return default

    text = str(value).strip()

    if text == "" or text.lower() == "nan":
        return default

    return value