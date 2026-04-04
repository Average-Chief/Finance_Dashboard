from app.db import init_db, engine
from app.core.exceptions import register_handlers
from app.core.rate_limit import register_rate_limiter
from app.core.bootstrap import create_initial_admin
from app.routes import records, dashboard, auth, users
from fastapi import FastAPI
from sqlmodel import Session

#fastapi app setup
app = FastAPI(
    title="Finance Dashboard",
    description="Backend for finance data processing", 
    version="1.0", 
    docs_url="/docs", 
    redoc_url="/redoc"
)

#initiate db to create tables and an admin account
@app.on_event("startup")
def on_startup():
    init_db()

    with Session(engine) as session:
        create_initial_admin(session)


#register exception and limit handlers
register_handlers(app)
register_rate_limiter(app)

#route register
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)

@app.get("/", tags=["Health"])
def health_check():
    return {"status":"Up and running", "message":"Finance Dashboard Backend is live"}