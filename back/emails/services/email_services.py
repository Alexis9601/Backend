from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_otp_email(mail_data, template):
    html_body = render_to_string(template, mail_data)
    email = EmailMultiAlternatives(
        subject='{otp} es tu código de TravesIA'.format(otp = mail_data["otp"]),
        body="",
        from_email='travesia@gmail.com',
        to=[mail_data["email"]],
    )
    email.attach_alternative(html_body, "text/html")
    email.send()