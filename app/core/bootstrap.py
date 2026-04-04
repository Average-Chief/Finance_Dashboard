from sqlmodel import Session, select
from app.models.user import User, Role
from app.core.auth import hash_password

#creates an admin account as the first user
def create_initial_admin(session: Session):
    existing_user = session.exec(select(User)).first()
    if existing_user:
        return

    admin = User(
        email="admin@finance.com",
        name="Admin",
        hashed_password=hash_password("admin123"),
        role=Role.admin,
        is_active=True
    )

    session.add(admin)
    session.commit()