# PIWOT_LEGALADVISOR

An AI-powered contract management and analysis dashboard. Upload business contracts in PDF format, get instant AI-driven analysis, and manage your contracts in a modern, user-friendly interface.

## Features

- **AI Contract Analysis:** Upload PDF contracts and receive instant, detailed analysis using Google Gemini AI.
- **Modern Dashboard:** Clean, responsive UI built with Next.js, React, and Tailwind CSS.
- **Drag-and-Drop Upload:** Easily upload contracts with drag-and-drop or file picker.
- **Contract Table:** View, search, and filter all uploaded contracts.
- **Analysis Modal:** Click any contract to view its AI-generated analysis.
- **Backend Integration:** Python Flask backend for file handling and AI communication.

## Tech Stack

- **Frontend:** Next.js, React, TypeScript, Tailwind CSS
- **Backend:** Python, Flask, Google Gemini AI API , TensorFlow 
- **Other:** Axios, React Dropzone

## Getting Started

### Prerequisites

- Node.js (v18+ recommended)
- Python 3.10+
- pip (Python package manager)

### Clone the Repository

```bash
git clone https://github.com/chaurasia-aryan/PIWOT_LEGALADVISOR.git
cd PIWOT_LEGALADVISOR
```

---

### Backend Setup

1. **Install Python dependencies:**
    ```bash
    cd Backend
    pip install -r requirements.txt
    ```
    *(If `requirements.txt` is missing, install Flask, flask-cors, python-dotenv, PyMuPDF, google-generativeai)*

2. **Set up your environment variables:**
    - Create a `.env` file in the `Backend` directory and add your Google Gemini API key:
      ```
      GEMINI_API_KEY=your_google_gemini_api_key
      ```

3. **Run the backend server:**
    ```bash
    python app.py
    ```
    The backend will run at `http://localhost:5000`.

---

### Frontend Setup

1. **Install Node.js dependencies:**
    ```bash
    cd ../frontend
    npm install
    ```

2. **Run the frontend development server:**
    ```bash
    npm run dev
    ```
    The frontend will run at `http://localhost:3000`.

---

## Usage

1. Open your browser and go to [http://localhost:3000](http://localhost:3000).
2. Use the dashboard to upload PDF contracts.
3. Click "View Analysis" on any contract to see the AI-generated summary and metadata.

---

## Project Structure

```
PIWOT_LEGALADVISOR/
│
├── Backend/           # Flask backend for AI analysis
│   ├── app.py
│   └── ...
│
└── frontend/          # Next.js frontend dashboard
    ├── app/
    ├── components/
    └── ...
```

---

## Contributing

Contributions are welcome! Please open issues or pull requests for improvements, bug fixes, or new features.

---

## License

This project is licensed under the MIT License.

---

**Made with ❤️ for the PIWOT Hackathon 2025**
