import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_reset_email(email_list, fullname, username, pwd):
    sender_email = ""
    sender_password = ""
    sender_name = "Aludecor Customer Connect"

    subject = "Forgot Password Request"
    
    # message_body = f"""Dear {username},

    #                     You have requested a password reset. Click the link below to reset your password:

    #                     [RESET PASSWORD LINK]

    #                     If you did not request this, please ignore this email.

    #                     Best Regards,  
    #                     Your Support Team
    #                 """
    html_content = f"""
                        <div>
                        <div>Dear <strong>{fullname}</strong>,</div>
                        <br />
                        <div>As you requested please find your Login Credentials below:</div>
                        </div>
                        <div>&nbsp;</div>
                        <div>Username: <strong>{username}</strong></div>
                        <div>Password: <strong>{pwd}</strong></div>
                        <div>&nbsp;</div>
                        <div>We strongly recommend changing your password from the <strong>Profile Hub section</strong>.</div>
                        <div><br />
                        <div>If you did not request this, please ignore this email.</div>
                        <br />
                        <div>Best Regards,</div>
                        <div><strong>Team Aludecor</strong></div>
                        </div>
                    """

    # Create MIME message
    msg = MIMEMultipart()
    msg["From"] = f"{sender_name} <{sender_email}>"  # Custom Sender Name
    msg["To"] = ", ".join(email_list)  # Join emails in one request
    msg["Subject"] = subject
    # msg.attach(MIMEText(message_body, "plain"))
    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email_list, msg.as_string())  # Send all emails together
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
