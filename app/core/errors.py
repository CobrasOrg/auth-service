from fastapi.responses import JSONResponse
from fastapi import Request, status, HTTPException
from fastapi.exceptions import RequestValidationError

def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail}
    )

def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    
    sanitized_errors = []
    for error in errors:
        error_location = str(error.get("loc", []))
        error_input = error.get("input", {})

        is_sensitive = (
            any(field.lower() in error_location.lower() 
                for field in ["password", "token"]) or
            any(field in error.get("msg", "").lower() 
                for field in ["password", "token"]) or
            (isinstance(error_input, dict) and 
             any(field in str(error_input.keys()).lower() 
                 for field in ["password", "token"]))
        )
        
        if is_sensitive:
            sanitized_error = {
                "loc": error["loc"],
                "msg": error["msg"]
            }
        else:
            sanitized_error = {
                "loc": error["loc"],
                "msg": error["msg"],
                "input": error.get("input")
            }
        
        sanitized_errors.append(sanitized_error)
        
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "errors": sanitized_errors}
    )