import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 465)  # Replace with your SMTP server details
    server.startssl()
    server.login('codynego@gmail.com', 'jqpistshewlexgjq')  # Replace with your email credentials
    server.quit()
    print("SMTP connection successful")
except Exception as e:
    print(f"SMTP connection error: {str(e)}")
