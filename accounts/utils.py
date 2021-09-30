"""
Utils module to generate token for setting password
"""

from django.contrib.auth.tokens import PasswordResetTokenGenerator


class PasswordResetToken(PasswordResetTokenGenerator):
    """
    class for generating token
    """

    def _make_hash_value(self, user, timestamp):
        """
        Adding password value as hash to invalidate the token once
        password is set
        """
        return (
            str(user.pk) + str(timestamp) + str(user.password)
        )


password_reset_token = PasswordResetToken()
