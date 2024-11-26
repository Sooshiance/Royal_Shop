from .models import User, OTP, Profile


class UserRepository:
    @staticmethod
    def create_user(**kwargs):
        return User.objects.create_user(**kwargs)

    @staticmethod
    def get_user_by_username(username):
        return User.objects.get(username=username)

    @staticmethod
    def get_user_by_id(user_id):
        return User.objects.get(uid=user_id)


class OTPRepository:
    @staticmethod
    def create_otp(user, otp):
        return OTP.objects.create(user=user, otp=otp)

    @staticmethod
    def get_otp(user, otp):
        return OTP.objects.filter(user=user, otp=otp).first()


class PasswordResetTokenRepository:
    @staticmethod
    def create_token(user, token, expires_at):
        return OTP.objects.create(user=user, otp=token, expires_at=expires_at)

    @staticmethod
    def get_token(token):
        return OTP.objects.filter(otp=token).first()
