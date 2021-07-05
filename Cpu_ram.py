import paramiko
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


hostname = "10.0.2.15"
username = "supriya"
commands = [
    "hostnamectl",
    "top -b -n1 | grep 'Cpu(s)' | awk '{print $2 + $4}' ",
    "free | grep Men | awk '{print $4/$2 * 100.0}'"
]

client = paramiko.SSHClient()

client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(hostname=hostname, username=username)
except:
    print("*[!] cannot connect to the SSH server")
    exit()

ls = []
for command in commands:
    print("="*50, command, "="*50)
    stdin, stdout, stderr = client.exec_command(command)
    ls (stdout.read().decode())
    print(ls)
    err = stderr.read().decode()
    if err:
        print(err)

fieldsnames=["VM name","IpAddress", "Cpu_usage","Ram usage","Time Stamp"]

lst1=lst[1].split("\n")
lst2=lst[2].split("\n")
print(lst[1])
with open("output.csv","w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(fieldnames)
    csvwriter.writerow([username,hostname,lst1[0],lst2[0]])
emailfrom = "supriyachowdary32@gmail.com"
emailto = "saisandeep29@gail.com"
fileTosend = "output.csv"

message = MIMEMultipart()
message["From"] = emailfrom
message["To"] = emailto
message["Subject"] = "A test mail is sender to receiver"

ctype, encoding = mimetypes.guess_type(fileToSend)
if ctype is None or encoding is not None:
    ctype = "application/octet-stream"

maintype, subtype = ctype.split("/", 1)
if maintype == "text":
    fp = open(fileToSend)
    # Note: we should handle calculating the charset
    attachment = MIMEText(fp.read(), _subtype=subtype)
    fp.close()
elif maintype == "image":
    fp = open(fileToSend, "rb")
    attachment = MIMEImage(fp.read(), _subtype=subtype)
    fp.close()
elif maintype == "audio":
    fp = open(fileToSend, "rb")
    attachment = MIMEAudio(fp.read(), _subtype=subtype)
    fp.close()
else:
    fp = open(fileToSend, "rb")
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)
attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)

message.attach(attachment)

server = smtplib.SMTP("smtp.gmail.com:587")
server.starttls()
server.login(username,password)
server.sendmail(emailfrom, emailto, msg.as_string())
server.quit()
