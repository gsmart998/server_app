import hashlib
import uuid


class Password:
    """
    Сlass to handle user password.
    """
    def hash_password(password: str) -> str:
        """
        Recive a regular password, returns a hashed one with salt added.
        """
        salt = uuid.uuid4().hex
        return hashlib.sha256(
            salt.encode() + password.encode()).hexdigest() + ':' + salt

    def check_password(hashed_password: str, user_password: str) -> bool:
        """
        Recive a hashed and regular passwords, return True if matches.
        """
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(
            salt.encode() + user_password.encode()).hexdigest()
