import aiosmtplib
from email.message import EmailMessage


class Mailer:
    @staticmethod
    async def send(code: int, email: str) -> None:
        msg = EmailMessage()
        msg["From"] = "andrijlupov@gmail.com"
        msg["To"] = email
        msg["Subject"] = ""
        msg.set_content("Your code is {}".format(code))
        await aiosmtplib.send(msg, hostname="smtp.gmail.com", port=465,
                              username="andrijlupov@gmail.com",
                              password="postgres",
                              use_tls=True)
