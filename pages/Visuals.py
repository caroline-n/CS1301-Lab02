# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.
import csv

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Your finances from January to September")

# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.

#loading data from csv file
try:
    csvdf = pd.read_csv('data.csv')
    st.dataframe(csvdf)    
except pd.errors.EmptyDataError:
    st.warning("The 'data.csv' file is empty or has no valid data to process.")
except Exception:
    st.warning("Sorry, there was a problem reading the 'data.csv' file.")
#loading data from json file
try:
    with open("data.json", "r") as infile:
        myData = json.load(infile) #converting json data into a python dictionary or a list
    jsondf = pd.DataFrame(myData["data_points"])
    st.header(myData["chart_title"])
    st.dataframe(jsondf)
except:
    st.warning("Sorry, there was a problem reading the json file.")

# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.

st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH
try:
    st.subheader(myData["chart_title"]) # CHANGE THIS TO THE TITLE OF YOUR GRAPH
    # TO DO:
    # - Create a static graph (e.g., bar chart, line chart) using st.bar_chart() or st.line_chart().
    # - Use data from either the CSV or JSON file.
    # - Write a description explaining what the graph shows.
    st.area_chart(jsondf, x="Income (thousand USD)", y="Well-being")
    st.write("This is a **static area chart**. Can money buy happiness? This graph shows the harsh reality: happiness increases with reported income. In other words, research found that higher incomes are associated with higher daily happiness and overal life satisfaction.")
    st.info("Data's source: Proceedings of the National Academy of Sciences")
except:
    pass


# GRAPH 2: DYNAMIC GRAPH
try:
    st.divider()
    st.subheader("Saving Amount by Month") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
    # TODO:
    # - Create a dynamic graph that changes based on user input.
    # - Use at least one interactive widget (e.g., st.slider, st.selectbox, st.multiselect).
    # - Use Streamlit's Session State (st.session_state) to manage the interaction.
    # - Add a '#NEW' comment next to at least 3 new Streamlit functions you use in this lab.
    # - Write a description explaining the graph and how to interact with it.
    monthCol = csvdf.columns[0]
    amtCol = csvdf.columns[1]
    
    if "selected" not in st.session_state:
        st.session_state["selected"] = list(csvdf[monthCol])
    if "min" not in st.session_state:
        st.session_state["min"] = int(csvdf[amtCol].min())
        
    #user filters months (multiselect)
    selected = st.multiselect( #NEW
        "Which month(s) do you want to graph?",
        options=list(csvdf[monthCol]),
        default=list(csvdf[monthCol])
    )
    st.session_state["selected"] = selected

    #user chooses minimum amount to display (slider)
    st.write("Choose a minimum amount to display:")
    if st.button("Set to max"):
        st.session_state["min"] = int(csvdf[amtCol].max())
    if st.button("Set to min"):
        st.session_state["min"] = int(csvdf[amtCol].min())
    stepping = st.number_input("Choose a step for the slider below:", min_value=1, value=50)
    st.slider( #NEW
        "",
        int(csvdf[amtCol].min()),
        int(csvdf[amtCol].max()),
        int(csvdf[amtCol].min()),
        step=stepping,
        key="min"
    )

    filtered = csvdf[
        (csvdf[monthCol].isin(st.session_state["selected"])) &
        (csvdf[amtCol] >= st.session_state["min"])
    ]
    order = ["January", "February", "March", "April", "May", "June",
             "July", "August", "September"]
    filtered[monthCol] = pd.Categorical(filtered[monthCol],
                                     categories=order, ordered=True)
    filtered = filtered.sort_values(monthCol)
    st.line_chart(filtered, x=monthCol, y=amtCol)
    #months are displayed in the right order
    st.write("This graph is a **dynamic line chart**. It shows your saving amount by month and allows you to change the graph in real time. Check out the info box for more instructions.")
    st.info("You can use the multiselect box to add months you would like to display or drop months you would like to hide. The 'Set to max' button will help you quickly choose the greatest amount, and the 'Set to min' the smallest amount. You can also drag the slider to specify the minimum amount you would like to show on the graph.")
except:
    pass
    
# GRAPH 3: DYNAMIC GRAPH
try:
    st.divider()
    st.subheader("Histogram for Amounts") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
    # TO DO:
    # - Create another dynamic graph.
    # - If you used CSV data for Graph 1 & 2, you MUST use JSON data here (or vice-versa).
    # - This graph must also be interactive and use Session State.
    # - Remember to add a description and use '#NEW' comments.

    #user chooses if they want to graph postive, negative, or all balances (radio)
    if "balances" not in st.session_state:
        st.session_state["balances"] = "All"

    st.write("Choose which type of balance you would like to graph:")
    incr = st.button("Next option") #NEW
    if incr:
        if st.session_state["balances"] == "All":
            st.session_state["balances"] =  "Positive & Zero"
        elif st.session_state["balances"] == "Positive & Zero":
            st.session_state["balances"] = "Negative"
        else:
            st.session_state["balances"] = "All"

    st.radio( #NEW
    "",
    ["All", "Positive & Zero", "Negative"],
    index=["All", "Positive & Zero", "Negative"].index(st.session_state["balances"]),
    key="balances"
)
    
    if st.session_state["balances"] == "Positive & Zero":
        bar = csvdf[csvdf[amtCol] >= 0]
    elif st.session_state["balances"] == "Negative":
        bar = csvdf[csvdf[amtCol] < 0]
    else:
        bar = csvdf

    
    #graphing counts
    bar = bar.value_counts().reset_index()
    bar.columns = ['index', amtCol, 'Count']
    

    st.bar_chart(bar, x=amtCol, y='Count')

    st.write("This is a **dynamic bar chart**. It graphs how many time a saving amount appears in your data. Check out the info box for more instructions.")
    st.info('To interact with this graph, you can choose which type of balance you would like to see. The next button is there so you can quickly go through the options. By default, the graph will show all balances. By choosing "Positive & Zero", you will graph only amounts that are greater or equal to zero. Otherwise, if you choose "Negative", you will graph only amounts that are less than zero.')
except:
    pass
