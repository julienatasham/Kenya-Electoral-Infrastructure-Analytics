"""
===============================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

MODULE:
    Theme Loader

PURPOSE:
    Loads the application's global CSS stylesheet.

AUTHOR:
    Julie Natasha
===============================================================================
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

# =============================================================================
# PROJECT PATHS
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSS_FILE = PROJECT_ROOT / "assets" / "style.css"

# =============================================================================
# LOAD GLOBAL STYLESHEET
# =============================================================================

def load_theme() -> None:
    """
    Load the global stylesheet.

    The function silently exits if the stylesheet
    cannot be found.
    """

    if not CSS_FILE.exists():
        return

    with open(CSS_FILE, encoding="utf-8") as css:

        st.markdown(

            f"<style>{css.read()}</style>",

            unsafe_allow_html=True,

        )