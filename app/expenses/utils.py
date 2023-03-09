from flask_login import current_user


def send_sms_to() -> str:
    return "+{}".format(current_user.phone)
