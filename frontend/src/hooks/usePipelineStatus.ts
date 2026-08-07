import { useState, useEffect, useCallback } from 'react'
import { api } from '../services/api'
import { PipelineStatusResponse } from '../types/types'

export const usePipelineStatus = () => {
  const [status, setStatus] = useState<PipelineStatusResponse | null>(null)
  const [loading, setLoading] = useState(true)

  const refresh = useCallback(async () => {
    try {
      const data = await api.getPipelineStatus()
      setStatus(data)
    } catch (err) {
      console.error('Failed to fetch pipeline status:', err)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    refresh()
    const interval = setInterval(refresh, 1000)
    return () => clearInterval(interval)
  }, [refresh])

  return { status, loading, refresh }
}
