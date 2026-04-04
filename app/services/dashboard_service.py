from app.models.record import FinancialRecord, RecordType
from sqlmodel import Session, select, func

#total income, total expense, total net balance, total records, top expense category
def get_dashboard_summary(session: Session)->dict:
    #total income
    income_res = session.exec(
        select(func.coalesce(func.sum(FinancialRecord.amount),0))
        .where(FinancialRecord.type==RecordType.income)
        .where(FinancialRecord.is_deleted==False)
    ).one()

    #total expense
    expense_res = session.exec(
        select(func.coalesce(func.sum(FinancialRecord.amount),0))
        .where(FinancialRecord.type==RecordType.expense)
        .where(FinancialRecord.is_deleted==False)
    ).one()

    #total records
    count_res = session.exec(
        select(func.count(FinancialRecord.id))
        .where(FinancialRecord.is_deleted==False)
    ).one()

    #top expense category
    top_category_row = session.exec(
        select(
            FinancialRecord.category,
            func.sum(FinancialRecord.amount).label("total"),
        )
        .where(FinancialRecord.type==RecordType.expense)
        .where(FinancialRecord.is_deleted==False)
        .group_by(FinancialRecord.category)
        .order_by(func.sum(FinancialRecord.amount).desc())
        .limit(1)
    ).first()

    total_income = float(income_res)
    total_expense = float(expense_res)

    return {
        "total_income": round(total_income,2),
        "total_expense": round(total_expense,2),
        "net_balance": round(total_income-total_expense,2),
        "total_records": count_res,
        "top_category": top_category_row[0] if top_category_row else None,
        "top_category_total": round(float(top_category_row[1]),2) if top_category_row else None,
    }

#amounts grouped by category and type
def get_category_breakdown(session: Session)->list[dict]:
    res = session.exec(
        select(
            FinancialRecord.category,
            FinancialRecord.type,
            func.sum(FinancialRecord.amount).label("total"),
        )
        .where(FinancialRecord.is_deleted==False)
        .group_by(FinancialRecord.category, FinancialRecord.type)
        .order_by(FinancialRecord.category)
    ).all()

    return [
        {
            "category": row[0],
            "type": row[1].value,
            "total": round(float(row[2]),2),
        }
        for row in res
    ]

#income and expense aggregated by month
def get_monthly_trends(session: Session)->list[dict]:
    records = session.exec(
        select(FinancialRecord)
        .where(FinancialRecord.is_deleted==False)
        .order_by(FinancialRecord.date)
    ).all()

    months: dict[str, dict]={}
    for r in records:
        key = r.date.strftime("%Y-%m")
        if key not in months:
            months[key] = {"month": key,"income": 0.0, "expense":0.0}
        if r.type==RecordType.income:
            months[key]["income"]+=r.amount
        else:
            months[key]["expense"]+=r.amount
    
    result =sorted(months.values(),key=lambda x:x["month"])
    for item in result:
        item["income"]= round(item["income"],2)
        item["expense"]= round(item["expense"],2)
        item["net"]= round(item["income"]-item["expense"],2)
    
    return result

#recent 'n' records sorted by date
def recent_activity(session: Session, n: int=5)->list[FinancialRecord]:
    query = (
        select(FinancialRecord)
        .where(FinancialRecord.is_deleted==False)
        .order_by(FinancialRecord.date.desc())
        .limit(n)
    )
    return list(session.exec(query).all())

