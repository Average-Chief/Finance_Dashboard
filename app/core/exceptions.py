from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

#error handlers
#clean validation errors instead of pydantic output
async def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = []
    for i in exc.errors():
        errors.append(
            {
                "field": "->".join(str(loc) for loc in i['loc']),
                "message": i["msg"]
            }
        )
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Error in Validation",
            "errors": errors
        }
    )

async def global_exception_handler(request:Request, exc:Exception):
    return JSONResponse(
        status_code=500,
        content={"detail":"Internal sever error"}
    )

def register_handlers(app):
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, global_exception_handler)

