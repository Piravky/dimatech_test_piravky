from fastapi import HTTPException, status

dont_have_permission = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You don't have permission to do this action",
    headers={"WWW-Authenticate": "Bearer"},
)

email_is_registered = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Email already registered"
)

invalid_signature = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid signature",
)

user_dont_exist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
)

transaction_exists = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Transaction was completed",
)

