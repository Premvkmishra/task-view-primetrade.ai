import os
import psycopg2
from psycopg2.extras import DictCursor
from pathlib import Path
from dotenv import load_dotenv

# Load env from repo root
ROOT_DOTENV = Path(__file__).resolve().parents[1] / ".env"
if ROOT_DOTENV.exists():
    load_dotenv(ROOT_DOTENV)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in environment")

SQL = r"""
-- Create enums if not exist
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
        CREATE TYPE user_role AS ENUM ('user', 'admin');
    END IF;
END $$;

DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'task_status') THEN
        CREATE TYPE task_status AS ENUM ('pending', 'in_progress', 'completed');
    END IF;
END $$;

-- users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'user',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ensure unique email index
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users (email);

-- tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NULL,
    status task_status NOT NULL DEFAULT 'pending',
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- helpful indexes
CREATE INDEX IF NOT EXISTS ix_tasks_user_id ON tasks (user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks (status);
"""

def run():
    # psycopg2 honors sslmode=require in DATABASE_URL
    with psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(SQL)
            print("Supabase schema ensured (enums, tables, indexes)")

if __name__ == "__main__":
    run()
