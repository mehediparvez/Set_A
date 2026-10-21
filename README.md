# Set A - Programming Assignments & Research Projects

This repository contains programming assignments and a research project.

## Projects

### Q1: Employee Management System (Python)
A console-based employee management application demonstrating **Object-Oriented Programming** with inheritance. Supports adding Programmers and Managers, and displaying all employee records.

- **Language:** Python 3
- **Concepts:** Classes, Inheritance, Polymorphism, Method Overriding
- **Directory:** `Q1_Employee/`

### Q2: Text Formatter (C# Windows Forms)
A GUI application for formatting text with different styles (Bold, Italic, Underline) and colors (Red, Blue, Green).

- **Language:** C# (.NET 10, Windows Forms)
- **Concepts:** GUI Programming, Event Handling, Radio Buttons
- **Directory:** `Q2_TextFormatter/`

### Q3: Student Database (C# Windows Forms + SQLite)
A GUI application for managing student records with SQLite database backend. Supports inserting and viewing student information (Roll, Name, Mark).

- **Language:** C# (.NET 10, Windows Forms)
- **Concepts:** Database (SQLite), CRUD Operations, DataGridView
- **Directory:** `Q3_StudentDB/`

### Bangla Profanity & Toxic Comment Detection (ML Research)
A machine learning research project comparing multiple approaches for detecting toxic comments in Bangla text: fine-tuned BanglaBERT, XLM-RoBERTa, LLM zero-shot (Groq), and a `better_profanity` library baseline. Includes training notebooks, evaluation visualizations, and a Gradio demo app.

- **Language:** Python 3
- **Concepts:** NLP, Transfer Learning, Transformers, LLM, Text Classification
- **Models:** BanglaBERT, XLM-RoBERTa, Groq LLM
- **Directory:** `BanglaProfanityDetection/`

## Getting Started

### Q1 - Python
```bash
cd Q1_Employee
python employee.py
```

### Q2 - C# Text Formatter
```bash
cd Q2_TextFormatter
dotnet run
```

### Q3 - C# Student DB
```bash
cd Q3_StudentDB
dotnet run
```

### Bangla Profanity Detection
```bash
cd BanglaProfanityDetection
pip install -r requirements.txt
jupyter notebook notebooks/
```
