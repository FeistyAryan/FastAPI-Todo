from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session
from app.services.auth_service import auth_service
from app.api.v1.dependencies import get_valid_session_model_from_refresh_token
from app.models.session import Session as SessionModel
from app.schemas.token import Token

router = APIRouter()

@router.post("/login",
response_model=Token
)
async def login_for_access_token(
    response: Response,
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]= None
):
    access_token, refresh_token = await auth_service.login(session=session, request=request, email=form_data.username, password=form_data.password)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=False,
        samesite="lax",
        secure=False
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh",
response_model=Token
)
async def refresh_access_token(
    response: Response,
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_session: Annotated[SessionModel, Depends(get_valid_session_model_from_refresh_token)]
):
    access_token, new_refresh_token = await auth_service.refresh(session=session, request=request, old_session=current_session)

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=False,
        samesite="lax",
        secure=False
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(
    response: Response,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_session: Annotated[AsyncSession, Depends(get_valid_session_model_from_refresh_token)]
):
    await auth_service.logout(session=session, session_to_delete=current_session)
    response.delete_cookie(key="refresh_token")
    return Response(status_code=204)