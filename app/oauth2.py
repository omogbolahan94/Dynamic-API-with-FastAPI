from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


load_dotenv(override=True)


# the required values to generate token
secret_key = os.getenv("SECRET_KEY")
algorithm = 'HS256'
access_token_expring_date = 20


def create_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=access_token_expring_date)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt



