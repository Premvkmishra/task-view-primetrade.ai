import { Link } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { CheckCircle2, ListTodo, Shield, ArrowRight } from 'lucide-react';

const Index = () => {
  const { user } = useAuth();

  if (user) {
    window.location.href = '/dashboard';
    return null;
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16 md:py-24">
        <div className="flex flex-col items-center text-center space-y-8">
          <div className="rounded-full bg-primary p-4">
            <ListTodo className="h-12 w-12 text-primary-foreground" />
          </div>
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight">
            Task Management <span className="text-primary">Made Simple</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl">
            Organize your work, track progress, and collaborate with your team. 
            Built with role-based access control for secure task management.
          </p>
          <div className="flex gap-4">
            <Link to="/register">
              <Button size="lg" className="group">
                Get Started
                <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Button>
            </Link>
            <Link to="/login">
              <Button size="lg" variant="outline">
                Sign In
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="grid gap-6 md:grid-cols-3">
          <Card>
            <CardContent className="pt-6">
              <div className="rounded-lg bg-primary/10 p-3 w-fit mb-4">
                <CheckCircle2 className="h-6 w-6 text-primary" />
              </div>
              <h3 className="font-semibold text-lg mb-2">Easy Task Management</h3>
              <p className="text-muted-foreground">
                Create, update, and organize tasks with an intuitive interface. 
                Track status from pending to completion.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="rounded-lg bg-primary/10 p-3 w-fit mb-4">
                <Shield className="h-6 w-6 text-primary" />
              </div>
              <h3 className="font-semibold text-lg mb-2">Role-Based Access</h3>
              <p className="text-muted-foreground">
                Secure authentication with user and admin roles. 
                Control who can view and manage tasks.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="rounded-lg bg-primary/10 p-3 w-fit mb-4">
                <ListTodo className="h-6 w-6 text-primary" />
              </div>
              <h3 className="font-semibold text-lg mb-2">Real-time Updates</h3>
              <p className="text-muted-foreground">
                See changes instantly as you work. 
                Collaborate efficiently with your team.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  );
};

export default Index;
