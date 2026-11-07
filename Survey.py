# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os  # Used for file paths and checking whether a file exists.
import csv  # Used to write rows into a CSV file.

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Crystal Preferences Survey 📝")
st.write("Please fill out the form below to share your crystal interests!")

# Find data.csv in the main Lab02 folder (one level above pages).
csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data.csv")
headers = ["Crystal", "Chakra", "Experience", "Rating"]

# Set up the file with column names if it is missing or empty.
if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

# DATA INPUT FORM
# 'st.form' groups the input widgets until the user clicks Submit Data.
with st.form("survey_form"):
    # A text input collects a string, as required by the lab.
    crystal_input = st.text_input("What is your favorite crystal?")
    chakra_input = st.selectbox(
        "Which chakra interests you most?",
        ["Root", "Sacral", "Solar Plexus", "Heart", "Throat", "Third Eye", "Crown"]
    )
    experience_input = st.selectbox(
        "How experienced are you with crystals?",
        ["Beginner", "Intermediate", "Experienced"]
    )
    rating_input = st.slider("How interested are you in crystals?", 1, 5, 3)

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block runs ONLY when the submit button is clicked.
    if submitted:
        if crystal_input.strip() == "":
            st.warning("Please enter a crystal name before submitting.")
        else:
            # Create a new row and append it to data.csv.
            new_row = [crystal_input.strip(), chakra_input, experience_input, rating_input]
            with open(csv_path, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(new_row)

            st.success("Your data has been submitted!")
            st.write(
                f"You entered: **Crystal:** {crystal_input}, "
                f"**Chakra:** {chakra_input}, "
                f"**Experience:** {experience_input}, "
                f"**Rating:** {rating_input}"
            )

# DATA DISPLAY
# Show the current contents of the CSV file to help with debugging.
st.divider()
st.header("Current Data in CSV")

# Check if the CSV file exists and has data rows.
if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
    current_data_df = pd.read_csv(csv_path)
    if current_data_df.empty:
        st.info("No survey responses yet. Submit the form to add one!")
    else:
        st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
