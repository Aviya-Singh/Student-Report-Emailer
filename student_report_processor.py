import json
import logging
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class StudentReportEmailSender:
    def __init__(self, config_path='config.json'):
        """
        Initialize email sender with configuration from config.json
        """
        # Load email configuration
        with open(config_path, 'r') as config_file:
            self.config = json.load(config_file)

        # Load student reports
        with open('studentReports.json', 'r') as reports_file:
            # Load the entire JSON file as a single list
            self.reports = json.load(reports_file)

    def generate_email_html(self, student_data):
        """
        Create HTML content for email body
        """
        # HTML template with inline styles
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
                h1 {{ color: black; font-weight: bold; text-align: center; }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                    white-space: nowrap;
                }}
                th {{
                    background-color: #f2f2f2;
                    color: black;
                    text-transform: uppercase;
                }}
                th:nth-child(1), td:nth-child(1),
                th:nth-child(2), td:nth-child(2),
                th:nth-child(3), td:nth-child(3),
                th:nth-child(4), td:nth-child(4) {{ width: 25%; }}
            </style>
        </head>
        <body>
            <h1>{student_data['displayName']} - Student Report</h1>
            <table>
                <tr>
                    <th>Course</th>
                    <th>Major</th>
                    <th>Enrollment Date</th>
                    <th>Grades</th>
                </tr>
        """

        # Add course details to HTML
        for course in student_data.get('courses', [student_data]):
            # Format grades
            grades_str = "<br>".join([
                f"{key}: {value}" for key, value in course['Grades'].items()
            ])

            html_content += f"""
                <tr>
                    <td>{course['Course']}</td>
                    <td>{course['Major']}</td>
                    <td>{course['Enrollment Date']}</td>
                    <td>{grades_str}</td>
                </tr>
            """

        # Close HTML tags
        html_content += """
            </table>
        </body>
        </html>
        """

        return html_content

    def consolidate_reports(self):
        """
        Consolidate reports by email, keeping unique course information
        """
        consolidated_reports = {}

        for report in self.reports:
            for email, data in report.items():
                if email not in consolidated_reports:
                    consolidated_reports[email] = {
                        'displayName': data['displayName'],
                        'courses': [data]
                    }
                else:
                    # Check if this course is already in the list
                    if not any(existing['Course'] == data['Course'] for existing in consolidated_reports[email]['courses']):
                        consolidated_reports[email]['courses'].append(data)

        return consolidated_reports

    def send_report_emails(self):
        """
        Send emails with HTML reports to each student
        """
        # Email sending configuration
        smtp_server = self.config['smtp_server']
        smtp_port = self.config['smtp_port']
        sender_email = self.config['sender_email']
        sender_password = self.config['sender_password']

        # Consolidate reports
        consolidated_reports = self.consolidate_reports()

        # Iterate through unique emails in the reports
        for email, student_data in consolidated_reports.items():
            try:
                # Generate HTML content
                html_content = self.generate_email_html(student_data)

                # Create a unique filename
                filename = f"{student_data['displayName'].replace(' ', '_')}_report.html"

                # Save HTML to file
                with open(filename, 'w') as f:
                    f.write(html_content)

                # Create multipart message
                message = MIMEMultipart('alternative')
                message['From'] = sender_email
                message['To'] = email
                message['Subject'] = f"{student_data['displayName']} | Student Report"

                # Attach HTML content
                html_part = MIMEText(html_content, 'html')
                message.attach(html_part)

                # Send email
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(sender_email, sender_password)
                    server.send_message(message)

                logging.info(f"Email sent successfully to {email}")

                # Delete HTML file
                os.remove(filename)
                logging.info(f"Deleted HTML file: {filename}")

            except Exception as e:
                logging.error(f"Failed to send email to {email}. Error: {str(e)}")
                try:
                    os.remove(filename) # attempt to delete file even if email fails.
                    logging.info(f"Deleted HTML file: {filename}")
                except:
                    pass

def main():
    # Create email sender and send reports
    email_sender = StudentReportEmailSender()
    email_sender.send_report_emails()

if __name__ == "__main__":
    main()