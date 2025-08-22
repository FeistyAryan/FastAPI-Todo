from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_db
from app.services.auth_service import auth_service
from app.api.v1.dependencies import get_valid_session_model_from_refresh_token, oauth2_scheme
from app.models.session import Session as SessionModel
from app.schemas.token import Token

router = APIRouter()

@router.post("/login",
response_model=Token
)
async def login_for_access_token(
    response: Response,
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]= None
):
    access_token, refresh_token = await auth_service.login(db=db, request=request, email=form_data.username, password=form_data.password)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        secure=True
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh",
response_model=Token
)
async def refresh_access_token(
    response: Response,
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_session: Annotated[SessionModel, Depends(get_valid_session_model_from_refresh_token)]
):
    access_token, new_refresh_token = await auth_service.refresh(db=db, request=request, old_session=current_session)

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        samesite="lax",
        secure=True
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_session: Annotated[SessionModel, Depends(get_valid_session_model_from_refresh_token)],
    access_token: Annotated[str, Depends(oauth2_scheme)]
):
    await auth_service.logout(db=db, session_to_delete=current_session, access_token=access_token)
    response.delete_cookie(key="refresh_token", path = "/")
    return Response(status_code=204)