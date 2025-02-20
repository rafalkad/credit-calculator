# 💼 Credit Manager GUI

A Python-based GUI application for managing credit records. This project allows users to add, update, delete, and calculate various credit-related details using a simple graphical interface.

## ✨ Features

- ➕ Add new credit records
- ✏️ Update existing credit information
- ❌ Delete credit records
- 💸 Calculate monthly installments
- ⚖️ Calculate interest and remaining balance
- 🚫 Handle missed payments

## 💻 Technologies Used

- 🐍 Python
- 🖥️ Tkinter (GUI)
- 🗄️ SQLAlchemy (Database ORM)
- 🏦 PostgreSQL (Database)

## ⚙️ Installation

### 1. 🔄 Clone the repository

```bash
$ git clone https://github.com/yourusername/your-repo.git
$ cd your-repo
```

### 2. 🛠️ Create a virtual environment

```bash
$ python -m venv venv
$ source venv/bin/activate  # On macOS/Linux
$ venv\Scripts\activate  # On Windows
```

### 3. 📚 Install dependencies

```bash
$ pip install -r requirements.txt
```

## ♻️ Generating `requirements.txt`

If you need to regenerate `requirements.txt,` use the following command:

```bash
$ pip freeze > requirements.txt
```

## ⚙️ Configuration

Make sure to update `app_engine.py` with your database connection details:

```
DATABASE_URL = "postgresql://username:password@localhost:5432/database_name"
```

## 🌟 Running the Application

Run the main script:

```bash
$ python main.py
```

## 📁 Database Setup

Ensure you have PostgreSQL installed and running. Create the database before running the application:


```sql
CREATE DATABASE credit_manager;
```

## 📂 Folder Structure

```
|-- controller.py        # Handles user interactions and database logic
|-- credit.py           # Defines Credit model using SQLAlchemy
|-- app_engine.py       # Database connection setup
|-- SQLCredit.py        # Repository implementation for database operations
|-- repositorystrategy.py # Abstract repository strategy
|-- view.py             # GUI implementation using Tkinter
|-- main.py             # Application entry point
|-- requirements.txt    # List of dependencies
```

## 🤝 Contributing

Feel free to fork this repository and submit pull requests. Any contributions to improve the functionality or UI are welcome!

## ⚖️ License

This project is licensed under the MIT License.

## 👤 Author

Rafał 🚀 Passionate Python developer with a keen interest in financial applications. Connect with me on:

🐙 GitHub: rafalkad
✉️ Email: rafalkadlubiak@wp.pl