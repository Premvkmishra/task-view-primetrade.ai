<div align="center">

<img alt="Project banner" src="./assets/sss1.png" width="640" />

# Secure Node Stack (FastAPI + React)

Secure, scalable REST API with JWT auth, RBAC, and Tasks CRUD. Backend: FastAPI + SQLAlchemy. DB: Supabase Postgres (or SQLite for local dev). Frontend: Vite + React + TypeScript + shadcn/ui.

</div>

---

## Architecture
- Backend: `server/` (FastAPI, SQLAlchemy, Pydantic, JWT)
- DB: Supabase Postgres (via `DATABASE_URL`), optional SQLite fallback for local dev
- Frontend: `src/` (Vite + React + TS)
- Shared response shape: `{ success: boolean, data: any, message: string }`

## Quick start

- Prereqs: Node 18+, Python 3.11+, PowerShell (Windows), Supabase project (optional for prod)

1) Clone and install frontend deps
```
npm install
```

2) Python venv and install backend deps
```
cd server
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

3) Environment (.env at repo root)
```
# Server
PORT=4000
NODE_ENV=development
JWT_SECRET=change-this-in-prod
# Supabase (preferred for prod)
# Use pooled port 6543 if 5432 is blocked; keep @ encoded as %40
DATABASE_URL="postgresql://postgres:Secure%40123@db.<project-ref>.supabase.co:6543/postgres?sslmode=require"
```
Optional frontend env `.env.local`:
```
VITE_API_URL=http://localhost:4000/api/v1
```

4) Create database schema
- Supabase (hosted Postgres):
```
cd server
python supabase.py
```
- Local dev fallback (SQLite):
```
# set in repo-root .env
DATABASE_URL="sqlite:///./dev.db"
cd server
python -m app.scripts.init_db
```

5) Run backend
```
cd server
uvicorn app.main:app --host 0.0.0.0 --port 4000 --reload
```
Docs: http://localhost:4000/docs

6) Run frontend
```
npm run dev
```
Vite dev URL is shown in the terminal.

## Database schema

- Enums
  - `user_role`: `user` | `admin`
  - `task_status`: `pending` | `in_progress` | `completed`
- Tables
  - `users`
    - `id` SERIAL PRIMARY KEY
    - `email` VARCHAR(255) UNIQUE NOT NULL
    - `password` VARCHAR(255) NOT NULL (bcrypt hashed)
    - `role` user_role DEFAULT `user`
    - `created_at`, `updated_at` TIMESTAMPTZ DEFAULT now()
  - `tasks`
    - `id` SERIAL PRIMARY KEY
    - `title` VARCHAR(255) NOT NULL
    - `description` TEXT
    - `status` task_status DEFAULT `pending`
    - `user_id` INT NOT NULL REFERENCES users(id) ON DELETE CASCADE
    - `created_at`, `updated_at` TIMESTAMPTZ DEFAULT now()
- Indexes
  - `ix_users_email` (unique)
  - `ix_tasks_user_id`
  - `idx_tasks_status`

Schema creation options:
- `server/supabase.py` executes SQL for enums, tables, and indexes on Supabase.
- `app/scripts/init_db.py` uses SQLAlchemy `metadata.create_all` for local SQLite.

## API
Base: `/api/v1`

- Auth
  - POST `/auth/register`
    - Body: `{ email: string, password: string, role?: 'user'|'admin' }`
    - 201 → `{ success, data: { user, token }, message }`
  - POST `/auth/login`
    - Body: `{ email: string, password: string }`
    - 200 → `{ success, data: { user, token }, message }`

- Tasks (Bearer token required)
  - GET `/tasks?status=pending&page=1&limit=10`
    - 200 → `{ success, data: { tasks: Task[], total: number }, message }`
  - GET `/tasks/{id}`
    - 200 → `{ success, data: Task, message }`
  - POST `/tasks`
    - Body: `{ title: string, description?: string, status?: 'pending'|'in_progress'|'completed' }`
    - 201 → `{ success, data: Task, message }`
  - PUT `/tasks/{id}`
    - Body: partial `{ title?, description?, status? }`
    - 200 → `{ success, data: Task, message }`
  - DELETE `/tasks/{id}`
    - 200 → `{ success, data: null, message }`

Task ownership & RBAC:
- Users can access only their tasks.
- Admins can access all tasks.

## JWT security
- JWT created with HS256 and `JWT_SECRET`, expires in 24h.
- Sent by clients in `Authorization: Bearer <token>` header.
- Avoid storing tokens in non-HTTP-only cookies in production. This demo uses localStorage for simplicity.
- Change `JWT_SECRET` in production and rotate periodically.
- Rate limiting and security headers can be added; FastAPI supports middleware.

## Frontend integration
- API client: `src/lib/api.ts` uses `VITE_API_URL` or defaults to `http://localhost:4000/api/v1`.
- AuthContext wires Register/Login to backend and persists `{ user, token }` in localStorage.
- TaskList calls backend CRUD and renders results.

## Troubleshooting Supabase connectivity (Windows)
- If DNS fails for `db.<project-ref>.supabase.co`:
  - Set adapter DNS to Cloudflare (1.1.1.1/1.0.0.1) or Google (8.8.8.8/8.8.4.4), then `ipconfig /flushdns`.
  - Ensure IPv6 is enabled or your network supports it.
- If port 5432 is blocked, use pooled port 6543 in `DATABASE_URL`.
- Corporate firewalls/VPNs may block DB ports; try a different network or hotspot.
- Local dev fallback: set `DATABASE_URL="sqlite:///./dev.db"` and run `python -m app.scripts.init_db`.

## Scripts
- Init Supabase schema: `python server/supabase.py`
- Init local SQLite: `python -m app.scripts.init_db`
- Seed admin (optional): `python -m app.seed` (admin@example.com / Admin@123)

## Project scripts
- Frontend
  - `npm run dev` – Vite dev server
  - `npm run build` – build frontend
  - `npm run preview` – preview build
- Backend
  - `uvicorn app.main:app --host 0.0.0.0 --port 4000 --reload`

## License
MIT

The only requirement is having Node.js & npm installed - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

Follow these steps:

```sh
# Step 1: Clone the repository using the project's Git URL.
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the project directory.
cd <YOUR_PROJECT_NAME>

# Step 3: Install the necessary dependencies.
npm i

# Step 4: Start the development server with auto-reloading and an instant preview.
npm run dev
```

**Edit a file directly in GitHub**

- Navigate to the desired file(s).
- Click the "Edit" button (pencil icon) at the top right of the file view.
- Make your changes and commit the changes.

**Use GitHub Codespaces**

- Navigate to the main page of your repository.
- Click on the "Code" button (green button) near the top right.
- Select the "Codespaces" tab.
- Click on "New codespace" to launch a new Codespace environment.
- Edit files directly within the Codespace and commit and push your changes once you're done.

## What technologies are used for this project?

This project is built with:

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS

## How can I deploy this project?

Simply open [Lovable](https://lovable.dev/projects/389bc697-2fab-4429-b715-2443afa8e4b0) and click on Share -> Publish.

## Can I connect a custom domain to my Lovable project?

Yes, you can!

To connect a domain, navigate to Project > Settings > Domains and click Connect Domain.

Read more here: [Setting up a custom domain](https://docs.lovable.dev/features/custom-domain#custom-domain)
