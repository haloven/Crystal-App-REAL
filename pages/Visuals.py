# This creates the page for displaying data visualizations.

import streamlit as st
import json
import plotly.express as px  #  allow users to hover over data points, zoom in, and interact with the visualization in graphs
import pandas as pd   # Python library used to organize, manipulate, and analyze data
from pathlib import Path

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈"
)

st.title("🌇 Spiritual Visuals 🌃")

# LOAD JSON FILE
with open("data.json", "r") as file:
    data = json.load(file)


def activities_section(data):

    tab1, tab2 = st.tabs(["Origins🎴", "♡✹Your Progress✹♡"])

    with tab1:

        st.header("Origins🎴")
        st.subheader("Chakras")
        st.write("Explore chakra and crystal associations!")

        # STATIC VISUALIZATION
        st.header("Crystal Associations by Chakra")

        labels = []
        values = []

        for item in data["data_points"]:
            labels.append(item["label"])
            values.append(item["value"])

        chakra_colors = {
            "Root": "#FF0000",
            "Sacral": "#FF8000",
            "Solar Plexus": "#FFD700",
            "Heart": "#00AA00",
            "Throat": "#008BFF",
            "Third Eye": "#4B0082",
            "Crown": "#8A2BE2"
        }

        fig = px.bar(
            x=labels,
            y=values,
            color=labels,
            color_discrete_map=chakra_colors,
            title=data["chart_title"],
            labels={
                "x": "Chakra",
                "y": "Number of Crystal Associations",
                "color": "Chakra"
            }
        )

        fig.update_layout(
            dragmode=False,
            xaxis=dict(fixedrange=True),
            yaxis=dict(fixedrange=True)
        )

        st.plotly_chart(
            fig,
            config={
                "scrollZoom": False,
                "displayModeBar": False
            }
        )

        st.caption(
            "Counts represent associations within a selected "
            "collection of 17 crystals."
        )

        # CRYSTAL INFORMATION
        st.subheader("Explore the Crystals")
        st.write("Click on a crystal to learn more!")

        crystals = data["crystals"]

        for name, details in crystals.items():

            with st.expander(name):
                st.write("Color:", details["color"])
                st.write(
                    "Associated Chakras:",
                    ", ".join(details["chakras"])
                )
                st.write("Crystal Group:", details["group"])
                st.write(
                    "Traditional Properties:",
                    ", ".join(details["properties"])
                )

        # DYNAMIC VISUALIZATION
        st.header("Explore Crystal Groups")

        crystal_groups = data["crystal_groups"]
        group_names = list(crystal_groups.keys())

        # SESSION STATE
        if "selected_group" not in st.session_state:
            st.session_state.selected_group = group_names[0]

        # USER INPUT
        selected = st.selectbox(
            "Select a crystal group:",
            group_names,
            key="selected_group"
        )

        #DATA FOR SELECTED GROUP
        selected_data = crystal_groups[selected]

      
        chart_df = pd.DataFrame({
            "Chakra": list(selected_data.keys()),
            "Crystal Associations": list(selected_data.values())
        })

        # DYNAMIC LINE CHART
        st.line_chart(
            chart_df,
            x="Chakra",
            y="Crystal Associations"
        )

        st.write("Currently displaying:", selected)

        # LIST CRYSTALS IN SELECTED GROUP
        st.subheader("Crystals in This Group")

        for name, details in crystals.items():

            if details["group"] == selected:
                st.write("-", name)

# PART 2: GRAPHS FROM data.csv

    with tab2:

        st.header("♡✹Crystal Community Insights✹♡")
        st.write("Explore responses from our crystal survey!")

        csv_file = Path(__file__).resolve().parent.parent / "data.csv"

        # Check that the CSV file exists
        if not csv_file.exists() or csv_file.stat().st_size == 0:
            st.info("No survey data available yet.")

        else:

            # READ CSV DATA
            survey_data = pd.read_csv(csv_file)

            if survey_data.empty:
                st.info("Complete the survey to see the charts!")

            else:

                # STATIC VISUALIZATION
                st.subheader("Most Popular Chakras")

                chakra_counts = (
                    survey_data["Chakra"]
                    .value_counts()
                    .reset_index()
                )

                chakra_counts.columns = ["Chakra", "Responses"]

                pie_fig = px.pie(
                    chakra_counts,
                    names="Chakra",
                    values="Responses",
                    title="Favorite Chakras Among Survey Participants"
                )

                st.plotly_chart(
                    pie_fig,
                    use_container_width=True
                )

                # DYNAMIC VISUALIZATION
                st.subheader("Crystal Interest by Experience")

                # Initialize session state
                if "experience_filter" not in st.session_state:
                    st.session_state.experience_filter = "All"

                experience_options = [
                    "All", "Beginner", "Intermediate", "Experienced"
                ]

                # User interaction
                selected_experience = st.selectbox(
                    "Filter by experience level:",
                    experience_options,
                    key="experience_filter"
                )

                # Filter data according to user selection
                if selected_experience == "All":
                    filtered_data = survey_data
                else:
                    filtered_data = survey_data[
                        survey_data["Experience"] == selected_experience
                    ]

                # Create chart from selected data
                if filtered_data.empty:
                    st.info("No responses for this experience level.")

                else:
                    average_ratings = (
                        filtered_data.groupby("Chakra")["Rating"]
                        .mean()
                        .reset_index()
                    )

                    st.bar_chart(
                        average_ratings,
                        x="Chakra",
                        y="Rating",
                        x_label="Chakra",
                        y_label="Average Interest Rating"
                    )

                    st.write(
                        "Currently displaying:",
                        selected_experience
                    )

                    # EXTRA CREDIT: MEAN AND MEDIAN
                    mean_rating = filtered_data["Rating"].mean()
                    median_rating = filtered_data["Rating"].median()

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Mean Interest Rating",
                            round(mean_rating, 2)
                        )

                    with col2:
                        st.metric(
                            "Median Interest Rating",
                            round(median_rating, 2)
                        )

activities_section(data)

