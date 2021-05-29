from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():

    def hash_pass(password: str):
        return pwd_context.hash(password)
