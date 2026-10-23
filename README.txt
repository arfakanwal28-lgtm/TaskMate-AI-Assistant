TASKMATE — PENPOT-INSPIRED FLASK WEBSITE

Pages included:
- Dashboard
- My Tasks (search, complete, edit, delete)
- Add/Edit Task
- AI Assistant (rule-based suggestions based on saved tasks)

IMPORTANT:
This is a student prototype. The assistant suggestions are rule-based, not a trained AI model.
The website does not connect to an external AI service.

HOW TO RUN IN VS CODE (Windows PowerShell)

1. Extract this ZIP file.
2. In VS Code choose File > Open Folder and select the extracted TaskMate_Penpot_Match folder.
3. Open Terminal > New Terminal.
4. Create a virtual environment (only needed once):
   py -m venv .venv
5. Activate it:
   .\.venv\Scripts\Activate.ps1
   If PowerShell blocks activation, use Command Prompt terminal and run:
   .venv\Scripts\activate.bat
6. Install Flask:
   python -m pip install -r requirements.txt
7. Start the website:
   python app.py
8. In Chrome or Edge open:
   http://127.0.0.1:5000

Keep the terminal open while using the website. Press Ctrl+C in the terminal to stop it.

If you already have a TaskMate project open, save a backup before replacing files.
This project creates tasks.db automatically when first run.
