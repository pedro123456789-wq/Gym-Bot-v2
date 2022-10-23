import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendEmail(dest, subj, body):
    #html code
    html = f'''
    <!DOCTYPE html>
    <html>
       <body style = 'background:white'>
            <h1 style = 'text-align: center; font-family: Verdana; color: #0e0e87'>Gym Bot</h1>
            <h4 style = 'text-align: center; font-family: Verdana; color: #0e0e87'>Your AI Personal Trainer</h4>
            <p style = 'text-align: center; font-family: Verdana; color: black; margin-top: 6vh'>{body}</p>
            <p style = 'text-align: center; font-family: Verdana; color: black; margin-top: 2vh'>Thank you for signing up, verify your email and start your journey</p>
            <h4 style = 'text-align: center; font-family: Verdana; color: #0e0e87; margin-top: 4vh'>The Gym Bot team</h4>
        </body>
    </html>
    '''
    
    senderEmail = 'pl156176@gmail.com'
    password = 'ltmmiwsaowrxbhjk'
    
    # Create a multipart email form and define the values for the from, to and subject fields.
    message = MIMEMultipart()
    message['From'] = senderEmail
    message['To'] = dest
    message['Subject'] = subj

    #attach html to email form
    message.attach(MIMEText(html, "html"))
    emailString = message.as_string()

    # connect to gmail server and send email 
    context = ssl.create_default_context() 
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(senderEmail, password)
        server.sendmail(senderEmail, dest, emailString)
        
    
if __name__ == '__main__':
    sendEmail('pl156176@gmail.com', 'Confirmation code', 'Your code is 12345')