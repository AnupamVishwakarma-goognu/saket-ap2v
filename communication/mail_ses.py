def send_mail_ses(rec_email=None,message_body=None,header1=None, header2_line=None):
    import smtplib  
    import email.utils
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    print("----> Mail Sending to : ")
    print(rec_email)

    # Replace sender@example.com with your "From" address. 
    # This address must be verified.
    SENDER = 'no-reply@ap2v.com'  
    # SENDERNAME = 'AP2V alerts'                  #H1
    SENDERNAME = header1                          #H1

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT  = str(rec_email)

    # Replace smtp_username with your Amazon SES SMTP user name.
    USERNAME_SMTP = "AKIA46T2GUX5BX4XY7PA"

    # Replace smtp_password with your Amazon SES SMTP password.
    PASSWORD_SMTP = "BE/5YahtLR/QYxwvegc3dxqaQwKymQzCXqUwE/8QGmN6"

    # (Optional) the name of a configuration set to use for this message.
    # If you comment out this line, you also need to remove or comment out
    # the "X-SES-CONFIGURATION-SET:" header below.
    #CONFIGURATION_SET = "ConfigSet"

    # If you're using Amazon SES in an AWS Region other than US West (Oregon), 
    # replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP  
    # endpoint in the appropriate region.
    HOST = "email-smtp.ap-south-1.amazonaws.com"
    PORT = 587

    # The subject line of the email.
    # SUBJECT = 'AP2V Test alert mail'            #H2
    SUBJECT = header2_line                        #H2

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test\r\n"
                "This email was sent through the Amazon SES SMTP "
                "Interface using the Python smtplib package."
                )

    # The HTML body of the email.
    BODY_HTML = message_body

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['To'] = RECIPIENT
    # Comment or delete the next line if you are not using a configuration set
    #msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(BODY_TEXT, 'plain')
    part2 = MIMEText(BODY_HTML, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Try to send the message.
    try:  
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        #stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        print ("Error: ", e)
        return 0,e
    else:
        print ("Email sent!")
        e=None
        return 1,e