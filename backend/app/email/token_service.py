import hashlib
import secrets


class TokenService:

    @staticmethod
    def generate_token():
        raw_token = secrets.token_urlsafe(32)

        token_hash = hashlib.sha256(
            raw_token.encode()
        ).hexdigest()

        return raw_token, token_hash

    @staticmethod
    def hash_token(
        token: str,
    ) -> str:
        return hashlib.sha256(
            token.encode()
        ).hexdigest()