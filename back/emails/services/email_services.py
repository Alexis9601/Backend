from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_otp_email(mail_data):
    html_body = render_to_string("template.html", mail_data)
    email = EmailMultiAlternatives(
        subject='{otp} es tu código de AppName'.format(otp = mail_data["otp"]),
        body="",
        from_email='hello@trial-x2p03476qn7gzdrn.mlsender.net',
        to=[mail_data["email"]],
    )
    email.attach_alternative(html_body, "text/html")
    email.send()