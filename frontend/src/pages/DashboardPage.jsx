import { useAuth } from '../features/auth/AuthContext';

export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <div className="p-10">
      <h1 className="text-3xl font-bold">Welcome to the Dashboard</h1>
      <p className="mt-4 text-gray-600">Logged in as: {user.email}</p>
    </div>
  );
}