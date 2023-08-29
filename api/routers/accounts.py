from fastapi import (
    Body,
    status,
    Depends,
    Request,
    Response,
    APIRouter,
    HTTPException,
)

from utils.authenticator import authenticator
from models.accounts import (
    Account,
    AccountAll,
    AccountOut,
    AccountForm,
    AccountToken,
    AccountUpdate,
    DuplicateAccountError,
)
from uuid import UUID
from typing import List
from bson import ObjectId
from clients.client import db
from models.apis import HttpError
from repositories.accounts import AccountRepo
from utils.authenticator import authenticator

router = APIRouter()


@router.get("/token", response_model=AccountToken | None)
async def get_token(
    request: Request,
    account: AccountOut = Depends(authenticator.try_get_current_account_data),
) -> AccountToken | None:
    if account and authenticator.cookie_name in request.cookies:
        return {
            "access_token": request.cookies[authenticator.cookie_name],
            "type": "Bearer",
            "account": account,
        }


# AUTH clause. Use this function when ready
# @router.get("/token", response_model=AccountToken | None)
# async def get_token(
#     request: Request,
#     account: AccountOut = Depends(authenticator.try_get_current_account_data),
# ) -> AccountToken | None:
#     print("request is:", request)
#     if not account:
#          raise HTTPException(status_code=404, detail="Account not found")
#     elif authenticator.cookie_name not in request.cookies:
#         raise HTTPException(
#             status_code=400, detail="Required cookie not found"
#         )
#     elif authenticator.cookie_name in request.cookies:
#         return {
#             "access_token": request.cookies[authenticator.cookie_name],
#             "type": "Bearer",
#         }


@router.post("/api/accounts", response_model=AccountToken | HttpError)
async def create_account(
    info: Account,
    request: Request,
    response: Response,
    repo: AccountRepo = Depends(),
):
    hashed_password = authenticator.hash_password(info.password)
    try:
        account = repo.create(info, hashed_password)
    except DuplicateAccountError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create an account with those credentials",
        )
    form = AccountForm(username=info.username, password=info.password)
    token = await authenticator.login(response, request, form, repo)
    return AccountToken(account=account, **token.dict())


@router.put(
    "/updateByEmail",
    response_description="Update an account",
    response_model=AccountUpdate,
)
def update_account_by_email(
    email: str,  # Take the email as a string parameter
    account: AccountUpdate = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    existing_account = db.accounts.find_one(
        {"email": email}
    )  # Look up account by email
    if not existing_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with email {email} not found",
        )

    account_data = {k: v for k, v in account.dict().items() if v is not None}

    if account_data:
        db.accounts.update_one(
            {"email": email}, {"$set": account_data}
        )  # Update account by email

    return db.accounts.find_one({"email": email})


@router.get(
    "/accounts",
    response_description="Get a list of all accounts",
    response_model=List[
        AccountAll
    ],  # Assuming AccountOut is your output model
)
def get_all_accounts():
    accounts = db.accounts.find()  # This fetches all accounts
    accounts_list = list(
        accounts
    )  # Convert to list since find() returns a cursor
    return accounts_list


@router.get(
    "/accountByEmail",
    response_description="Get an account by email",
    response_model=AccountAll,  # Assuming AccountAll is your output model
)
def get_account_by_email(email: str):  # Changed id to email here
    account = db.accounts.find_one(
        {"email": email}  # Changed to look up by email
    )
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with email {email} not found",
        )
    return account
