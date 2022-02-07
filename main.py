from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from models import (
    RegistrationDetails,
    LoginDetails,
    check_if_user_exists,
    create_user,
    get_user,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to InsuranceHive"}


@app.post("/register")
async def register(registration_details: RegistrationDetails):
    user_exists = check_if_user_exists(registration_details)
    if user_exists:
        return {"message": "Account already exists"}
    user = create_user(registration_details)
    return user


@app.post("/login")
async def login(login_details: LoginDetails):
    user = get_user(login_details)
    if not user:
        return {"error": "User does not exist."}
    return user
