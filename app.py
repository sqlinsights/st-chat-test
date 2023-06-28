import streamlit as st
import altair as alt
import pandas as pd
import numpy as np


@st.cache_data(
    show_spinner=False,
)
def generate_data() -> dict:
    regions = ["LATAM", "EMEA", "APAC", "NA"]
    months = [
        "JAN",
        "FEB",
        "MAR",
        "APR",
        "MAY",
        "JUN",
        "JUL",
        "AUG",
        "SEPT",
        "OCT",
        "NOV",
        "DEC",
    ]

    main_dict = {}
    for r in regions:
        main_dict[r] = {i: np.random.randint(low=1, high=100) for i in months}
    return (
        pd.DataFrame(main_dict)
        .transpose()
        .reset_index()
        .rename(columns={"index": "REGION"})
        .melt(
            id_vars=["REGION"],
            value_vars=[
                "JAN",
                "FEB",
                "MAR",
                "APR",
                "MAY",
                "JUN",
                "JUL",
                "AUG",
                "SEPT",
                "OCT",
                "NOV",
                "DEC",
            ],
        )
        .rename(columns={"variable": "MONTH", "value": "BOOKINGS"})
    )


with st.spinner("Generating Data"):
    df = generate_data()

st.title("Chat my Stats")

if "prompts" not in st.session_state:
    st.session_state["prompts"] = {}


def update_prompts(key: str) -> None:
    if key in st.session_state:
        st.session_state["prompts"][key] = st.session_state[key]


columns_list = [""]
columns_list.extend(df.columns)
with st.chat_message("Data Bot", avatar="⚙️"):
    st.write("Found some data for you, do you want to take a look?")


first_prompt = st.chat_input(
    "Yes or No", on_submit=update_prompts, args=["first_prompt"], key="first_prompt"
)
if st.session_state["prompts"].get("first_prompt"):
    if str(st.session_state["prompts"].get("first_prompt")).upper() == "YES":
        with st.chat_message("Me", avatar="👨🏼‍💻"):
            st.write(str(st.session_state["prompts"].get("first_prompt")))
        with st.chat_message("Data Bot", avatar="⚙️"):
            st.write("Great!")
            st.dataframe(df.head(20), hide_index=True)
    second_prompt = st.chat_input(
        "Would you like to visualize it?",
        on_submit=update_prompts,
        args=["second_prompt"],
        key="second_prompt",
    )
    if st.session_state["prompts"].get("second_prompt"):
        if str(st.session_state["prompts"].get("second_prompt")).upper() == "YES":
            with st.chat_message("Me", avatar="👨🏼‍💻"):
                st.write(str(st.session_state["prompts"].get("second_prompt")))
            with st.chat_message("Data Bot", avatar="⚙️"):
                visual_type = st.selectbox(
                    "What visual would you like?",
                    options=["", "BarChart", "LineChart"],
                    on_change=update_prompts,
                    args=["visual_type"],
                    key="visual_type",
                )
            if st.session_state["prompts"].get("visual_type"):
                if st.session_state["prompts"].get("visual_type") != "":
                    with st.chat_message("Data Bot", avatar="⚙️"):
                        st.write(
                            f'Perfect, {st.session_state["prompts"].get("visual_type")} it is!'
                        )
                with st.chat_message("Data Bot", avatar="⚙️"):
                    st.selectbox(
                        "What field you would like to use for X?",
                        options=columns_list,
                        key="x_field",
                        on_change=update_prompts,
                        args=["x_field"],
                        index=0,
                    )
                if st.session_state["prompts"].get("x_field"):
                    with st.chat_message("Data Bot", avatar="⚙️"):
                        st.selectbox(
                            "What field you would like to use for Y?",
                            options=[
                                i
                                for i in columns_list
                                if i != st.session_state["prompts"]["x_field"]
                            ],
                            key="y_field",
                            on_change=update_prompts,
                            args=["y_field"],
                            index=0,
                        )
                    if st.session_state["prompts"].get("y_field"):
                        with st.chat_message("Data Bot", avatar="⚙️"):
                            st.selectbox(
                                "What field you would like to use for Color?",
                                options=[
                                    i
                                    for i in columns_list
                                    if i
                                    not in [
                                        st.session_state["prompts"]["x_field"],
                                        st.session_state["prompts"]["y_field"],
                                    ]
                                ],
                                key="color_field",
                                on_change=update_prompts,
                                args=["color_field"],
                                index=0,
                            )
                        if st.session_state["prompts"].get("color_field"):
                            with st.chat_message("Data Bot", avatar="⚙️"):
                                if (
                                    st.session_state["prompts"].get("visual_type")
                                    == "LineChart"
                                ):
                                    base_chart = (
                                        alt.Chart(df)
                                        .mark_line()
                                        .encode(
                                            x=f'{st.session_state["prompts"]["x_field"]}:N',
                                            y=f'{st.session_state["prompts"]["y_field"]}:Q',
                                            color=f'{st.session_state["prompts"]["color_field"]}:N',
                                        )
                                    )
                                if (
                                    st.session_state["prompts"].get("visual_type")
                                    == "BarChart"
                                ):
                                    base_chart = (
                                        alt.Chart(df)
                                        .mark_bar()
                                        .encode(
                                            x=f'{st.session_state["prompts"]["x_field"]}:N',
                                            y=f'{st.session_state["prompts"]["y_field"]}:Q',
                                            color=f'{st.session_state["prompts"]["color_field"]}:N',
                                        )
                                    )

                                st.altair_chart(base_chart, use_container_width=True)

    if str(st.session_state["prompts"].get("first_prompt")).upper() == "NO":
        with st.chat_message("Me", avatar="👨🏼‍💻"):
            st.write(str(st.session_state["prompts"].get("first_prompt")))
        with st.chat_message("Data Bot", avatar="⚙️"):
            st.write("Ok Then!")
