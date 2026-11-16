from fastapi import Depends

from app.core.security import verify_token
from uuid import UUID


# def get_current_user(
#     token_data=Depends(verify_token)
# ):
#     return token_data
def get_current_user():
    return {
        "customer_id": UUID("11111111-1111-1111-1111-111111111111")
    }