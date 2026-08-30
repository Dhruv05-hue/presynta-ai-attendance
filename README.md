# 🎓 PRESYNTA — Intelligent AI Attendance Management

> **Intelligent Presence Management powered by Face Recognition and Voice Recognition.**

PRESYNTA is a modern **AI-powered attendance management platform** designed to make classroom attendance faster, smarter, and easier to manage.

Built with **Python, Streamlit, Supabase, Computer Vision, and Voice Recognition**, PRESYNTA allows teachers to manage subjects, enroll students, capture classroom attendance using faces or voices, review AI-generated results, and explore detailed attendance records.

Students receive their own portal for managing subjects and viewing attendance information.

---

## ✨ Key Features

### 🤖 AI Face Attendance

Teachers can capture or upload classroom photographs and let PRESYNTA automatically identify enrolled students.

- Capture classroom photos directly from the application
- Upload multiple classroom images
- Detect multiple faces
- Generate 128-dimensional facial embeddings
- Identify students using an SVM classifier
- Verify predictions against stored facial embeddings
- Reject low-confidence matches
- Automatically generate Present / Absent results
- Review attendance before saving

---

### 🎙️ AI Voice Attendance

PRESYNTA also provides voice-based attendance as an alternative to facial recognition.

Teachers can record classroom audio while students respond with phrases such as:

> **"I am present."**

The voice pipeline then:

1. Processes the classroom recording
2. Detects speech segments
3. Generates voice embeddings
4. Compares them against enrolled student voice profiles
5. Applies a similarity threshold
6. Identifies matching students
7. Generates attendance results

Only students enrolled in the selected subject are considered during recognition.

---

## 👨‍🏫 Teacher Portal

The redesigned teacher dashboard provides a centralized workspace for classroom management.

Teachers can:

- Create and manage subjects
- View enrolled student counts
- View total classes conducted
- Share subjects with students
- Generate subject enrollment links
- Generate QR codes for quick enrollment
- Capture face attendance
- Capture voice attendance
- Review attendance before confirmation
- Browse previous attendance sessions
- View student-level attendance for individual classes

---

## 👨‍🎓 Student Portal

Students have a dedicated interface for managing their academic attendance.

Students can:

- View enrolled subjects
- Join subjects using enrollment codes
- Join subjects through shared links
- Join through teacher-generated QR codes
- View subject information
- Access attendance information
- Manage their subject enrollment

---

## 🔗 Smart Subject Enrollment

PRESYNTA provides multiple ways for students to join a subject.

### Enrollment Code

Teachers create subjects with unique subject codes that students can enter manually.

### Shareable Link

PRESYNTA can generate a direct enrollment URL for a subject.

```text
PRESYNTA
    ↓
Teacher selects subject
    ↓
Generate enrollment link
    ↓
Student opens link
    ↓
Enrollment confirmation
    ↓
Student joins subject
```

### QR Code Enrollment

Every shareable subject link can also be represented as a QR code.

Students can scan the QR code and immediately open the subject enrollment flow.

---

# 📊 Attendance Records

PRESYNTA organizes attendance around actual classroom sessions rather than displaying only raw attendance logs.

```text
Teacher
   │
   └── Subject
          │
          ├── Class Session
          │      ├── Student A → Present
          │      ├── Student B → Absent
          │      └── Student C → Present
          │
          └── Class Session
                 ├── Student A → Present
                 ├── Student B → Present
                 └── Student C → Absent
```

Teachers can select a subject and inspect individual classes with:

- Class date
- Class time
- Student name
- Student ID
- Present / Absent status
- Attendance statistics

This provides a much clearer history of classroom attendance.

---

# 🧠 Face Recognition Pipeline

```text
Classroom Image
       │
       ▼
Face Detection
       │
       ▼
Facial Landmarks
       │
       ▼
128-D Face Embedding
       │
       ▼
SVM Classification
       │
       ▼
Predicted Student
       │
       ▼
Embedding Verification
       │
       ▼
Similarity Threshold
       │
   ┌───┴───┐
   ▼       ▼
Present   Reject
```

The face recognition pipeline converts each detected face into a numerical embedding.

An SVM classifier predicts the likely student identity. The predicted student's stored facial embedding is then compared with the detected embedding as an additional verification step.

---

# 🎙️ Voice Recognition Pipeline

```text
Classroom Audio
       │
       ▼
Audio Preprocessing
       │
       ▼
Speech Segmentation
       │
       ▼
Voice Embedding
       │
       ▼
Compare Enrolled Profiles
       │
       ▼
Similarity Threshold
       │
       ▼
Identify Student
       │
       ▼
Generate Attendance
```

PRESYNTA uses stored voice embeddings to compare recorded speech against students enrolled in the selected subject.

---

# 🏗️ Project Architecture

```text
PRESYNTA/
│
├── src/
│   │
│   ├── components/
│   │   ├── dialog_add_photo.py
│   │   ├── dialog_attendance_result.py
│   │   ├── dialog_auto_enroll.py
│   │   ├── dialog_create_subject.py
│   │   ├── dialog_enroll.py
│   │   ├── dialog_share_subject.py
│   │   ├── dialog_voice_attendance.py
│   │   ├── footer.py
│   │   ├── header.py
│   │   └── subject_card.py
│   │
│   ├── database/
│   │   ├── config.py
│   │   └── db.py
│   │
│   ├── pipelines/
│   │   ├── face_pipeline.py
│   │   └── voice_pipeline.py
│   │
│   ├── screen/
│   │   ├── home_screen.py
│   │   ├── student_screen.py
│   │   └── teacher_screen.py
│   │
│   └── ui/
│       └── base_layout.py
│
├── .streamlit/
│   └── secrets.toml
│
├── .gitignore
├── requirements.txt
└── app.py
```

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application language |
| **Streamlit** | Web application and interactive UI |
| **Supabase** | Backend database services |
| **PostgreSQL** | Relational database |
| **Dlib / Face Recognition** | Face detection and embeddings |
| **Scikit-learn SVM** | Face classification |
| **Resemblyzer** | Voice embeddings and speaker recognition |
| **Librosa** | Audio loading and processing |
| **NumPy** | Numerical and embedding operations |
| **Pandas** | Attendance processing and tables |
| **Segno** | QR code generation |
| **bcrypt** | Password hashing |

---

# 🗄️ Database Design

PRESYNTA uses **Supabase/PostgreSQL** to manage application data.

The primary relationships are:

```text
Teachers
   │
   └── Subjects
          │
          ├── Subject Students
          │       │
          │       └── Students
          │              ├── Face Embedding
          │              └── Voice Embedding
          │
          └── Attendance Logs
                  ├── Student ID
                  ├── Subject ID
                  ├── Timestamp
                  └── Attendance Status
```

Attendance records contain:

- Student ID
- Subject ID
- Timestamp
- Present / Absent status

The shared timestamp allows records belonging to the same attendance session to be grouped together.

---

# 🔄 Complete Attendance Workflow

## Face Attendance

```text
Teacher selects subject
          ↓
Capture / Upload classroom photos
          ↓
Detect student faces
          ↓
Generate face embeddings
          ↓
Predict identities
          ↓
Verify embeddings
          ↓
Check enrolled students
          ↓
Generate Present / Absent results
          ↓
Teacher reviews results
          ↓
Confirm & Save
          ↓
Attendance stored in Supabase
```

## Voice Attendance

```text
Teacher selects subject
          ↓
Record classroom audio
          ↓
Detect speech segments
          ↓
Generate voice embeddings
          ↓
Compare enrolled voice profiles
          ↓
Identify students
          ↓
Generate Present / Absent results
          ↓
Teacher reviews results
          ↓
Confirm & Save
          ↓
Attendance stored in Supabase
```

---

# 🎨 Modern Responsive Interface

PRESYNTA features a completely redesigned interface built around a consistent visual system.

The UI includes:

- Dedicated student and teacher portals
- Modern subject cards
- Responsive dashboards
- Mobile-friendly layouts
- Consistent typography
- Interactive dialogs
- Attendance review tables
- Subject-level attendance navigation
- Session-level attendance details
- QR-based enrollment
- Clear empty states and status indicators

The interface is designed to remain usable across desktop, tablet, and mobile screen sizes.

---

# 🔐 Security

Sensitive credentials must **never be committed to GitHub**.

PRESYNTA supports configuration through Streamlit secrets:

```text
.streamlit/secrets.toml
```

Example:

```toml
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-key"
```

Your `.gitignore` should include:

```gitignore
.env
.streamlit/
venv/
venv311/
__pycache__/
*.pyc
```

> ⚠️ Never commit Supabase keys, passwords, API keys, or other private credentials.

Teacher passwords should be stored as secure password hashes rather than plain-text passwords.

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone <your-new-presynta-repository-url>
cd presynta-ai-attendance
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Supabase

Create your Supabase project and configure the required tables and relationships.

Add the required credentials to:

```text
.streamlit/secrets.toml
```

## 5. Start PRESYNTA

```bash
streamlit run app.py
```

Streamlit will provide the local application URL.

---

# 🎯 Project Goals

PRESYNTA was created to improve traditional classroom attendance by combining AI recognition with modern attendance management.

The project aims to:

- ⏱️ Reduce time spent taking attendance
- 🤖 Automate student identification
- 📸 Support multi-student classroom image recognition
- 🎙️ Provide voice-based attendance
- 📊 Organize attendance by subject and class session
- 🔗 Simplify student enrollment
- 📱 Provide a responsive web interface
- 🗄️ Centralize attendance records
- 👨‍🏫 Simplify attendance management for teachers
- 👨‍🎓 Provide students with direct access to their subjects

---

# ⚠️ AI Recognition Considerations

AI recognition accuracy can be influenced by environmental conditions.

### Face recognition

Factors include:

- Lighting
- Camera quality
- Face angle
- Distance from camera
- Occlusion
- Image resolution

### Voice recognition

Factors include:

- Background noise
- Microphone quality
- Multiple people speaking simultaneously
- Voice variations
- Recording distance

For real-world deployment, biometric recognition should be used responsibly with appropriate privacy, security, and consent practices.

---

# 🔮 Future Improvements

Potential future improvements include:

- [ ] Advanced attendance analytics
- [ ] Attendance percentage visualization
- [ ] CSV/PDF report exports
- [ ] Automated attendance reports
- [ ] Improved voice separation in noisy classrooms
- [ ] Improved face recognition under difficult conditions
- [ ] Duplicate-session protection
- [ ] More advanced authentication and authorization
- [ ] Notification system
- [ ] Additional attendance insights

---

# 👨‍💻 Author

**Dhruv Pawar**

BSc IT | AI/ML Developer

Interested in:

- Artificial Intelligence
- Machine Learning
- Computer Vision
- Generative AI
- Backend Development
- Full-Stack AI Applications

---

# ⭐ PRESYNTA

If you find **PRESYNTA** useful or interesting, consider giving the repository a ⭐.

> **PRESYNTA — Intelligent Presence Management.**