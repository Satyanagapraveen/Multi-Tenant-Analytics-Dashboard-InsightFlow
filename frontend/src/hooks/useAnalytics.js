import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../api/client';

// 1. Fetch the user's workspaces
export const useWorkspaces = () => {
  return useQuery({
    queryKey: ['workspaces'],
    queryFn: async () => {
      const { data } = await apiClient.get('/api/workspaces/');
      return data;
    },
  });
};

// 2. Fetch the summary numbers (cached in Redis)
export const useDashboardSummary = (workspaceSlug) => {
  return useQuery({
    queryKey: ['summary', workspaceSlug],
    queryFn: async () => {
      const { data } = await apiClient.get(`/api/w/${workspaceSlug}/dashboard/summary/`);
      return data;
    },
    enabled: !!workspaceSlug, // Only run if we actually have a slug
  });
};

// 3. Fetch the chart data
export const useTimeSeries = (workspaceSlug, period = '30d') => {
  return useQuery({
    queryKey: ['timeseries', workspaceSlug, period],
    queryFn: async () => {
      const { data } = await apiClient.get(`/api/w/${workspaceSlug}/dashboard/timeseries/?period=${period}`);
      return data;
    },
    enabled: !!workspaceSlug,
  });
};

export const useCreateWorkspace = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (name) => {
      const { data } = await apiClient.post('/api/workspaces/', { name });
      return data;
    },
    onSuccess: () => {
      // This is magic. It tells React Query "The database changed! Go fetch the new list!"
      queryClient.invalidateQueries({ queryKey: ['workspaces'] });
    },
  });
};