"""
===============================================================================
KEIAP Page Header Component
===============================================================================
"""

import streamlit as st


def render_page_header(title, description):

    st.markdown(
        f"""
        <div class="page-header">

            <h1>
                {title}
            </h1>

            <p>
                {description}
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )