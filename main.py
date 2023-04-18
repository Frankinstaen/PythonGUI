from Entity.Models import Base, engine, Personal, Pc, Departments, Сontracts, Login_dates
from sqlalchemy import select
from sqlalchemy.orm import create_session, Session, joinedload
from sqlalchemy.orm import contains_eager, joinedload


if __name__ == '__main__':
    with Session(engine) as session:
        query = session.query(Personal).options(joinedload(Personal.department),
                                                joinedload(Personal.pc),
                                                joinedload(Personal.login_dates),
                                                joinedload(Personal.salary),
                                                joinedload(Personal.contracts))
        results = query.all()
        results = list(set(results))
    print(1)
