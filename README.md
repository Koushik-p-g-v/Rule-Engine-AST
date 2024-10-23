# Rule Engine Application with AST

This project is a simple 3-tier Rule Engine Application designed to determine user eligibility based on attributes such as age, salary, department, etc., using an Abstract Syntax Tree (AST). The application allows users to create, combine, evaluate, modify, and delete rules. 

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLAlchemy (SQLite)
- **Frontend:** HTML, CSS (Bootstrap), JavaScript

## Key Features

1. **Rule Creation:** 
   - Users can create new rules, whether simple or complex. 
   - Rules are stored in the database for future use.

2. **Combining Rules:** 
   - Users can combine multiple rules using the `AND` operator. 
   - Combination can be done using existing rules, new rules, or a combination of both. 
   - Combined rules are saved in the database.

3. **Evaluating Rule:** 
   - Users can evaluate rules from the database or define one-time-use rules.
   - Rule evaluation is based on user-provided attribute values in JSON format.

4. **Modifying Rule:** 
   - Users can modify existing rules if there are any mistakes or updates required.
   - Modifications are reflected in the database.

5. **Deleting Rule:** 
   - Users can delete single or multiple rules that are no longer needed.

6. **Displaying Rules:** 
   - All the rules that are in the database are displayed as a table.

## Product Design

### 1. User Interface (UI)
- **HTML:** Used for structuring the webpage.
- **CSS (Bootstrap):** Provides a simple, responsive, and visually appealing design.
- **JavaScript:** Implements the functionality of buttons and interactions on the webpage.

### 2. Backend
- **Flask (Python):** A lightweight web framework for building the backend.
- **Abstract Syntax Tree (AST):** Represents rules as tree structures, where operators (e.g., `AND`, `OR`, `>`) act as nodes, and attributes (e.g., age, salary) act as operands or leaves.

### 3. Database
- **SQLAlchemy (SQLite):** Manages database interactions and handles rule storage, modification, and deletion. 

## How It Works

1. **Rule Creation:** 
   - Users enter rule definitions (e.g., `age > 30 AND salary > 50000`).
   - The rules are stored as nodes (operators) and leaves (operands) in an Abstract Syntax Tree (AST).
   
2. **Combining Rules:** 
   - Multiple rules can be combined using logical operators such as `AND`.
   
3. **Rule Evaluation:**
   - Users can input a JSON object that provides values for the rule's attributes. 
   - The system evaluates the rule based on these values and determines if the user meets the rule criteria.

4. **Modify and Delete Rules:** 
   - Users can modify rules if needed and save the changes.
   - Unwanted rules can be removed from the database.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Koushik-p-g-v/Rule-Engine-AST.git
2. Navigate into project repository:
   ```bash
   cd Rule-Engine-AST
3. Create and Activate a virtual environment:
   ```bash
   python3 -m venv venv
   venv\Scripts\activate
4. Install Dependencies:
   ```bash
   pip install -r requirements.txt
5. Run the Application:
   ```bash
   python app.py
6. Open a browser and navigate to `http://127.0.0.1:5000` to use the Rule Engine Application.

## Database Setup
This application uses SQLite as its database. SQLAlchemy handles the interactions with the database. The database schema is created automatically upon running the application.

