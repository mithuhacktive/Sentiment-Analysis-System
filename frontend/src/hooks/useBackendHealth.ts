import { useState, useEffect, useCallback } from 'react';
import { api } from '../services/api';
import { HealthResponse } from '../types/analysis';

export function useBackendHealth(pollIntervalMs = 12000) {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [isConnected, setIsConnected] = useState<boolean | null>(null);
  const [isChecking, setIsChecking] = useState(false);
  const [lastChecked, setLastChecked] = useState<Date | null>(null);

  const checkHealth = useCallback(async () => {
    setIsChecking(true);
    try {
      const data = await api.getHealth();
      setHealth(data);
      setIsConnected(true);
      setLastChecked(new Date());
    } catch {
      setIsConnected(false);
      setHealth(null);
      setLastChecked(new Date());
    } finally {
      setIsChecking(false);
    }
  }, []);

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, pollIntervalMs);
    return () => clearInterval(interval);
  }, [checkHealth, pollIntervalMs]);

  return {
    health,
    isConnected,
    isChecking,
    lastChecked,
    isModelReady: !!health?.model_loaded,
    isOfflineMode: !!health?.offline_mode,
    refreshHealth: checkHealth,
  };
}
