"""
===============================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

MODULE
    Sidebar Navigation

DESCRIPTION
    Provides the application's global navigation sidebar.
    The sidebar is shared across every page to provide
    consistent navigation throughout the platform.

AUTHOR
    Julie Natasha
===============================================================================
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

# =============================================================================
# CONSTANTS
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

LOGO_PATH = PROJECT_ROOT / "assets" / "logo.png"


# =============================================================================
# SIDEBAR
# =============================================================================

def render_sidebar() -> None:
    """
    Render the application sidebar.
    """

    with st.sidebar:

        # ---------------------------------------------------------------------
        # Branding
        # ---------------------------------------------------------------------

        if LOGO_PATH.exists():

            st.image(str(LOGO_PATH), use_container_width=True)

        st.title("KEIAP")

        st.caption(
            "Kenya Electoral Infrastructure Analytics Platform"
        )

        st.divider()

        # ---------------------------------------------------------------------
        # Navigation
        # ---------------------------------------------------------------------

        st.subheader("Navigation")

        st.page_link(
            "app.py",
            label="Home Dashboard",
            icon="🏠",
        )

        st.page_link(
            "pages/1_Polling_Centre_Finder.py",
            label="Polling Centre Finder",
            icon="📍",
        )

        st.page_link(
            "pages/2_Statistics.py",
            label="Statistics",
            icon="📊",
        )

        st.page_link(
            "pages/3_Diaspora.py",
            label="Diaspora Voters",
            icon="🌍",
        )

        st.page_link(
            "pages/4_Prisons.py",
            label="Prison Voters",
            icon="🏛",
        )

        st.page_link(
            "pages/5_AI_Assistant.py",
            label="AI Assistant",
            icon="🤖",
        )

        st.divider()

        # ---------------------------------------------------------------------
        # Platform Information
        # ---------------------------------------------------------------------

        st.subheader("Platform")

        st.caption(
            """
            KEIAP provides interactive analytics,
            electoral infrastructure insights,
            and AI-assisted exploration of
            Kenya's electoral datasets.
            """
        )

        st.divider()

        st.caption("Version 1.0")