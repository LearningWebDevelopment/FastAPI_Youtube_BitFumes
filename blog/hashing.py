from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():

    def hash_pass(password: str):
        return pwd_context.hash(password)

    def verify(hashed_pass, plain_pass):
        return pwd_context.verify(plain_pass, hashed_pass)
