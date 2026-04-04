from datetime import date
from app.db import init_db, engine
from app.models.user import User, Role
from app.models.record import FinancialRecord, RecordType
from app.core.auth import hash_password
from sqlmodel import Session


def seed():
    init_db()

    with Session(engine) as session:

        #users
        admin = User(
            email="admin@finance.com",
            name="John Price",
            hashed_password=hash_password("admin123"),
            role=Role.admin,
        )
        analyst = User(
            email="analyst@finance.com",
            name="Haytham Kenway",
            hashed_password=hash_password("analyst123"),
            role=Role.analyst,
        )
        viewer = User(
            email="viewer@finance.com",
            name="Leon Kennedy",
            hashed_password=hash_password("viewer123"),
            role=Role.viewer,
        )

        session.add_all([admin, analyst, viewer])
        session.commit()
        session.refresh(admin)

        # records
        records = [
            #January 2026
            FinancialRecord(amount=5000, type=RecordType.income, category="Salary", currency="INR", date=date(2026, 1, 1), description="January salary", created_by=admin.id),
            FinancialRecord(amount=1200, type=RecordType.expense, category="Rent", currency="INR", date=date(2026, 1, 5), description="Monthly rent", created_by=admin.id),
            FinancialRecord(amount=200, type=RecordType.expense, category="Utilities", currency="INR", date=date(2026, 1, 10), description="Electricity bill", created_by=admin.id),
            FinancialRecord(amount=150, type=RecordType.expense, category="Food", currency="INR", date=date(2026, 1, 15), description="Groceries", created_by=admin.id),

            #February 2026
            FinancialRecord(amount=5000, type=RecordType.income, category="Salary", currency="INR", date=date(2026, 2, 1), description="February salary", created_by=admin.id),
            FinancialRecord(amount=500, type=RecordType.income, category="Freelance", currency="INR", date=date(2026, 2, 10), description="Side project", created_by=admin.id),
            FinancialRecord(amount=1200, type=RecordType.expense, category="Rent", currency="INR", date=date(2026, 2, 5), description="Monthly rent", created_by=admin.id),
            FinancialRecord(amount=300, type=RecordType.expense, category="Food", currency="INR", date=date(2026, 2, 20), description="Dining out", created_by=admin.id),

            #March 2026
            FinancialRecord(amount=5200, type=RecordType.income, category="Salary", currency="INR", date=date(2026, 3, 1), description="March salary + bonus", created_by=admin.id),
            FinancialRecord(amount=1200, type=RecordType.expense, category="Rent", currency="INR", date=date(2026, 3, 5), description="Monthly rent", created_by=admin.id),
            FinancialRecord(amount=800, type=RecordType.expense, category="Travel", currency="INR", date=date(2026, 3, 15), description="Weekend trip", created_by=admin.id),
            FinancialRecord(amount=100, type=RecordType.expense, category="Utilities", currency="INR", date=date(2026, 3, 20), description="Internet bill", created_by=admin.id),

            #April 2026
            FinancialRecord(amount=5000, type=RecordType.income, category="Salary", currency="INR", date=date(2026, 4, 1), description="April salary", created_by=admin.id),
            FinancialRecord(amount=1000, type=RecordType.income, category="Investment", currency="INR", date=date(2026, 4, 10), description="Dividend", created_by=admin.id),
            FinancialRecord(amount=1200, type=RecordType.expense, category="Rent", currency="INR", date=date(2026, 4, 5), description="Monthly rent", created_by=admin.id),
            FinancialRecord(amount=250, type=RecordType.expense, category="Food", currency="INR", date=date(2026, 4, 18), description="Groceries", created_by=admin.id),
        ]

        session.add_all(records)
        session.commit()

        print("Database seeded successfully!")
        print(f"Users: admin / analyst / viewer (password: <role>123)")
        print(f"Records: {len(records)} financial entries created")


if __name__ == "__main__":
    seed()