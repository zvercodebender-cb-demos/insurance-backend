import random
from typing import Optional

from decouple import config
from pydantic import BaseModel
from sqlalchemy import String, Column
from sqlmodel import SQLModel, Field, create_engine, Session, select

from enums import ACCOUNT_TYPES, ALL_IN_ONE


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column("username", String, unique=True))
    beta_user: Optional[bool]
    account_type: Optional[str]


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

sql_url = config("DB_STRING", default=sqlite_url)

engine = create_engine(sql_url, echo=True)

SQLModel.metadata.create_all(engine)


class RegistrationDetails(BaseModel):
    username: str
    betaUser: Optional[bool] = False
    accountType: Optional[str] = None


class LoginDetails(BaseModel):
    username: str


def check_if_user_exists(details: RegistrationDetails):
    with Session(engine) as session:
        statement = select(User).where(User.username == details.username)
        results = session.exec(statement)
        user = results.first()
        return bool(user)


def get_user(details: LoginDetails):
    with Session(engine) as session:
        statement = select(User).where(User.username == details.username)
        results = session.exec(statement)
        user = results.first()
        return user


def create_user(details: RegistrationDetails):
    session = Session(engine)
    account_type = random.choice(ACCOUNT_TYPES)
    user = User(
        username=details.username,
        beta_user=details.betaUser,
        account_type=account_type,
    )
    session.add(user)
    session.commit()
    return {
        "username": details.username,
        "betaUser": details.betaUser,
        "accountType": account_type,
    }


def init_users():
    user_1 = RegistrationDetails(
        username="betauser", betaUser=True, accountType=ALL_IN_ONE
    )
    if not check_if_user_exists(user_1):
        create_user(user_1)

    user_2 = RegistrationDetails(
        username="regularuser", betaUser=False, accountType=ALL_IN_ONE
    )
    if not check_if_user_exists(user_2):
        create_user(user_2)


init_users()
