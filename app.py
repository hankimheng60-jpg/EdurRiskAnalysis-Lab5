import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="EduRisk Analytics - Lab 05",
    page_icon="🎓",
    layout="centered"
)

st.session_state.setdefault("risk_history", [])

# Step 8: Keep CSV Loading from Lab 03
def load_student_data():
    try:
        data = pd.read_csv(
            Path(__file__).with_name("students.csv"),
            header=None,
            names=[
                "Student Name",
                "Course",
                "Score",
                "Attendance",
                "Study Hours",
            ],
        )
        return data
    except FileNotFoundError:
        st.error(
            "students.csv was not found. Please place it in the same folder as app.py."
        )
        st.stop()


# Step 10: Keep the Risk Level Function
def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"
    
# Step 9: Keep Loading the Student Data
student_df = load_student_data()
total_students = len(student_df)
average_score = student_df["Score"].mean()
average_attendance = student_df["Attendance"].mean()
low_score_students = student_df[student_df["Score"] < 60].shape[0]

# Step 11: Keep the Risk Level Column
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(
        row["Score"],
        row["Attendance"]
    ),
    axis=1
)
# Step 13: Keep Sidebar Navigation
with st.sidebar:
    st.title("EduRisk Menu")
    selected_page = st.radio(
        "Select Page",
        ["Home", "Dashboard", "Student Data", "Risk Checker", "About"]
    )
# Home Page
if selected_page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Interactive Dashboard with Visualization and Filters")
    st.write(
        "Welcome to Lab 05."
    )
    st.write(
        "In this lab, the app improves the Dashboard page using "
        "grouped summaries, interactive filters, Streamlit charts, and Plotly charts."
    )
    st.success("Lab 05 app is running successfully!")

    with st.container(horizontal=True):
        st.metric("Students", total_students, icon=":material/group:", border=True)
        st.metric("Average score", f"{average_score:.1f}", icon=":material/grade:", border=True)
        st.metric(
            "Average attendance",
            f"{average_attendance:.1f}%",
            icon=":material/event_available:",
            border=True,
        )
        st.metric(
            "Students scoring below 60",
            low_score_students,
            icon=":material/warning:",
            border=True,
        )

    st.info("Choose a page from the menu to explore the dashboard, student data, or risk checker.")

# =========================================================
# Dashboard Page
# Step 13 : create interactive filters for the dashboard page
elif selected_page == "Dashboard":
    # Step 18: Add Dashboard Title and Instruction
    st.title("Interactive Student Performance Dashboard")
    st.write(
        "Use filters to explore student performance by course, risk level, "
        "and attendance. The dashboard updates based on your selections."
    )

    st.subheader("Dashboard Filters")
    # Step 19: Add Dashboard Filters Section
    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        course_options = ["All"] + sorted(student_df["Course"].unique())
        selected_course = st.selectbox(
            "Filter by Course",
            course_options
        )
    with filter_col2:
        risk_options = ["All"] + sorted(student_df["Risk Level"].unique())
        selected_risk = st.selectbox(
            "Filter by Risk Level",
            risk_options
        )
    with filter_col3:
        minimum_attendance = st.slider(
            "Minimum Attendance",
            0,
            100,
            0
        )

    filtered_df = student_df.copy()

    if selected_course != "All":
        filtered_df = filtered_df[
            filtered_df["Course"] == selected_course
        ]

    if selected_risk != "All":
        filtered_df = filtered_df[
            filtered_df["Risk Level"] == selected_risk
        ]

    filtered_df = filtered_df[
        filtered_df["Attendance"] >= minimum_attendance
    ]

    if filtered_df.empty:
        st.warning("No students match the selected filters. Please adjust the filters.")

    st.subheader("Filtered Dashboard Metrics")

    filtered_total_students = len(filtered_df)

    if filtered_total_students > 0:
        filtered_average_score = filtered_df["Score"].mean()
        filtered_average_attendance = filtered_df["Attendance"].mean()
        filtered_high_risk_students = filtered_df[
            filtered_df["Risk Level"] == "High Risk"
        ].shape[0]
    else:
        filtered_average_score = 0
        filtered_average_attendance = 0
        filtered_high_risk_students = 0

    # Step 26: Display Filtered Metric Cards
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric("Students", filtered_total_students)

    with metric_col2:
        st.metric("Average Score", round(filtered_average_score, 2))

    with metric_col3:
        st.metric(
            "Average Attendance",
            f"{round(filtered_average_attendance, 2)}%"
        )

    with metric_col4:
        st.metric("High Risk", filtered_high_risk_students)

    # Step 27: Add Course Summary Table
    st.subheader("Course Summary")

    if filtered_total_students > 0:
        course_summary = filtered_df.groupby("Course").agg(
            Students=("Student Name", "count"),
            Average_Score=("Score", "mean"),
            Average_Attendance=("Attendance", "mean"),
            Average_Study_Hours=("Study Hours", "mean")
        ).reset_index()

        st.dataframe(course_summary)
    else:
        st.info("No course summary available for the selected filters.")

    # Step 28: Add Risk Level Summary Table
    st.subheader("Risk Level Summary")

    if filtered_total_students > 0:
        risk_summary = filtered_df["Risk Level"].value_counts().reset_index()
        risk_summary.columns = ["Risk Level", "Students"]

        st.dataframe(risk_summary)
    else:
        st.info("No risk summary available for the selected filters.")

    # Step 29: Add Streamlit Charts Section
    st.subheader("Streamlit Charts")
    chart_col1, chart_col2 = st.columns(2)

    # Step 30: Add Student Score Chart
    with chart_col1:
        st.write("Student Scores")

        if filtered_total_students > 0:
            score_chart = filtered_df.set_index("Student Name")["Score"]
            st.bar_chart(score_chart)
        else:
            st.info("No score chart available.")

    with chart_col2:
        # Step 31: Add Course Count Chart
        st.write("Students by Course")

        if filtered_total_students > 0:
            course_count = filtered_df["Course"].value_counts()
            st.bar_chart(course_count)
        else:
            st.info("No course count chart available.")

    # Step 32: Add Plotly Charts Section
    st.subheader("Interactive Plotly Charts")
    plotly_col1, plotly_col2 = st.columns(2)

    if filtered_total_students > 0:
        with plotly_col1:
            average_score_by_course = (
                filtered_df.groupby("Course", as_index=False)["Score"]
                .mean()
            )
            score_by_course_fig = px.bar(
                average_score_by_course,
                x="Course",
                y="Score",
                title="Average Score by Course",
            )
            st.plotly_chart(score_by_course_fig)

        with plotly_col2:
            attendance_score_fig = px.scatter(
                filtered_df,
                x="Attendance",
                y="Score",
                color="Risk Level",
                hover_name="Student Name",
                title="Attendance vs. Score",
            )
            st.plotly_chart(attendance_score_fig)
    else:
        st.info("No Plotly charts available for the selected filters.")
# Step 33: Add Plotly Risk Distribution Chart
    with plotly_col1:
        st.write("Risk Level Distribution")

        if filtered_total_students > 0:
            risk_summary_chart = filtered_df["Risk Level"].value_counts().reset_index()
            risk_summary_chart.columns = ["Risk Level", "Students"]

            fig_risk = px.bar(
                risk_summary_chart,
                x="Risk Level",
                y="Students",
                color="Risk Level",
                title="Risk Level Distribution",
                color_discrete_map={
                    "Low Risk": "#16A34A",
                    "Medium Risk": "#F59E0B",
                    "High Risk": "#DC2626"
                }
            )

            st.plotly_chart(fig_risk, use_container_width=True)
        else:
            st.info("No risk distribution chart available.")
# Step 34: Add Plotly Score by Student Chart
    with plotly_col2:
        st.write("Student Scores by Risk Level")

        if filtered_total_students > 0:
            fig_score = px.bar(
                filtered_df,
                x="Student Name",
                y="Score",
                color="Risk Level",
                title="Student Scores by Risk Level",
                color_discrete_map={
                    "Low Risk": "#16A34A",
                    "Medium Risk": "#F59E0B",
                    "High Risk": "#DC2626"
                }
            )

            st.plotly_chart(fig_score, use_container_width=True)
        else:
            st.info("No score chart available.")
# Step 35: Add Filtered Student Records Table
    st.subheader("Filtered Student Records")

    if filtered_total_students > 0:
        st.dataframe(filtered_df)
    else:
        st.info("No student records to display.")
# Step 36: Add Ethical Visualization Reminder
    st.warning(
        "Ethics Reminder: Visualizations should support students and guide "
        "academic support decisions, not label or punish students."
    )


# End of Dashboard Page

# Step 24: Update the student data page
elif selected_page == "Student Data":
    st.title("Student Data")

    st.write(
        "This page displays and inspects the dataset loaded from students.csv."
    )

    st.subheader("Data Inspection")

    st.write("Rows and columns:", student_df.shape)

    st.write("Column names:")
    st.write(student_df.columns.tolist())

    st.write("First 5 rows:")
    st.dataframe(student_df.head())

    st.subheader("Full Student Dataset")
    st.dataframe(student_df)
# Step 25 : Create the risk checker page 
elif selected_page == "Risk Checker":
    st.title("Single Student Risk Checker", icon=":material/fact_check:")
    st.write(
        "Enter student information to check risk level. "
        "The result is based on score and attendance."
    )
    st.info(
        "This tool is for academic support. Risk results should help students, "
        "not label or punish them."
    )

    form_col, result_col = st.columns(2)

    with form_col:
        with st.form("risk_checker_form", border=True):
            input_name = st.text_input("Student Name")
            input_score = st.number_input("Score", 0, 100, 50)
            input_attendance = st.number_input("Attendance", 0, 100, 50)
            submitted = st.form_submit_button(
                "Check Risk", type="primary", icon=":material/search:"
            )

    with result_col:
        with st.container(border=True):
            if submitted:
                if input_name.strip() == "":
                    st.warning("Please enter the student name.")
                else:
                    risk_result = get_risk_level(input_score, input_attendance)
                    result = {
                        "Student Name": input_name.strip(),
                        "Score": input_score,
                        "Attendance": input_attendance,
                        "Risk Level": risk_result,
                    }
                    st.session_state["risk_history"].append(result)

                    st.write("Student Name:", input_name.strip())
                    st.write("Score:", input_score)
                    st.write("Attendance:", input_attendance)

                    if risk_result == "Low Risk":
                        st.success("Risk Level: Low Risk")
                        st.write("Student appears on track.")
                    elif risk_result == "Medium Risk":
                        st.warning("Risk Level: Medium Risk")
                        st.write("Monitor progress and provide guidance.")
                    else:
                        st.error("Risk Level: High Risk")
                        st.write("Student may need additional support.")
            else:
                st.caption("The result will appear here.")

    st.caption(
        "High risk: score or attendance below 60 · "
        "Medium risk: below 75 · Low risk: 75 and above"
    )

    st.subheader("Recent Risk Checks")
    if len(st.session_state["risk_history"]) > 0:
        history_df = pd.DataFrame(
            st.session_state["risk_history"]
        )
        st.dataframe(history_df)
    else:
        st.info("No risk checks yet.")

    if st.button("Clear History"):
        st.session_state["risk_history"] = []
        st.success("Risk check history cleared.")

    st.warning(
        "Ethics Reminder: Risk results should be used as guidance for support, "
        "not as final judgment about a student."
    )

# Step 26 : Update the about page
elif selected_page == "About":
    st.title("About")

    st.write("This app is part of Lab 04.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Forms, Validation, and Session State")

    st.info(
        "This version improves the Risk Checker page using Streamlit forms, "
        "input validation, and session state."
    )

    st.warning(
        "Ethics Reminder: Student risk information should be used responsibly "
        "to support learning and student success."
    )
