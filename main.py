import streamlit as st


# Class definitions (unchanged from original)
class Tutor:
    def __init__(self, firstName, lastName, username, bio, subjects, image):
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.bio = bio
        self.subjects = subjects  # list of integers that correlates with subject list
        self.image = image
        with open("tutors.csv", "a") as f:
            f.write(f"{firstName} {lastName}, {username}, \"{bio}\", {subjects},{image}\n")
            f.close()

    def modifySubjects(self, newList):
        self.subjects = newList

    def getSubjectNames(self, subjects):
        list = openSubjectList()
        return [list[i] for i in subjects]


class Student:
    def __init__(self, firstName, lastName, username, grade, subjects):
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.grade = grade
        self.subjects = subjects  # list of integers that correlates with subject list
        with open("students.csv", "a") as f:
            f.write(f"{firstName} {lastName}, {username}, {grade}, {subjects}\n")
            f.close()

    def modifySubjects(self, newList):
        self.subjects = newList

    def getSubjectNames(self, subjects):
        list = openSubjectList()
        return [list[i] for i in subjects]


# Page configuration
st.set_page_config(page_title="BridgeSTEM Tutoring", layout="wide", initial_sidebar_state="expanded")


# Load subjects from file
def openSubjectList():
    with open('subjectList.txt', 'r') as f:
        SUBJECTS = [line.strip().strip('"') for line in f.readlines()]
        f.close()
    return SUBJECTS


def accountExists(username):
    """Check if username already exists in student.csv"""
    try:
        with open('students.csv', 'r') as f:
            content = f.read()
            f.close()
            # Check if username appears in the file
            if username in content:
                return True
            return False
    except FileNotFoundError:
        # If file doesn't exist yet, account doesn't exist
        return False


def loadTutors():
    """Load tutors from tutors.csv file"""
    tutors = []
    try:
        with open('tutors.csv', 'r') as f:
            lines = f.readlines()
            f.close()

        for line in lines:
            if line.strip():
                # Parse CSV line: Name, username, "bio", [subjects], image
                parts = line.strip().split(', ')
                name = parts[0]  # "FirstName LastName"
                username = parts[1]

                # Find the bio (enclosed in quotes)
                bio_start = line.find('"')
                bio_end = line.find('"', bio_start + 1)
                bio = line[bio_start + 1:bio_end]

                # Find the subjects list
                subjects_start = line.find('[')
                subjects_end = line.find(']')
                subjects_str = line[subjects_start:subjects_end + 1]
                subjects = eval(subjects_str)  # Convert string to list

                # Get image filename (last part)
                image = parts[-1].strip()

                tutors.append({
                    'name': name,
                    'username': username,
                    'bio': bio,
                    'subjects': subjects,
                    'image': image
                })
    except FileNotFoundError:
        # Return empty list if file doesn't exist
        pass

    return tutors


# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Sidebar navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Home", use_container_width=True):
    st.session_state.current_page = 'home'
if st.sidebar.button("Create Account", use_container_width=True):
    st.session_state.current_page = 'create_account'

st.sidebar.divider()
st.sidebar.markdown("### BridgeSTEM")
st.sidebar.markdown("If you have any questions or are interested in becoming a tutor please feel free to reach out to Amit Vaysman")
st.sidebar.markdown("23amitvays@gmail.com")
st.sidebar.markdown("(669)-284-4440")

# Common CSS (unchanged from original)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Work+Sans:wght@400&display=swap');

    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }

    footer {
        visibility: hidden;
    }

    /* Make all text black */
    * {
        color: #000000 !important;
    }

    /* Ensure sidebar text is black */
    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }

    /* Baby blue top bar */
    header[data-testid="stHeader"] {
        background-color: #89CFF0 !important;
    }

    /* White background for all input fields */
    input[type="text"], 
    textarea,
    select,
    .stTextInput input,
    .stSelectbox select,
    [data-baseweb="select"],
    [data-baseweb="input"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    /* White background for dropdown menus */
    [data-baseweb="popover"] {
        background-color: #FFFFFF !important;
    }

    [data-baseweb="menu"] {
        background-color: #FFFFFF !important;
    }

    [data-baseweb="menu"] li {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    [data-baseweb="menu"] li:hover {
        background-color: #F0F0F0 !important;
    }

    /* White background for select dropdown itself */
    [data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
    }

    /* Make ALL text black */
    * {
        color: #000000 !important;
    }

    body, p, span, div, label, input, textarea, select, option {
        color: #000000 !important;
    }

    /* Ensure sidebar is visible */
    [data-testid="stSidebar"] {
        background-color: #F8F9FA;
    }

    [data-testid="stSidebar"] button {
        background-color: #FFFFFF;
        border: 2px solid #E6E6E6;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }

    [data-testid="stSidebar"] button:hover {
        border-color: #4A90E2;
        background-color: #E3F2FD;
    }

    .section-text {
        font-family: 'Work Sans', sans-serif;
        font-size: 16px;
        line-height: 1.6;
        color: #000000;
    }

    hr {
        border: none;
        height: 1px;
        background-color: #E6E6E6;
        margin: 2rem 0;
    }

    /* Ensure all headers are fully visible */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
        opacity: 1 !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
    }

    /* IMPORTANT: Fix dropdown menu background to WHITE */
    [role="listbox"] {
        background: #FFFFFF !important;
    }

    [role="option"] {
        background: #FFFFFF !important;
        color: #000000 !important;
    }

    [role="option"]:hover {
        background: #F0F0F0 !important;
    }

    /* IMPORTANT: Dark blue ONLY for form submit button (NOT sidebar buttons) */
    form button[type="submit"],
    form button[data-testid="baseButton-primary"],
    .stForm button[kind="primary"],
    .stForm button {
        background: #1E3A8A !important;
        border: none !important;
    }

    form button[type="submit"] p,
    form button[type="submit"] span,
    form button[data-testid="baseButton-primary"] p,
    form button[data-testid="baseButton-primary"] span,
    .stForm button p,
    .stForm button span {
        color: #FFFFFF !important;
    }

    form button[type="submit"]:hover,
    form button[data-testid="baseButton-primary"]:hover,
    .stForm button:hover {
        background: #1E40AF !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ===== HOME PAGE (ORIGINAL CONTENT) =====
if st.session_state.current_page == 'home':
    # Original main.py content starts here
    st.image("BridgeSTEM.png", use_container_width=True)

    st.markdown(
        "<div class='section-text'>BridgeSTEM Tutoring is a Bay Area-based initiative dedicated to bridging the gap between struggling high schoolers and passionate community college students. Whether you need a comprehensive 30-minute tutoring session online or a quick response on our subject-specific discussion boards, we provide the free, localized support students need to excel.</div>",
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        """
        <div style="
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            font-size: 32px;
            color: #000000;
            opacity: 1;
            margin-bottom: 0.5rem;
        ">
            10+ Active Tutors
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='section-text'>Unlock expert guidance from a wide network of real community college STEM students from three separate campuses:<br>West Valley College, Mission College, and De Anza College.</div>",
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        """
        <div style="
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            font-size: 32px;
            color: #000000;
            opacity: 1;
            margin-bottom: 0.5rem;
        ">
            Help is available in 30 subjects
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='section-text'>Our curriculum spans the full STEM range—including Mathematics from Algebra to Calculus, and Sciences like Physics, Biology, Chemistry and Economics. We offer specialized mentorship for 15 Advanced Placement (AP) courses, ensuring students stay on track during the school year and while studying for their AP tests.</div>",
        unsafe_allow_html=True
    )

    st.divider()

    # Tutor Profiles Section
    st.markdown(
        """
        <div style="
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            font-size: 32px;
            color: #000000;
            opacity: 1;
            margin-bottom: 1.5rem;
        ">
            Meet Our Tutors
        </div>
        """,
        unsafe_allow_html=True
    )

    # Load tutors from CSV
    tutors = loadTutors()
    SUBJECTS = openSubjectList()

    # Create rows of 3 tutors each (10 total = 4 rows, last row has 1 tutor)
    num_rows = (len(tutors) + 2) // 3  # Round up division

    for row in range(num_rows):
        cols = st.columns(3)

        for col_idx, col in enumerate(cols):
            tutor_idx = row * 3 + col_idx

            # Only display if we have a tutor for this slot
            if tutor_idx < len(tutors):
                tutor = tutors[tutor_idx]

                with col:
                    # Profile picture
                    try:
                        st.image(tutor['image'], width=80)
                    except:
                        st.markdown(
                            '<div style="width: 80px; height: 80px; border-radius: 50%; background: #E6E6E6; margin: 0 auto 1rem auto;"></div>',
                            unsafe_allow_html=True
                        )

                    # Name
                    st.markdown(f"**{tutor['name']}**")

                    # Bio
                    st.markdown(tutor['bio'])

                    # Subject tags - show ALL subjects, 2 per row
                    tags_html = '<div style="margin-top: 0.5rem;">'
                    for i, subject_idx in enumerate(tutor['subjects']):
                        if subject_idx < len(SUBJECTS):
                            subject_name = SUBJECTS[subject_idx]

                            # Start a new row div every 2 tags
                            if i % 2 == 0:
                                if i > 0:
                                    tags_html += '</div>'  # Close previous row
                                tags_html += '<div style="margin-bottom: 0.5rem;">'

                            tags_html += f'''<span style="
                                display: inline-block;
                                background: #E3F2FD;
                                color: #1976D2;
                                padding: 0.25rem 0.75rem;
                                border-radius: 20px;
                                font-size: 11px;
                                font-weight: 500;
                                margin-right: 0.5rem;
                            ">{subject_name}</span>'''

                    # Close the last row div
                    if tutor['subjects']:
                        tags_html += '</div>'
                    tags_html += '</div>'

                    st.markdown(tags_html, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

# ===== CREATE ACCOUNT PAGE =====
elif st.session_state.current_page == 'create_account':
    st.markdown("# Create Account")
    st.markdown("<div class='section-text'>Fill out the form below to create your BridgeSTEM account.</div>",
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("create_account_form"):
        st.markdown("### Personal Information")

        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name *", placeholder="John")
        with col2:
            last_name = st.text_input("Last Name *", placeholder="Doe")

        username = st.text_input("Username *", placeholder="johndoe123")

        grade = st.selectbox(
            "Grade Level *",
            ["Middle School", "9th Grade", "10th Grade", "11th Grade", "12th Grade"]
        )

        st.markdown("### Select Your Subjects")
        st.markdown("<div class='section-text'>Choose all subjects you're interested in tutoring for:</div>",
                    unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Create checkboxes for all subjects
        selected_subjects = []

        # Display subjects in 2 columns for better layout
        col1, col2 = st.columns(2)

        SUBJECTS = openSubjectList()
        for i, subject in enumerate(SUBJECTS):
            if i % 2 == 0:
                with col1:
                    if st.checkbox(subject, key=f"subject_{i}"):
                        selected_subjects.append(i)
            else:
                with col2:
                    if st.checkbox(subject, key=f"subject_{i}"):
                        selected_subjects.append(i)

        st.markdown("<br>", unsafe_allow_html=True)

        # Submit button
        submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)

        if submitted:
            # Validation
            if not first_name or not last_name or not username:
                st.error("⚠️ Please fill in all required fields (First Name, Last Name, Username)")
            elif len(selected_subjects) == 0:
                st.error("⚠️ Please select at least one subject")
            elif accountExists(username):
                st.error(f"⚠️ Username '{username}' already exists. Please choose a different username.")
            else:

                selected_subject_names = [SUBJECTS[i] for i in selected_subjects]

                # Create the output data
                account_data = {
                    "firstName": first_name,
                    "lastName": last_name,
                    "username": username,
                    "grade": grade,
                    "subjects": selected_subjects  # List of indices
                }

                # Navigate back to home page
                st.session_state.current_page = 'home'
                st.rerun()