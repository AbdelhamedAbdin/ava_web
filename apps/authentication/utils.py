import string, random
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type



def generate_hex_16_key():
    return ''.join(random.choice(string.ascii_uppercase \
        + string.ascii_lowercase \
            + string.digits) for _ in range(16))


class SendToEmail:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()


class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.pk) + text_type(timestamp)


token_generator = AppTokenGenerator()


# random numbers
def random_text_msg_digit_code_generator():
    digits = '0123456789'
    result = ''
    for i in range(0, 6):
        result += random.choice(digits)
    return result


def unique_text_msg_code_generator(instance):
    new_txt_msg_code = random_text_msg_digit_code_generator()
    Klass = instance.__class__
    print(Klass)
    qs_exists = Klass.objects.filter(code=new_txt_msg_code).exists()

    if qs_exists:
        return unique_text_msg_code_generator(instance)
    return new_txt_msg_code
