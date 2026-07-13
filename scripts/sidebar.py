"""
===============================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

MODULE:
    Sidebar

PURPOSE:
    Renders the application's navigation sidebar.

AUTHOR:
    Julie Natasha
===============================================================================
"""

from __future__ import annotations

import streamlit as st

# =============================================================================
# PAGE DEFINITIONS
# =============================================================================

PAGES = [

    ("Home Dashboard", "app.py"),

    ("Polling Centre Finder", "pages/1_Polling_Centre_Finder.py"),

    ("Statistics", "pages/2_Statistics.py"),

    ("Diaspora Voters", "pages/3_Diaspora.py"),

    ("Prison Voters", "pages/4_Prisons.py"),

    ("AI Assistant", "pages/5_AI_Assistant.py"),

]

# =============================================================================
# SIDEBAR
# =============================================================================


def render_sidebar() -> None:
    """
    Render the application sidebar.
    """

    with st.sidebar:

        st.title("KEIAP")

        st.caption(
            "Kenya Electoral Infrastructure Analytics Platform"
        )

        st.divider()

        st.subheader("Navigation")

        for label, page in PAGES:

            st.page_link(
                page,
                label=label,
                use_container_width=True,
            )

        st.divider()

        st.subheader("Project")

        st.write("Version")
        st.caption("1.0.0")

        st.write("Datasets")

        st.caption(
            """
            • Polling Stations

            • Constituencies

            • Diaspora

            • Prison Voters
            """
        )

        st.divider()

        st.caption(
            "Developed using Streamlit and Plotly."
        )