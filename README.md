# 🧠 Task Analyzer
A smart, local habit tracker and analyzer built with Python and pandas.

---

## 📘 Overview
**Task Analyzer** helps users log, track, and analyze tasks to understand habits, improve consistency, and manage productivity.  
It’s entirely local — no online sync — designed around modular OOP structure and deep task-level analytics.

---

## ⚙️ Features

### 🔐 User Management
- Create, login, or delete accounts (stored securely in `users.csv`)
- Change username or password
- Each user’s tasks are stored independently in their own JSON file

---

### ✅ Task Control
- **Add Task:** Create tasks with name, type, importance, start date/time, deadline, and optional notes.  
- **Edit Task:** Modify any field, mark completion (with timestamp or current time), or flag as an outlier (excluded from analytics).  
- **Delete Task:** Permanently remove tasks from the database.

---

### 👀 Task Viewing
- **Quick View Tasks:**  
  Instantly view all or specific tasks (by ID).  
  Tasks are auto-sorted (completed → ongoing first, deadlines ascending).  
  Can export the viewed data to JSON.
  
- **Detailed View Tasks:**  
  Allows advanced filtering and sorting.  
  Users can filter by task type, importance, or completion status (e.g., completed, late, ongoing, outliers).  
  Customizable primary and secondary sorting fields (type, importance, start, deadline, etc.) with ascending/descending options.  
  Exportable to JSON for external analysis.

---

### 📊 Task Analytics
- **Analyse Tasks:**  
  Choose one or multiple task types/importances for focused analytics.  
  Displays:
  - Total tasks and completed counts  
  - On-time and late completion rates  
  - Average and expected durations  
  - Average delay and early completion  
  - Consistency via standard deviation of completion times  
  - Cross-category counts for comparative insight  
  Exportable to JSON for recordkeeping.
  
- **Detailed Analyse Tasks:**  
  Automatically performs the above analytics for **all** task type–importance combinations.  
  Provides a broader performance summary across all activity types.  
  Also exportable to JSON.

---

## 📂 Project Structure
```

task-analyzer/
│
├── src/
│   ├── main.py
│   ├── login.py
│   ├── tasks.py
│   ├── analyse.py
│   └── utils.py
│
└── database/
├── users.csv
├── alex_walker.json
├── hayden_parker.json
├── jordan_lee.json
├── morgan_kent.json
└── riley_cooper.json

```

---

## 🧰 Tech Stack
- **Language:** Python 3.x  
- **Libraries:** pandas, datetime, json  
- **Design:** Modular OOP architecture for maintainability and clarity  

---

## 🚀 Usage
```

git clone https://github.com/manvikgoyal01/task-analyzer.git
cd task-analyzer
python src/main.py

```

Login or create a new user when prompted.  
Follow the on-screen options to add, edit, view, and analyze your tasks.

---

## 📈 Key Metrics
- Average & expected task duration  
- On-time rate  
- Late vs early completion  
- Average delay / early time  
- Consistency (standard deviation)  
- Category and count breakdown  
```
