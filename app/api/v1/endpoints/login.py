from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.api.v1.dependencies import get_valid_session_model_from_refresh_token
from app.models.session import Session as SessionModel
from app.schemas.token import Token
from app.crud.user import get_user_by_email
from app.crud.session import delete_session_by_id, create_session
from app.core.config import settings

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
    user = await get_user_by_email(session=session, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    db_session = await create_session(
        session=session,
        user_id=user.id,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host
    )

    access_token = create_access_token(data= {"sub": user.email})
    refresh_token = create_refresh_token(data= {"sub": user.email, "jti": str(db_session.id)})

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite='lax',
        secure=True
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
    await delete_session_by_id(session=session, id=current_session.id)
    new_session = await create_session(
        session=session,
        user_id=current_session.user_id,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host
    )

    access_token = create_access_token(data={"sub": current_session.user.email})
    new_refresh_token = create_refresh_token(data={"sub": current_session.user.email, "jti": str(new_session.id)})

    response.set_cookie(
        key="refresh_token", 
        value=new_refresh_token, 
        httponly=True, 
        samesite="lax", 
        secure=True # Set to False if not using HTTPS in dev
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(
    response: Response,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_session: Annotated[AsyncSession, Depends(get_valid_session_model_from_refresh_token)]
):
    await delete_session_by_id(session=session, id=current_session.id)
    response.delete_cookie(key="refresh_token")

    return {"message": "Logout Successful"}