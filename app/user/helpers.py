import re


EMAIL_PATTERN = r'^\S+@\S+\.\S+$'
PHONE_PATTERN = r'^\+?[0-9]{9,12}[0-9]$'


def get_credential_types(account: str) -> dict:
    """
    This function check if account is username or email or phone.
    And response corresponding result.
    """
    if re.match(EMAIL_PATTERN, account):
        return {"email": account}
    if re.match(PHONE_PATTERN, account):
        return {"phone": account}
    return {"username": account}
