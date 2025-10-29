import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { TaskDialog } from '@/components/TaskDialog';
import { Plus, Pencil, Trash2 } from 'lucide-react';
import { toast } from 'sonner';
import { api } from '@/lib/api';

export interface Task {
  id: number;
  title: string;
  description: string;
  status: 'pending' | 'in_progress' | 'completed';
  user_id: number;
  created_at: string;
  updated_at: string;
}

export function TaskList() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  useEffect(() => {
    const load = async () => {
      if (!user) return;
      try {
        const res = await api.get<{ success: boolean; data: { tasks: Task[]; total: number } }>(
          `/tasks?page=1&limit=20`
        );
        setTasks(res.data.tasks);
      } catch (e: any) {
        toast.error(e.message || 'Failed to load tasks');
      }
    };
    load();
  }, [user]);

  const handleCreateTask = async (taskData: { title: string; description?: string; status?: Task['status'] }) => {
    try {
      const res = await api.post<{ success: boolean; data: Task; message: string }>(
        '/tasks',
        taskData
      );
      setTasks([res.data, ...tasks]);
      toast.success('Task created successfully');
      setIsDialogOpen(false);
    } catch (e: any) {
      toast.error(e.message || 'Failed to create task');
    }
  };

  const handleUpdateTask = async (taskData: { title?: string; description?: string; status?: Task['status'] }) => {
    if (!editingTask) return;
    try {
      const res = await api.put<{ success: boolean; data: Task; message: string }>(
        `/tasks/${editingTask.id}`,
        taskData
      );
      const updated = res.data;
      setTasks(tasks.map(t => (t.id === updated.id ? updated : t)));
      toast.success('Task updated successfully');
      setEditingTask(null);
      setIsDialogOpen(false);
    } catch (e: any) {
      toast.error(e.message || 'Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    try {
      await api.delete<{ success: boolean; data: null; message: string }>(`/tasks/${taskId}`);
      setTasks(tasks.filter(task => task.id !== taskId));
      toast.success('Task deleted successfully');
    } catch (e: any) {
      toast.error(e.message || 'Failed to delete task');
    }
  };

  const getStatusColor = (status: Task['status']) => {
    switch (status) {
      case 'completed':
        return 'bg-green-500/10 text-green-700 dark:text-green-400';
      case 'in_progress':
        return 'bg-blue-500/10 text-blue-700 dark:text-blue-400';
      case 'pending':
        return 'bg-yellow-500/10 text-yellow-700 dark:text-yellow-400';
    }
  };

  const getStatusLabel = (status: Task['status']) => {
    return status.replace('_', ' ').charAt(0).toUpperCase() + status.slice(1).replace('_', ' ');
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-end">
        <Button onClick={() => setIsDialogOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          New Task
        </Button>
      </div>

      {tasks.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <p className="text-muted-foreground">No tasks yet. Create your first task to get started!</p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {tasks.map((task) => (
            <Card key={task.id} className="hover:shadow-lg transition-shadow">
              <CardContent className="p-4">
                <div className="space-y-3">
                  <div className="flex items-start justify-between">
                    <h3 className="font-semibold">{task.title}</h3>
                    <Badge variant="secondary" className={getStatusColor(task.status)}>
                      {getStatusLabel(task.status)}
                    </Badge>
                  </div>
                  
                  <p className="text-sm text-muted-foreground line-clamp-2">
                    {task.description}
                  </p>
                  
                  {/* Owner info is not included in TaskOut; admin UI can be extended later */}
                  
                  <div className="flex gap-2 pt-2">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => {
                        setEditingTask(task);
                        setIsDialogOpen(true);
                      }}
                    >
                      <Pencil className="h-3 w-3" />
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleDeleteTask(task.id)}
                    >
                      <Trash2 className="h-3 w-3" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <TaskDialog
        open={isDialogOpen}
        onOpenChange={(open) => {
          setIsDialogOpen(open);
          if (!open) setEditingTask(null);
        }}
        onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
        task={editingTask}
      />
    </div>
  );
}
