from jinja2 import Template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import xlsxwriter # type: ignore
import os
import datetime
from math import ceil


def get_week_of_month(dt):
    first_day = dt.replace(day=1)
    dom = dt.day
    adjusted_dom = dom + first_day.weekday()
    return int(ceil(adjusted_dom/7.0))

# remapped weekday number to match that of Groovy in Resolve
def remap_weekday(weekday):
    if weekday == 6:  # Sunday
        return 1
    elif weekday == 0:  # Monday
        return 2
    elif weekday == 1:  # Tuesday
        return 3
    elif weekday == 2:  # Wednesday
        return 4
    elif weekday == 3:  # Thursday
        return 5
    elif weekday == 4:  # Friday
        return 6
    elif weekday == 5:  # Saturday
        return 7
    else:
        return None

def emailReport(sitesStatus, sessionDate):

    now = datetime.datetime.now()

    # Define email server and credentials
    smtpServer = os.environ.get('SMTP_SERVER')
    smtpPort = os.environ.get('SMTP_PORT')
    senderEmail = os.environ.get('MAILER_EMAIL')
    senderPassword = os.environ.get('MAILER_PWD')

    emailRecipients = os.environ.get('EMAIL_TO')

    # Set up email server
    server = smtplib.SMTP(smtpServer, smtpPort)
    server.starttls()
    server.login(senderEmail, senderPassword)

    # Read the email template
    with open("template.html", "r") as file:
        template_str = file.read()

    emailContent = jinjaTemplate.render(sitesStatus)

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = senderEmail
    msg["To"] = emailRecipients


    weekday = remap_weekday(now.weekday())

    weekDays = {
        "1" : "Sunday",
        "7" : "Saturday"
    }

    msg["Subject"] = weekDays[weekday] + " "  + "GTD5 Customer Count Process Result (" + sessionDate  + ")"

    # Attach the HTML content to the email
    msg.attach(MIMEText(emailContent, "html"))

    # Print and send the email
    # print(f"Sending email to {emailRecipients}:\n{email_content}\n\n")

    server.sendmail(senderEmail, emailRecipients, msg.as_string())

    server.quit()


def generatedExcelFile(result, sessionDate):
    workbook = xlsxwriter.Workbook("output/CustomerCount_DataSheet_" + sessionDate + ".xlsx")
    worksheet = workbook.add_worksheet()

    # generate xls file    
    row = 0
    for key in result:
        [fileName, stringTcu, darkCount] = key.split("_")

        count = result[key]

        worksheet.write(row, 0, fileName)
        worksheet.write(row, 1, stringTcu)
        worksheet.write(row, 2, darkCount)
        worksheet.write(row, 3, count)
        worksheet.write(row, 4, sessionDate)
        row += 1

    workbook.close()


def getDayAndWeek(now):
    weekday = remap_weekday(now.weekday())

    w = get_week_of_month(now)

    if weekday == 6:  # if the day is sunday
        w = get_week_of_month(now) - 1

    if w == 0:
        w = w + 1

    return [weekday, w]


def find_files_created_days_ago(directory, days_ago, recursive=False):
    """
    Find all files in the specified directory that were created exactly X days ago.
    
    Args:
        directory (str): The directory to search in
        days_ago (int): Number of days ago to check for
        recursive (bool): Whether to search recursively through subdirectories
    
    Returns:
        list: List of file paths created X days ago
    """
    # Calculate the target date (current date minus days_ago)
    target_date = datetime.datetime.now().date() - datetime.timedelta(days=days_ago)
    
    # Start and end of the target day
    start_of_day = datetime.datetime.combine(target_date, datetime.time.min)
    end_of_day = datetime.datetime.combine(target_date, datetime.time.max)
    
    matching_files = []
    
    # Determine which files to scan
    if recursive:
        # Walk through all subdirectories
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if check_file_creation_date(file_path, start_of_day, end_of_day):
                    matching_files.append(file_path)
    else:
        # Only scan files in the specified directory
        for item in os.listdir(directory):
            file_path = os.path.join(directory, item)
            if os.path.isfile(file_path) and check_file_creation_date(file_path, start_of_day, end_of_day):
                matching_files.append(file_path)
    
    return matching_files

def check_file_creation_date(file_path, start_of_day, end_of_day):
    """
    Check if a file was created between the start and end of the target day.
    
    Args:
        file_path (str): Path to the file
        start_of_day (datetime): Start of the target day
        end_of_day (datetime): End of the target day
    
    Returns:
        bool: True if the file was created on the target day, False otherwise
    """
    try:
        # Get file creation time (ctime on Windows, birthtime on some Unix systems)
        # Note: On some Unix systems, this might return the metadata change time instead
        creation_time = os.path.getctime(file_path)
        creation_datetime = datetime.datetime.fromtimestamp(creation_time)
        
        # Check if the creation time is within the target day
        return start_of_day <= creation_datetime <= end_of_day
    except Exception as e:
        print(f"Error checking file {file_path}: {e}")
        return False