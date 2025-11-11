```markdown
# 🧠 Task Analyzer
A smart, local habit tracker and analyzer built with Python and pandas.

---

## 📘 Overview
**Task Analyzer** helps users log, track, and analyze tasks to improve consistency and productivity.  
It’s fully local — no AI or online sync — focusing on clean structure, OOP design, and data-driven analysis.

---

## ⚙️ Features

### 🔐 User Management
- Create, login, or delete accounts (stored in `users.csv`)
- Change username or password

### ✅ Task Control
- Add, edit, or delete tasks
- Mark completion, track on-time or delayed finish
- Tag importance, type, notes, and outliers
- Each user has a separate JSON file

### 👀 Viewing & Exporting
- **Quick View:** View all or a specific task (sorted); exportable to JSON
- **Detailed View:** Filter by type, importance, or status; multi-level sorting; exportable to JSON

### 📊 Analytics
- **Analyse:** For selected task types/importances → totals, delays, on-time %, averages, and standard deviation
- **Detailed Analyse:** Runs full analysis for all type + importance combinations
- Both exportable to JSON

---

## 📂 Project Structure
```

task-analyzer/
│
├── src/
│   ├── main.py        # Main program & logic
│   ├── login.py       # User management
│   ├── tasks.py       # Task operations
│   ├── analyse.py     # Data analysis
│   └── utils.py       # Helper utilities
│
└── database/
├── users.csv
├── alex_walker.json
├── hayden_parker.json
├── jordan_lee.json
├── morgan_kent.json
└── riley_cooper.json

````

---

## 🧰 Tech Stack
- **Language:** Python 3.x  
- **Libraries:** pandas, datetime, json  
- **Design:** Modular OOP structure

---

## 🚀 Usage
1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/task-analyzer.git
   cd task-analyzer
````

2. Run the main program:

   ```bash
   python src/main.py
   ```

3. Log in with an existing user or create a new one.

**Sample Credentials**

```
alex_walker, alex123
hayden_parker, hayden123
jordan_lee, jordan123
riley_cooper, riley123
morgan_kent, morgan123
```

---

## 📈 Key Metrics

* Average & expected task duration
* On-time rate
* Late vs early completion
* Average delay / early time
* Consistency (standard deviation)
* Category and count breakdown

```
```
