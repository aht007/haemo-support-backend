"""
Utils module to generate token for setting password
"""

from django.contrib.auth.tokens import PasswordResetTokenGenerator


class PasswordResetToken(PasswordResetTokenGenerator):
    """
    class for generating token
    """

    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp)
        )


password_reset_token = PasswordResetToken()
