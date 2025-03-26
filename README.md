# Student Report Emailer

This Python project automates the process of generating and sending student report emails. It reads student data from a JSON file, consolidates reports for students with multiple courses, and sends formatted HTML emails containing student grades. Temporary HTML files are generated for each email and deleted after successful delivery.

## Features

* **JSON Data Input:** Reads student information from a `studentReports.json` file.
* **Report Consolidation:** Handles duplicate student entries by consolidating course information into a single report.
* **HTML Email Generation:** Creates well-formatted HTML emails with student details and grades.
* **Email Delivery:** Sends emails using SMTP, configurable via `config.json`.
* **Temporary File Handling:** Generates and deletes temporary HTML files for each email.
* **Logging:** Provides logging for successful and failed email sends.

## Prerequisites

* Python 3.x
* SMTP server credentials (for sending emails)

## Setup

1.  **Clone the Repository:**

    ```bash
    git clone [your-repository-url]
    cd [your-repository-directory]
    ```

2.  **Create `config.json`:**

    Create a `config.json` file in the project's root directory with your SMTP server details:

    ```json
    {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 465,
        "sender_email": "your_email@gmail.com",
        "sender_password": "your_password"
    }
    ```

    **Note:** Replace `"your_email@gmail.com"` and `"your_password"` with your actual email credentials.

3.  **Prepare `studentReports.json`:**

    Create a `studentReports.json` file with student data in the following format:

    ```json
    [
        {
            "[email address removed]": {
                "displayName": "Student Name",
                "Major": "Student Major",
                "Course": "Course Name",
                "Enrollment Date": "Enrollment Date",
                "Grades": {
                    "Midterm1": 90,
                    "Midterm2": 85,
                    "FinalExam": 95
                }
            }
        },
        // ... more student entries
    ]
    ```

4.  **Run the Script:**

    ```bash
    python student_report_processor.py
    ```

## Usage

Run the `student_report_processor.py` script to send student report emails.

## Contributing

Feel free to contribute to this project by submitting pull requests.

## License

[Your License (e.g., MIT)]