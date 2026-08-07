# Summary

## What was implemented

- React frontend with Vite + TypeScript setup in `frontend/` directory
- FastAPI backend API layer in `src/backend/api/`
- API endpoints for pipeline control (accept, reject, skip, back) and status
- Dev/production mode configuration via Vite proxy and environment variables
- Updated Runner class to support both PyQt GUI and API server modes

## Design decisions

- Used FastAPI for the backend API due to its simplicity and automatic docs
- Vite proxy configured for development mode, production can use reverse proxy
- API routes mirror existing PipelineManager methods for consistency
- Added `main_api.py` entry point that starts both pipeline and API server

## Notable changes

- Added `fastapi` and `uvicorn` to requirements.txt
- Updated `.gitignore` for frontend build artifacts
- Created `frontend/src/types/types.ts` for shared TypeScript types
- Created `frontend/src/services/api.ts` for API communication
- Created `frontend/src/hooks/usePipelineStatus.ts` for polling pipeline status
- Created `frontend/src/components/PipelineControls.tsx` for UI controls

## Testing notes

- Run `main_api.py` to start API server on port 8000
- Run `cd frontend && npm run dev` to start frontend dev server on port 5173
- Frontend proxies `/api` requests to backend in development mode

## Related tasks

- None
