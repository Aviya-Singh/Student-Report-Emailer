# Student Report Emailer

This Python project automates the process of generating and sending student report emails. It reads student data from a JSON file, consolidates reports, and sends formatted HTML emails to students.

## Features

* **JSON Data Input:** Reads student information from a `studentReports.json` file.
* **Report Consolidation:** Handles students with multiple courses by consolidating their course information into a single email report.
* **HTML Email Generation:**
    * Generates styled HTML emails based on an `email_template.html` file.
    * Uses inline CSS for maximum compatibility with various email clients.
    * Formats the email content to display course information in a structured table.
* **Email Delivery:** Sends emails using SMTP, configurable via `config.json`.
* **Logging:** Provides logging for successful and failed email sends.
* **Consistent Table Formatting:** Ensures the first column of the course information tables has a fixed width for consistent alignment.

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
                "courses": [
                    {
                        "Major": "Student Major",
                        "Course": "Course Name",
                        "Enrollment Date": "Enrollment Date",
                        "Grades": {
                            "Midterm1": 90,
                            "Midterm2": 85,
                            "FinalExam": 95
                        }
                    },
                    // ... more courses for this student (if any)
                ]
            }
        },
        // ... more student entries
    ]
    ```

    **Important:**

    * The `courses` key now holds a *list* of course dictionaries.
    * If a student has only one course, it will still be a list containing a single course dictionary.

4.  **Create `email_template.html`:**

    Create an `email_template.html` file in the project's root directory. This file defines the structure and styling of the email. Make sure it includes the `{student_name}` and `{courses_tables}` placeholders.

    Example:

    ```html
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </head>
    <body style="font-family: Arial, sans-serif; font-size: 16px; margin: 0; padding: 20px; background-color: #f9f9f9;">
        <div style="margin: 0 auto; padding: 20px; width: 80%; background-color: #f9f9f9; border: 1px solid #ccc; border-radius: 5px;">
            <h1 style="font-family: Arial, sans-serif; font-size: 20px; font-weight: bold; text-align: left;">Hi {student_name},</h1>
            <p style="font-family: Arial, sans-serif; font-size: 16px; color: #333333; text-align: left;">Here is the student report for you:</p>
            {courses_tables}
            <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333333;">Thanks,<br>Aviya Singh</p>
        </div>
    </body>
    </html>
    ```

    **Note:** This template uses inline styles for better email client compatibility.

5.  **Run the Script:**

    ```bash
    python student_report_processor.py
    ```

## Usage

Run the `student_report_processor.py` script to send student report emails. The script will process the `studentReports.json` file, format the data into HTML emails using `email_template.html`, and send the emails using the SMTP settings from `config.json`.

## Important Notes

* Ensure your email account allows less secure app access or generate an app password if using Gmail.
* Email rendering can be inconsistent across different email clients. It is crucial to test the generated emails in various email clients (e.g., Gmail, Outlook, Yahoo Mail) to ensure they display correctly.
* The script prioritizes inline CSS for maximum email client compatibility.

## Contributing

Feel free to contribute to this project by submitting pull requests.

## License

[Your License (e.g., MIT)]