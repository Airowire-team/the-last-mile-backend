from sqlalchemy import create_engine, text

engine = create_engine(
)

with engine.connect() as conn:
    result = conn.execute(text("SELECT datname FROM pg_database"))
    for row in result:
        print(row[0])