from fastapi import Header, HTTPException, Depends
from typing import Optional

VALID_API_KEY = "special-key"


def verify_api_key(api_key: Optional[str] = Header(None, alias="api_key")):
    if api_key is None or api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="API key is missing or invalid")
    return api_key
