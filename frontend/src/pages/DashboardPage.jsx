import { useAuth } from '../features/auth/AuthContext';
import { useWorkspaces, useDashboardSummary, useTimeSeries } from '../hooks/useAnalytics';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Activity, MousePointer2, LogIn, LayoutDashboard } from 'lucide-react';

export default function DashboardPage() {
  const { user } = useAuth();
  
  // 1. Get workspaces first
  const { data: workspaces, isLoading: loadingWorkspaces } = useWorkspaces();
  
  // 2. Safely grab the first workspace's slug (if it exists)
  const activeSlug = workspaces?.[0]?.slug;

  // 3. Fetch analytics for that specific workspace
  const { data: summary, isLoading: loadingSummary } = useDashboardSummary(activeSlug);
  const { data: timeseries, isLoading: loadingChart } = useTimeSeries(activeSlug);

  if (loadingWorkspaces || loadingSummary || loadingChart) {
    return <div className="flex h-screen items-center justify-center">Loading Analytics...</div>;
  }

  if (!workspaces || workspaces.length === 0) {
    return <div className="p-10 text-xl font-semibold">You don't have any workspaces yet.</div>;
  }

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      {/* Header */}
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Analytics Overview</h1>
        <p className="text-slate-500">Workspace: <span className="font-semibold text-blue-600">{workspaces[0].name}</span></p>
      </header>

      {/* Top Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-slate-500 font-medium">Total Events</h3>
            <Activity className="text-blue-500 w-5 h-5" />
          </div>
          <p className="text-3xl font-bold text-slate-800">{summary?.total_events || 0}</p>
        </div>

        {summary?.events_by_type.map((event) => (
          <div key={event.event_name} className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-slate-500 font-medium capitalize">{event.event_name.replace('_', ' ')}</h3>
              {event.event_name === 'button_click' ? <MousePointer2 className="text-indigo-500 w-5 h-5" /> : 
               event.event_name === 'page_view' ? <LayoutDashboard className="text-emerald-500 w-5 h-5" /> :
               <LogIn className="text-orange-500 w-5 h-5" />}
            </div>
            <p className="text-3xl font-bold text-slate-800">{event.count}</p>
          </div>
        ))}
      </div>

      {/* Main Chart Section */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 h-96">
        <h3 className="text-lg font-bold text-slate-800 mb-6">Events Over Time (30 Days)</h3>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={timeseries}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
            <XAxis dataKey="date" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
            <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
            <Tooltip 
              contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            />
            <Line 
              type="monotone" 
              dataKey="count" 
              stroke="#3b82f6" 
              strokeWidth={3} 
              dot={{ fill: '#3b82f6', strokeWidth: 2 }} 
              activeDot={{ r: 8 }} 
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}