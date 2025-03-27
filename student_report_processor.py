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
        Create HTML content for email body using email_template.html.
        """
        # Read the HTML template from file
        with open('email_template.html', 'r') as template_file:
            html_template = template_file.read()

        course_table_template = """
            <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                <tr>
                    <td style="font-family: Arial, sans-serif; font-size: 16px; padding: 10px; border: 1px solid #005ccc; text-align: left; background-color: #4887dd; color: #fff; width: 150px;">Course:</td>
                    <td style="font-family: Arial, sans-serif; font-size: 16px; padding: 10px; border: 1px solid #005ccc; text-align: left; background-color: #f0f0f0;">{course_name}</td>
                </tr>
                <tr>
                    <td style="font-family: Arial, sans-serif; font-size: 16px; padding: 10px; border: 1px solid #005ccc; text-align: left; background-color: #4887dd; color: #fff; width: 150px;">Major:</td>
                    <td style="font-family: Arial, sans-serif; font-size: 16px; padding: 10px; border: 1px solid #005ccc; text-align: left; background-color: #f0f0f0;">{major}</td>
                </tr>
                <tr>
                    <td style="font-family: Arial, sans-serif; font-size: 16px; padding: 10px; border: 1px solid #005ccc; text-align: left; background-color: #4887dd; color: #fff; width: 150px;">Enrollment Date:</td>
                    <td style="font-family: Arial, sans-serif; font-size: 16px; padding: 10px; border: 1px solid #005ccc; text-align: left; background-color: #f0f0f0;">{enrollment_date}</td>
                </tr>
                <tr>
                    <td style="font-family: Arial, sans-serif; font-size: 16px; padding: 10px; border: 1px solid #005ccc; text-align: left; background-color: #4887dd; color: #fff; width: 150px;">Grades:</td>
                    <td style="font-family: Arial, sans-serif; font-size: 16px; padding: 10px; border: 1px solid #005ccc; text-align: left; background-color: #f0f0f0;">{grades}</td>
                </tr>
            </table>
        """

        courses_tables = ""

        for course in student_data.get('courses', [student_data]):
            grades_str = "<br>".join([f"{key} : {value}" for key, value in course['Grades'].items()])
            courses_tables += course_table_template.format(
                course_name=course['Course'],
                major=course['Major'],
                enrollment_date=course['Enrollment Date'],
                grades=grades_str
            )

        html_content = html_template.format(student_name=student_data['displayName'], courses_tables=courses_tables)
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
        Send emails with HTML reports to each student using template.
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
                # Generate HTML content using template
                html_content = self.generate_email_html(student_data)

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

            except Exception as e:
                logging.error(f"Failed to send email to {email}. Error: {str(e)}")

def main():
    # Create email sender and send reports
    email_sender = StudentReportEmailSender()
    email_sender.send_report_emails()

if __name__ == "__main__":
    main()