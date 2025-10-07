# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).
import csv

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")
# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.text_input("How do you want to name your month column?", placeholder="Month")
    value_input = st.text_input("How do you want to name your amount column?", placeholder="Amount")
    months = ["January", "February", "March", "April", "May", "June" , "July", "August", "September"]

    sav1 = st.number_input("Enter your saving amount for January ($):",
                                   value=0, step=50)
    sav2 = st.number_input("Enter your saving amount for February:",
                                   value=0, step=50)
    sav3 = st.number_input("Enter your saving amount for March:",
                                   value=0, step=50)
    sav4 = st.number_input("Enter your saving amount for April:",
                                   value=0, step=50)
    sav5 = st.number_input("Enter your saving amount for May:",
                                   value=0, step=50)
    sav6 = st.number_input("Enter your saving amount for June:",
                                   value=0, step=50)
    sav7 = st.number_input("Enter your saving amount for July:",
                                   value=0, step=50)
    sav8 = st.number_input("Enter your saving amount for August:",
                                   value=0, step=50)
    sav9 = st.number_input("Enter your saving amount for September:",
                                   value=0, step=50)
    savings = [sav1, sav2, sav3, sav4, sav5, sav6, sav7, sav8, sav9]
    #if cleared:
    cleared = st.form_submit_button("Clear Data")
    if cleared:
        open('data.csv', 'w').close()
        st.success("CSV file cleared!")
    
    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data", type='primary')

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        if not category_input and not value_input:
            category_input = "Month"
            value_input = "Amount"
        elif not category_input:
            category_input = "Month"
        elif not value_input:
            value_input = "Amount"

        with open('data.csv', 'a', newline='') as datafile: #open in append mode
            writer = csv.writer(datafile)
            writer.writerow([category_input, value_input])
            for month, saving in zip(months, savings):
                writer.writerow([month, saving])
            
        # --- YOUR LOGIC GOES HERE --- (DONE)
        # TO DO:
        # 1. Create a new row of data from 'category_input' and 'value_input'.
        # 2. Append this new row to the 'data.csv' file.
        #    - You can use pandas or Python's built-in 'csv' module.
        #    - Make sure to open the file in 'append' mode ('a').
        #    - Don't forget to add a newline character '\n' at the end.
        
        st.success("Your data has been submitted! Go to the visualisation page to see graphs.")

# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    try:
        #read the CSV file
        current_data_df = pd.read_csv('data.csv')
        #show the DataFrame as a table on screen
        st.dataframe(current_data_df)
    except:
        pass
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
