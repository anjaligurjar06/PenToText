# ✍️ PenToText

> **Context-Aware Handwritten Document Transcription System**

PenToText is an AI-powered web application that transforms handwritten documents into accurate, structured, and editable digital text. Unlike traditional OCR systems that rely solely on image recognition, PenToText improves transcription accuracy by leveraging contextual information provided by the user, making it especially effective for domain-specific handwritten documents such as medical prescriptions, exam papers, and class notes.

The application allows users to upload handwritten images or PDF documents, specify the document category, and provide relevant contextual information such as a patient's medical condition or an academic subject. This additional context helps the AI transcription engine better understand ambiguous handwriting and generate more reliable results.

After transcription, users can review and edit the generated text, inspect low-confidence predictions, export the final document in multiple formats, and maintain a searchable history of all previously processed documents.

---

##  Problem Statement

Handwritten documents are often difficult to interpret due to poor handwriting, abbreviations, and domain-specific terminology. Traditional OCR solutions frequently misinterpret such documents because they lack contextual understanding.

For example:

- Medical prescriptions contain complex drug names and abbreviations.
- Exam papers include technical subject-specific terminology.
- Personal notes often contain shorthand and inconsistent handwriting.

These limitations lead to inaccurate digitization and require extensive manual correction.

---

##  Solution

PenToText introduces **Context-Aware Handwriting Recognition** by combining handwritten document images with user-provided contextual information before transcription.

The AI model receives:

- The handwritten document
- Document category
- Subject or medical condition
- Additional user-provided context

Using this information, the transcription engine generates significantly more accurate text while highlighting uncertain words for manual verification.

---

# ✨ Features

- 📄 Upload handwritten documents (JPG, PNG, PDF)
- 🧠 Context-aware AI transcription
- 📝 Editable transcription results
- ⚠️ Low-confidence word highlighting
- 💊 Structured extraction for medical prescriptions
- 📚 Question-wise formatting for exam papers
- 📥 Export results as PDF or DOCX
- 📜 View and manage transcription history
- 🔍 Search previous transcriptions
- 🔐 Secure user authentication
- 📱 Responsive design for desktop and mobile

---

#  System Workflow

```text
User Login
      │
      ▼
Upload Handwritten Document
      │
      ▼
Select Document Category
      │
      ▼
Provide Context
      │
      ▼
AI Processes Image + Context
      │
      ▼
Generate Transcription
      │
      ▼
Review & Edit
      │
      ▼
Export / Save
      │
      ▼
History Dashboard
```

---

#  Technology Stack

## Frontend

- React.js
- Vite
- JavaScript
- HTML5
- CSS3
- React Router DOM
- Axios
- React Icons

## Backend

- FastAPI
- Python

## Database

- PostgreSQL

## AI & OCR

- Vision Language Model (VLM)
- OCR Engine Integration

---

```

---

# 📋 Usage

1. Register or log in to your account.
2. Upload a handwritten image or PDF.
3. Select the document category.
4. Provide contextual information.
5. Submit the document for transcription.
6. Review and edit the generated text.
7. Export the transcription as PDF or DOCX.
8. Access previous transcriptions from the History page.

---

#  Supported Document Types

- 🩺 Medical Prescriptions
- 📖 Exam Papers
- 📚 Class Notes
- 📝 General Notes
- 📄 Other Handwritten Documents

---

#  Future Enhancements

- 🌍 Multi-language handwriting recognition
- 📷 Live camera scanning
- 📂 Batch document upload
- 📱 Android & iOS applications
- 📊 Admin analytics dashboard
- ☁️ Cloud storage integration
- 🤖 Improved AI confidence scoring
- 📑 OCR fallback for low-quality documents

---


---

## ⭐ If you found this project interesting, consider giving it a star on GitHub!
>>>>>>> 219469a5e949e62803e232df9893b7d4fd79cef5
