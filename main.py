import streamlit as st
import time
from quiz_data import quiz_data  # Import quiz data

# Initialize session state
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
    st.session_state.quiz_started = False
    st.session_state.difficulty = None
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.quiz_completed = False
    st.session_state.start_time = None  # ✅ Track quiz start time once
    st.session_state.end_time = None  # ✅ Track quiz end time
    st.session_state.user_answers = []
    st.session_state.filtered_quiz_data = []

st.title("🎓 Python Quiz App")
st.markdown("---")

# User Name Input
if not st.session_state.user_name:
    user_input = st.text_input("Enter your name to start:", key="user_name_input")
    if st.button("Start Quiz"):
        if user_input.strip():
            st.session_state.user_name = user_input.strip()
            st.rerun()
else:
    st.write(f"👋 Welcome, **{st.session_state.user_name}**!")

    # Difficulty Selection
    if not st.session_state.quiz_started:
        st.markdown("## Select Difficulty")
        col1, col2, col3 = st.columns(3)
        if col1.button("Easy"):
            st.session_state.difficulty = "Easy"
        if col2.button("Medium"):
            st.session_state.difficulty = "Medium"
        if col3.button("Hard"):
            st.session_state.difficulty = "Hard"

        if st.session_state.difficulty:
            st.session_state.quiz_started = True
            st.session_state.start_time = time.time()  # ✅ Start time is set only once

            # ✅ Filter quiz data based on difficulty
            filtered_questions = [
                q for q in quiz_data if q["difficulty"] == st.session_state.difficulty
            ]

            if not filtered_questions:
                st.error(
                    "No questions available for this difficulty. Please check quiz_data.py!"
                )
                st.stop()

            st.session_state.filtered_quiz_data = filtered_questions
            st.session_state.user_answers = [None] * len(filtered_questions)
            st.rerun()

    # Quiz Logic
    if st.session_state.quiz_started and not st.session_state.quiz_completed:
        if st.session_state.current_question < len(st.session_state.filtered_quiz_data):
            question = st.session_state.filtered_quiz_data[
                st.session_state.current_question
            ]

            # Progress Bar
            progress_value = (st.session_state.current_question + 1) / len(
                st.session_state.filtered_quiz_data
            )
            st.progress(progress_value)

            st.write(
                f"**Question {st.session_state.current_question + 1}/{len(st.session_state.filtered_quiz_data)}**"
            )
            st.subheader(question["question"])

            # Display choices
            selected_choice = st.radio(
                "Select your answer:",
                question["choices"],
                key=f"question_{st.session_state.current_question}",
                index=None,
            )

            # ✅ Show total time elapsed since quiz start
            time_elapsed = (
                int(time.time() - st.session_state.start_time)
                if st.session_state.start_time
                else 0
            )
            st.write(f"⏱️ Time Elapsed: {time_elapsed} seconds")

            # ✅ Automatically move to the next question when an answer is selected
            if selected_choice:
                st.session_state.user_answers[st.session_state.current_question] = (
                    selected_choice
                )
                if selected_choice == question["answer"]:
                    st.session_state.score += 1
                    st.success("✅ Correct Answer!")
                else:
                    st.error(
                        f"❌ Incorrect Answer! The correct answer was: **{question['answer']}**"
                    )

                # ✅ Pause briefly, then move to the next question
                time.sleep(1)
                st.session_state.current_question += 1

                if st.session_state.current_question >= len(
                    st.session_state.filtered_quiz_data
                ):
                    st.session_state.quiz_completed = True
                    st.session_state.end_time = (
                        time.time()
                    )  # ✅ Set end time when quiz is completed

                st.rerun()

    # Final Score and Summary
    if st.session_state.quiz_completed:
        total_time_taken = (
            int(st.session_state.end_time - st.session_state.start_time)
            if st.session_state.start_time and st.session_state.end_time
            else 0
        )

        st.markdown("---")
        st.write(f"🎉 **Quiz Completed, {st.session_state.user_name}!**")
        st.write(
            f"⏱️ **Total Time Taken:** {total_time_taken} seconds"
        )  # ✅ Fixed time issue
        st.write(
            f"📊 **Final Score:** {st.session_state.score}/{len(st.session_state.filtered_quiz_data)}"
        )

        st.markdown("### 📝 Quiz Summary")
        for i, q in enumerate(st.session_state.filtered_quiz_data):
            st.write(f"**Question {i + 1}:** {q['question']}")
            st.write(f"**Your Answer:** {st.session_state.user_answers[i]}")
            st.write(f"**Correct Answer:** {q['answer']}")
            st.markdown("---")

        st.markdown("## 🏆 Leaderboard")
        st.write(
            f"🥇 {st.session_state.user_name} - {st.session_state.score}/{len(st.session_state.filtered_quiz_data)}"
        )

st.markdown(
    """
    <style>
    /* Background - Neon Glow Effect */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top, #0f0f0f, #000000 80%);
        color: white;
    }
    
    /* Header - Glassmorphism */
    [data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    /* Sidebar - Dark Glass with Neon */
    [data-testid="stSidebar"] {
        background: rgba(20, 20, 20, 0.9);
        backdrop-filter: blur(15px);
        border-right: 2px solid rgba(0, 255, 255, 0.3);
    }
    
    /* Quiz Questions - Neon Green */
    .stSubheader {
        color: #00ff99;
        font-weight: bold;
        text-shadow: 0px 0px 10px #00ff99;
    }

    /* Neon Button Effect */
    .stButton>button {
        background: linear-gradient(45deg, #ff00ff, #ff0099);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 18px;
        transition: 0.3s ease-in-out;
        box-shadow: 0px 0px 8px #ff00ff;
    }

    .stButton>button:hover {
        background: linear-gradient(45deg, #ff0099, #ff00ff);
        transform: scale(1.08);
        box-shadow: 0px 0px 12px #ff00ff;
        color: white;
    }

    /* Input Fields - Dark Neon */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border-radius: 10px;
        border: 1px solid rgba(0, 255, 255, 0.4);
        padding: 10px;
    }

    /* Progress Bar - Neon Green */
    .stProgress > div > div > div > div {
        background: linear-gradient(45deg, #00ff99, #00cc66);
        box-shadow: 0px 0px 6px #00ff99;
    }

    /* Quiz Summary - Cyan Glow */
    .stMarkdown h2 {
        color: #00ffff;
        text-shadow: 0px 0px 8px #00ffff;
    }

    /* Correct Answer - Neon Green */
    .correct-answer {
        color: #00ff00;
        font-weight: bold;
        text-shadow: 0px 0px 5px #00ff00;
    }

    /* Wrong Answer - Neon Red */
    .wrong-answer {
        color: #ff3333;
        font-weight: bold;
        text-shadow: 0px 0px 5px #ff3333;
    }

    </style>
    """,
    unsafe_allow_html=True,
)
