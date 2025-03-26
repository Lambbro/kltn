import jwt
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import OAuthFlowPassword
from fastapi.security import OAuth2

from database import SECRET_KEY, ALGORITHM

class OAuth2PasswordRequestEmail(OAuth2):
    def __init__(self, tokenUrl: str):
        flows = OAuthFlowsModel(password=OAuthFlowPassword(tokenUrl=tokenUrl))
        super().__init__(flows=flows)

oauth2_scheme = OAuth2PasswordRequestEmail(tokenUrl="dang-nhap")

def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không được cung cấp",
        )

    token = token.split("Bearer ")[1] if "Bearer " in token else token

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        print(f"Token nhận được: {token}")  # Debug
        print(f"Payload sau khi decode: {payload}")  # Debug

        email: str = payload.get("sub")
        quyen_han: str = payload.get("quyen_han")

        if email is None or quyen_han is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token không hợp lệ",
            )

        return {"email": email, "quyen_han": quyen_han}

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token đã hết hạn")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token không hợp lệ")
def check_permission(current_user: dict, required_permission: int):
    user_role = current_user.get("quyen_han")

    # Kiểm tra nếu quyền không hợp lệ
    if not isinstance(user_role, int) or user_role < 1 or user_role > 4:
        raise HTTPException(status_code=403, detail="Quyền không hợp lệ.")

    # Kiểm tra nếu quyền không chính xác
    if user_role != required_permission:
        raise HTTPException(status_code=403, detail="Bạn không có quyền truy cập.")

def check_higher_permission(current_user: dict, required_permission: int):
    user_role = current_user.get("quyen_han")

    # Kiểm tra nếu quyền không hợp lệ
    if not isinstance(user_role, int) or user_role < 1 or user_role > 4:
        raise HTTPException(status_code=403, detail="Quyền không hợp lệ.")

    # Kiểm tra nếu quyền không đủ
    if user_role > required_permission:
        raise HTTPException(status_code=403, detail="Bạn không có quyền thực hiện thao tác này.")
