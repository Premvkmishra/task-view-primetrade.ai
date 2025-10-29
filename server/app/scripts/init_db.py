from sqlalchemy import text
from ..db.session import engine
from ..models import Base


def init_db():
    # Create all tables and enums if they don't exist
    # SQLAlchemy will emit CREATE TYPE for named Enum on PostgreSQL
    Base.metadata.create_all(bind=engine, checkfirst=True)

    # Ensure helpful indexes exist if not created by metadata (safety)
    with engine.begin() as conn:
        conn.execute(text(
            "CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users (email)"
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS ix_tasks_user_id ON tasks (user_id)"
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks (status)"
        ))


if __name__ == "__main__":
    init_db()
    print("Database initialized.")
