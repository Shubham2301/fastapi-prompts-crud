from typing import Optional

def error_body(code: str, message:str, details: Optional[list] = None) -> dict:
    error = {"code": code, "message": message }

    if details is not None:
        error["details"] = details

    return {"error": error};