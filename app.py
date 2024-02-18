import streamlit as st
import re
from data import questions_list
from pymongo import MongoClient
import time

client = MongoClient("mongodb+srv://hritesh532004:9Gx3KKxDjwogHUZk@cluster0.e4l3u0u.mongodb.net/Anweshan?retryWrites=true&w=majority")
db = client["Anweshan"]
collection = db["Quiz"]

def quiz_app():
    st.markdown("<h1 style='text-align: center;'>IEEE Induction Quiz</h1>", unsafe_allow_html=True)
    st.markdown("---")

    questions = questions_list

    score = 0

    for i, q in enumerate(questions):
        st.subheader(f"Question {i + 1}: {q['question']}")
        user_answer = st.radio("Select an answer:", q["options"], index=None, key=f"{i}")
        st.markdown("---")
        if user_answer == q["correct_answer"]:
            score += 1
    return score

def home():
    st.markdown("<h1 style='text-align: center;'>Fill Up Your Details</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.write("")
    st.write("")
    name = st.text_input("Enter Your Full Name", placeholder="Full Name")
    st.write("")
    roll = st.text_input("Enter Your Registration Number", placeholder="1234567890")
    st.write("")
    email = st.text_input("Enter Your Email", placeholder="example@email.com")
    st.write("")
    branch = st.radio("Select Your Branch", ["Computer Science and Engineering", "Chemical Engineering", "Civil Engineering", "Electrical Engineering", "Electrical and Electronics Engineering", "Electronics and Telecommunication Engineering", "Information Technology", "Mechanical Engineering", "Metallurgical and Materials Engineering", "Production Engineering"],index=None)
    st.write("")
    return name, roll, email, branch

def check_records(roll):
    check_roll = collection.find_one({"Roll_No": roll})
    if check_roll:
        return 1

if 'final_points' not in st.session_state:
    st.session_state.final_points = 0


if __name__ == "__main__":
    if 'page' not in st.session_state:
        st.session_state.page = 1

    if st.session_state.page == 1:
        submitted = ""
        name, roll, email, branch = home()
        st.session_state.name = name
        st.session_state.roll = roll
        st.session_state.email = email
        st.session_state.branch = branch

        ispresent = check_records(roll)
        if ispresent:
            st.info("Record Already Exists.")
        else:
            submitted = st.button("Next")
        
        if submitted:
            if not name :
                st.info("Please enter your name.")
            elif name.isspace():
                if not name.isalpha():
                    st.error("Name should not contain any characters.")
            elif not roll:
                st.info("Please enter your registration number.")
            elif not roll.isdigit():
                st.error("Registration Number should not contain any other characters.")
            elif not (len(roll)>=10 and len(roll)<13):
                st.error("Enter a valid registration number.")
            elif not email:
                st.info("Please enter your e-mail.")
            elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',email):
                st.error("E-mail address is not valid.")
            elif not branch:
                st.info("Please select your branch.")
            else:
                st.session_state.page = 2


    elif st.session_state.page == 2:
        # st.set_page_config(layout="wide")
        # left_column, right_column = st.columns(2)

        # with left_column:
        st.session_state.final_points = quiz_app()
        st.write("")
        if st.button("Previous"):
            st.session_state.page = 1
        elif st.button("Submit"):
            st.write()
            st.session_state.page = 3


        # with right_column:
        #     st.markdown("""
        #         <style>
        #             .center {
        #                 display: flex;
        #                 flex-direction: column;
        #                 justify-content: center;
        #                 align-items: center;
        #                 height: 80vh; /* 100% of the viewport height */
        #             }
        #         </style>
        #     """, unsafe_allow_html=True)
        #     timer_duration = 10
        #     timer_placeholder = st.empty()
        #     # timer_placeholder.write("Timer: ")
        #     for i in range(timer_duration, 0, -1):
        #         time_text = f'<div class="center"><h1 id="timer_display">Time left: {i} seconds</h1></div>'
        #         timer_placeholder.markdown(time_text,unsafe_allow_html=True)
        #         time.sleep(1)
                
    
    elif st.session_state.page == 3:
        st.set_page_config(layout="wide")
        name = st.session_state.name
        roll = st.session_state.roll
        email = st.session_state.email
        branch = st.session_state.branch
        score = st.session_state.final_points

        user_data = {
            "Roll_No": roll,
            "Name": name,
            "Email": email,
            "Branch": branch,
            "Score": score
        }
        if collection.insert_one(user_data):
            db_text = "Quiz Submitted Successfully!"
        else:
            db_text = "Something Went Wrong!"
        st.balloons()
        st.markdown("""
            <style>
                .centered {
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    height: 70vh; /* 100% of the viewport height */
                }
            </style>
        """, unsafe_allow_html=True)
        html_text = f"""<div class='centered'>
                            <div>
                                <h1>Congratulations!!👏</h1>
                                <h2>{db_text}</h2>
                                <h2 class='centered-text'><b>You scored {score} out of {len(questions_list)}</b></h2>
                            </div>
                        </div>"""
        st.markdown(html_text, unsafe_allow_html=True)
