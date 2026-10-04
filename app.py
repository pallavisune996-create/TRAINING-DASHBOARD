import os
import base64
import pandas as pd
import streamlit as st
from datetime import date, time

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Training Portal",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 2. BACKGROUND IMAGE
# ============================================================

if os.path.exists("background.jpg"):
    with open("background.jpg", "rb") as f:
        bg = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{bg}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        [data-testid="stSidebar"] {{
            background-color: rgba(255,255,255,0.92);
        }}

        .block-container {{
            background-color: rgba(255,255,255,0.88);
            border-radius: 15px;
            padding: 25px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# 3. TITLE
# ============================================================

st.title("STAFF TRAINING PORTAL.")

# ============================================================
# 4. CREATE REQUIRED FOLDERS
# ============================================================

FOLDERS = [
    "employees",
    "training_videos",
    "training_ppt",
    "exam_papers",
    "submitted_papers",
    "response_videos"
]

for folder in FOLDERS:
    os.makedirs(folder, exist_ok=True)

# ============================================================
# 5. SESSION STATE
# ============================================================

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "emp_logged_in" not in st.session_state:
    st.session_state.emp_logged_in = False

if "emp_data" not in st.session_state:
    st.session_state.emp_data = {}

# ============================================================
# 6. SIDEBAR MENU
# ============================================================

st.sidebar.title("TRAINING PORTAL")

portal_selection = st.sidebar.radio(
    "Choose Portal:",
    [
        "👤 Employee Portal",
        "🔐 Admin Portal"
    ],
    key="main_portal_menu"
)

# ============================================================
# 🔐 ADMIN PORTAL
# ============================================================

if portal_selection == "🔐 Admin Portal":

    st.header("🔐 Admin Management Portal")

    # --------------------------------------------------------
    # ADMIN LOGIN
    # --------------------------------------------------------

    if not st.session_state.admin_logged_in:

        st.subheader("🔑 Admin Login")

        user = st.text_input(
            "Admin Username",
            key="admin_user_login"
        )

        pwd = st.text_input(
            "Admin Password",
            type="password",
            key="admin_password_login"
        )

        if st.button(
            "🔓 Login as Admin",
            key="admin_login_button"
        ):

            if user == "admin" and pwd == "admin123":

                st.session_state.admin_logged_in = True

                st.success(
                    "✅ Admin Login Successful!"
                )

                st.rerun()

            else:

                st.error(
                    "❌ Invalid Username or Password"
                )

    # --------------------------------------------------------
    # ADMIN DASHBOARD
    # --------------------------------------------------------

    else:

        st.sidebar.success("🟢 Admin Logged In")

        if st.sidebar.button(
            "🚪 Logout Admin",
            key="admin_logout_button"
        ):

            st.session_state.admin_logged_in = False
            st.rerun()

        # ----------------------------------------------------
        # ADMIN TABS
        # ----------------------------------------------------

        tab1, tab2, tab3 = st.tabs(
            [
                "👥 Employee Registration",
                "📚 Upload Training",
                "📊 Employee Records"
            ]
        )

        # ====================================================
        # TAB 1 - EMPLOYEE REGISTRATION
        # ====================================================

        with tab1:

            st.subheader(
                "👥 Upload Employee Master List"
            )

            st.write(
                "Upload Excel file containing employees who are allowed to access the training."
            )

            employee_file = st.file_uploader(
                "📂 Choose Employee Excel File",
                type=["xlsx"],
                key="employee_excel_upload"
            )

            if employee_file:

                try:

                    employee_df = pd.read_excel(
                        employee_file
                    )

                    st.write(
                        "### 👀 Employee List Preview"
                    )

                    st.dataframe(
                        employee_df,
                        use_container_width=True
                    )

                    if st.button(
                        "✅ Register Employees",
                        key="register_employee_button"
                    ):

                        employee_df.to_csv(
                            "employees/employee_list.csv",
                            index=False
                        )

                        st.success(
                            f"🎉 {len(employee_df)} employees registered successfully!"
                        )

                except Exception as e:

                    st.error(
                        f"❌ Error reading Excel file: {e}"
                    )

            st.info(
                "Excel should contain at least: Employee ID and Employee Name."
            )

        # ====================================================
        # TAB 2 - UPLOAD TRAINING
        # ====================================================

        with tab2:

            st.subheader(
                "📚 Training Material Publishing"
            )

            st.write(
                "Upload training material and publish it for registered employees."
            )

            training_title = st.text_input(
                "📌 Training Title",
                placeholder="Example: 5S Training / Quality Awareness / Safety Training",
                key="training_title"
            )

            st.divider()

            video = st.file_uploader(
                "🎥 Upload Training Video",
                type=["mp4", "avi", "mov"],
                key="training_video_upload"
            )

            ppt = st.file_uploader(
                "📊 Upload Training PPT",
                type=["ppt", "pptx"],
                key="training_ppt_upload"
            )

            paper = st.file_uploader(
                "📄 Upload Exam Paper",
                type=["pdf", "docx", "xlsx"],
                key="exam_paper_upload"
            )

            st.divider()

            if st.button(
                "📢 PUBLISH TRAINING TO ALL EMPLOYEES",
                key="publish_training_button"
            ):

                employee_csv = (
                    "employees/employee_list.csv"
                )

                if not os.path.exists(employee_csv):

                    st.error(
                        "❌ Please upload and register the Employee List first."
                    )

                elif not training_title.strip():

                    st.warning(
                        "⚠️ Please enter Training Title."
                    )

                elif not video and not ppt and not paper:

                    st.warning(
                        "⚠️ Please upload Video, PPT or Exam Paper."
                    )

                else:

                    if video:

                        video_path = os.path.join(
                            "training_videos",
                            video.name
                        )

                        with open(
                            video_path,
                            "wb"
                        ) as f:

                            f.write(
                                video.getbuffer()
                            )

                    if ppt:

                        ppt_path = os.path.join(
                            "training_ppt",
                            ppt.name
                        )

                        with open(
                            ppt_path,
                            "wb"
                        ) as f:

                            f.write(
                                ppt.getbuffer()
                            )

                    if paper:

                        paper_path = os.path.join(
                            "exam_papers",
                            paper.name
                        )

                        with open(
                            paper_path,
                            "wb"
                        ) as f:

                            f.write(
                                paper.getbuffer()
                            )

                    publish_data = pd.DataFrame(
                        [{
                            "Training Title": training_title,
                            "Video": video.name if video else "",
                            "PPT": ppt.name if ppt else "",
                            "Exam Paper": paper.name if paper else ""
                        }]
                    )

                    publish_data.to_csv(
                        "published_training.csv",
                        index=False
                    )

                    st.success(
                        "🚀 Training Published Successfully!"
                    )

                    st.info(
                        "✅ All registered employees can now access this training."
                    )

        # ====================================================
        # TAB 3 - EMPLOYEE RECORDS
        # ====================================================

        with tab3:

            st.subheader(
                "📊 Employee Submission Records"
            )

            csv_path = (
                "submitted_papers/responses_summary.csv"
            )

            if os.path.exists(csv_path):

                records = pd.read_csv(
                    csv_path
                )

                st.dataframe(
                    records,
                    use_container_width=True
                )

                st.divider()

                st.write(
                    "### 📥 Submitted Papers"
                )

                for index, row in records.iterrows():

                    if "Answer_Sheet" in row:

                        file_name = row["Answer_Sheet"]

                        file_path = os.path.join(
                            "submitted_papers",
                            str(file_name)
                        )

                        if os.path.exists(file_path):

                            with open(
                                file_path,
                                "rb"
                            ) as f:

                                st.download_button(
                                    "📥 Download Answer",
                                    f.read(),
                                    file_name=file_name,
                                    key=f"download_{index}"
                                )

            else:

                st.info(
                    "ℹ️ No employee submissions available yet."
                )


# ============================================================
# 👤 EMPLOYEE PORTAL
# ============================================================

elif portal_selection == "👤 Employee Portal":

    st.header(
        "👥 Employee Training & Exam Portal"
    )

    # --------------------------------------------------------
    # EMPLOYEE LOGIN
    # --------------------------------------------------------

    if not st.session_state.emp_logged_in:

        st.subheader(
            "🔑 Employee Sign-In"
        )

        # ====================================================
        # EMPLOYEE BASIC DETAILS
        # ====================================================

        emp_id = st.text_input(
            "Employee ID",
            placeholder="Example: DT101",
            key="employee_id_login"
        )

        emp_name = st.text_input(
            "Employee Name",
            key="employee_name_login"
        )

        # ====================================================
        # REQUIRED TRAINING DETAILS
        # ====================================================

        st.write("### 📋 Training Details")

        col1, col2 = st.columns(2)

        with col1:

            required_date = st.date_input(
                "📅 Required Date *",
                value=date.today(),
                key="required_training_date"
            )

            department = st.text_input(
                "🏢 Department *",
                placeholder="Example: Quality / Production / HR",
                key="employee_department"
            )

        with col2:

            required_time = st.time_input(
                "⏰ Required Time *",
                value=time(9, 0),
                key="required_training_time"
            )

            plant_name = st.text_input(
                "🏭 Plant Name *",
                placeholder="Example: Chhatrapati Sambhajinagar Plant",
                key="employee_plant_name"
            )

        st.info(
            "ℹ️ Date, Time, Department and Plant Name are mandatory."
        )

        if st.button(
            "🚀 Enter Training Portal",
            key="employee_login_button"
        ):

            employee_csv = (
                "employees/employee_list.csv"
            )

            if not os.path.exists(employee_csv):

                st.error(
                    "❌ Employee list has not been uploaded by Admin."
                )

            elif not emp_id.strip():

                st.warning(
                    "⚠️ Please enter Employee ID."
                )

            elif not emp_name.strip():

                st.warning(
                    "⚠️ Please enter Employee Name."
                )

            elif not department.strip():

                st.warning(
                    "⚠️ Please enter Department."
                )

            elif not plant_name.strip():

                st.warning(
                    "⚠️ Please enter Plant Name."
                )

            else:

                employee_df = pd.read_csv(
                    employee_csv
                )

                # Find Employee ID column
                id_column = None

                for col in employee_df.columns:

                    if col.lower().replace(
                        " ", "_"
                    ) in [
                        "employee_id",
                        "emp_id",
                        "employeeid",
                        "id"
                    ]:

                        id_column = col
                        break

                if id_column is None:

                    st.error(
                        "❌ Excel must contain Employee ID column."
                    )

                else:

                    match = employee_df[
                        employee_df[id_column]
                        .astype(str)
                        .str.strip()
                        .str.upper()
                        ==
                        emp_id.strip().upper()
                    ]

                    if len(match) == 0:

                        st.error(
                            "❌ Employee ID not registered. Access Denied."
                        )

                    else:

                        employee_row = match.iloc[0]

                        # Get employee name
                        name_column = None

                        for col in employee_df.columns:

                            if col.lower().replace(
                                " ", "_"
                            ) in [
                                "employee_name",
                                "emp_name",
                                "name"
                            ]:

                                name_column = col
                                break

                        registered_name = (
                            str(employee_row[name_column])
                            if name_column
                            else emp_name
                        )

                        # ====================================
                        # SAVE EMPLOYEE SESSION DETAILS
                        # ====================================

                        st.session_state.emp_logged_in = True

                        st.session_state.emp_data = {
                            "id": emp_id,
                            "name": registered_name,
                            "required_date": str(required_date),
                            "required_time": str(required_time),
                            "department": department,
                            "plant_name": plant_name
                        }

                        st.success(
                            f"✅ Welcome {registered_name}!"
                        )

                        st.rerun()

    # --------------------------------------------------------
    # EMPLOYEE DASHBOARD
    # --------------------------------------------------------

    else:

        emp = st.session_state.emp_data

        st.sidebar.success(
            f"👤 {emp['name']}\n\n"
            f"🆔 {emp['id']}\n\n"
            f"🏢 {emp['department']}\n\n"
            f"🏭 {emp['plant_name']}"
        )

        if st.sidebar.button(
            "🚪 Logout Employee",
            key="employee_logout_button"
        ):

            st.session_state.emp_logged_in = False
            st.session_state.emp_data = {}

            st.rerun()

        # ====================================================
        # EMPLOYEE INFORMATION
        # ====================================================

        st.subheader(
            f"👋 Welcome, {emp['name']}"
        )

        # ====================================================
        # REQUIRED DATE / TIME / DEPARTMENT / PLANT
        # ====================================================

        st.write("### 📋 Employee Training Details")

        info_col1, info_col2, info_col3, info_col4 = st.columns(4)

        with info_col1:

            st.info(
                f"🆔 Employee ID\n\n{emp['id']}"
            )

        with info_col2:

            st.info(
                f"📅 Required Date\n\n{emp['required_date']}"
            )

        with info_col3:

            st.info(
                f"⏰ Required Time\n\n{emp['required_time']}"
            )

        with info_col4:

            st.info(
                f"🏢 Department\n\n{emp['department']}"
            )

        st.info(
            f"🏭 Plant Name: **{emp['plant_name']}**"
        )

        # ====================================================
        # TRAINING INFORMATION
        # ====================================================

        if os.path.exists(
            "published_training.csv"
        ):

            published = pd.read_csv(
                "published_training.csv"
            )

            if len(published) > 0:

                training = published.iloc[-1]

                st.info(
                    f"📚 Current Training: {training['Training Title']}"
                )

        # ====================================================
        # TWO COLUMNS
        # ====================================================

        col1, col2 = st.columns(2)

        # ====================================================
        # LEFT - TRAINING
        # ====================================================

        with col1:

            st.subheader(
                "📚 1. Training Materials"
            )

            # ------------------------------
            # VIDEO
            # ------------------------------

            st.write(
                "### 🎥 Training Video"
            )

            video_files = os.listdir(
                "training_videos"
            )

            if video_files:

                for file_name in video_files:

                    video_path = os.path.join(
                        "training_videos",
                        file_name
                    )

                    st.write(
                        f"▶️ {file_name}"
                    )

                    st.video(
                        video_path
                    )

            else:

                st.info(
                    "No training video available."
                )

            # ------------------------------
            # PPT
            # ------------------------------

            st.write(
                "### 📊 Training PPT"
            )

            ppt_files = os.listdir(
                "training_ppt"
            )

            if ppt_files:

                for file_name in ppt_files:

                    ppt_path = os.path.join(
                        "training_ppt",
                        file_name
                    )

                    with open(
                        ppt_path,
                        "rb"
                    ) as f:

                        st.download_button(
                            "📥 Download PPT",
                            f.read(),
                            file_name=file_name,
                            key=f"ppt_{file_name}"
                        )

            else:

                st.info(
                    "No training PPT available."
                )

        # ====================================================
        # RIGHT - EXAM
        # ====================================================

        with col2:

            st.subheader(
                "📝 2. Exam & Submission"
            )

            # ------------------------------
            # EXAM PAPER
            # ------------------------------

            st.write(
                "### 📄 Exam Paper"
            )

            paper_files = os.listdir(
                "exam_papers"
            )

            if paper_files:

                for file_name in paper_files:

                    paper_path = os.path.join(
                        "exam_papers",
                        file_name
                    )

                    with open(
                        paper_path,
                        "rb"
                    ) as f:

                        st.download_button(
                            "📥 Download Exam Paper",
                            f.read(),
                            file_name=file_name,
                            key=f"paper_{file_name}"
                        )

            else:

                st.warning(
                    "No exam paper available."
                )

            st.divider()

            # ------------------------------
            # SUBMIT ANSWER PAPER
            # ------------------------------

            st.write(
                "### 📝 Submit Completed Exam"
            )

            answer_file = st.file_uploader(
                "Upload Completed Answer Paper",
                type=[
                    "pdf",
                    "docx",
                    "xlsx",
                    "jpg",
                    "png"
                ],
                key="employee_answer_upload"
            )

            if st.button(
                "📤 Submit Answer Paper",
                key="submit_answer_button"
            ):

                if not answer_file:

                    st.warning(
                        "⚠️ Please select your completed answer paper."
                    )

                else:

                    safe_name = (
                        f"{emp['id']}_{answer_file.name}"
                    )

                    save_path = os.path.join(
                        "submitted_papers",
                        safe_name
                    )

                    with open(
                        save_path,
                        "wb"
                    ) as f:

                        f.write(
                            answer_file.getbuffer()
                        )

                    # ========================================
                    # CREATE SUBMISSION RECORD
                    # ========================================

                    record = pd.DataFrame(
                        [{
                            "Emp_ID": emp["id"],
                            "Name": emp["name"],
                            "Required_Date": emp["required_date"],
                            "Required_Time": emp["required_time"],
                            "Department": emp["department"],
                            "Plant_Name": emp["plant_name"],
                            "Answer_Sheet": safe_name
                        }]
                    )

                    summary_file = (
                        "submitted_papers/responses_summary.csv"
                    )

                    if os.path.exists(
                        summary_file
                    ):

                        old_records = pd.read_csv(
                            summary_file
                        )

                        record = pd.concat(
                            [
                                old_records,
                                record
                            ],
                            ignore_index=True
                        )

                    record.to_csv(
                        summary_file,
                        index=False
                    )

                    st.success(
                        "✅ Answer Paper Submitted Successfully!"
                    )

            st.divider()
