import { useAuth } from '../features/auth/AuthContext';
import { useState } from 'react';
import { useWorkspaces, useDashboardSummary, useTimeSeries, useCreateWorkspace } from '../hooks/useAnalytics';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Activity, MousePointer2, LogIn, LayoutDashboard, PlusCircle,LogOut } from 'lucide-react';

export default function DashboardPage() {
    
  const { user, logoutUser } = useAuth();
  
  // 1. Get workspaces first
  const { data: workspaces, isLoading: loadingWorkspaces } = useWorkspaces();
  const [newWorkspaceName, setNewWorkspaceName] = useState('');
  const { mutate: createWorkspace, isPending: isCreating } = useCreateWorkspace();
  // 2. Safely grab the first workspace's slug (if it exists)
  const activeSlug = workspaces?.[0]?.slug;

  // 3. Fetch analytics for that specific workspace
  const { data: summary, isLoading: loadingSummary } = useDashboardSummary(activeSlug);
  const { data: timeseries, isLoading: loadingChart } = useTimeSeries(activeSlug);

  if (loadingWorkspaces || loadingSummary || loadingChart) {
    return <div className="flex h-screen items-center justify-center">Loading Analytics...</div>;
  }

 if (!workspaces || workspaces.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="bg-white p-10 rounded-2xl shadow-sm border border-slate-100 max-w-md w-full">
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold text-slate-900">Welcome to InsightFlow</h2>
            <p className="text-slate-500 mt-2">Let's create your first workspace to start tracking analytics.</p>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Company / Workspace Name</label>
              <input
                type="text"
                value={newWorkspaceName}
                onChange={(e) => setNewWorkspaceName(e.target.value)}
                placeholder="e.g. Acme Corp"
                className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              />
            </div>
            
            <button
              onClick={() => createWorkspace(newWorkspaceName)}
              disabled={isCreating || !newWorkspaceName}
              className="w-full flex justify-center items-center gap-2 bg-blue-600 text-white px-4 py-3 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isCreating ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              ) : (
                <>
                  <PlusCircle className="w-5 h-5" />
                  Create Workspace
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      {/* Header */}
      <header className="mb-8 flex justify-between items-center">
        <div>
            <h1 className="text-3xl font-bold text-slate-900">Analytics Overview</h1>
            <p className="text-slate-500">Workspace: <span className="font-semibold text-blue-600">{workspaces[0].name}</span></p>
        </div>
        <button 
          onClick={logoutUser}
          className="flex items-center gap-2 text-slate-500 hover:text-red-600 transition-colors px-4 py-2 rounded-lg hover:bg-red-50"
        >
          <LogOut className="w-5 h-5" />
          <span>Sign Out</span>
        </button>
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