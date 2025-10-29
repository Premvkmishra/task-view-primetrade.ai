import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { TaskList } from '@/components/TaskList';
import { LogOut, Shield, User } from 'lucide-react';

export default function Dashboard() {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card">
        <div className="container mx-auto flex items-center justify-between px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-primary p-2">
              {user?.role === 'admin' ? (
                <Shield className="h-5 w-5 text-primary-foreground" />
              ) : (
                <User className="h-5 w-5 text-primary-foreground" />
              )}
            </div>
            <div>
              <h1 className="text-xl font-semibold">Task Manager</h1>
              <p className="text-sm text-muted-foreground">{user?.email}</p>
            </div>
          </div>
          <Button variant="outline" onClick={logout}>
            <LogOut className="mr-2 h-4 w-4" />
            Logout
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto p-4 md:p-6">
        <div className="mb-6">
          <h2 className="text-2xl font-bold">
            {user?.role === 'admin' ? 'All Tasks' : 'My Tasks'}
          </h2>
          <p className="text-muted-foreground">
            {user?.role === 'admin' 
              ? 'Manage all tasks in the system' 
              : 'Manage your personal tasks'}
          </p>
        </div>
        <TaskList />
      </main>
    </div>
  );
}
