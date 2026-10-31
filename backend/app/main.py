from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import portfolio, digest, alerts, research
from app.core.config import settings, BASE_DIR

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="FINN: Mobile-First Financial Investment Agent for High-Conviction Indian Equities (NSE/BSE)"
)

# Enable CORS for mobile web and local frontend Vite server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(portfolio.router, prefix=settings.API_V1_PREFIX)
app.include_router(digest.router, prefix=settings.API_V1_PREFIX)
app.include_router(alerts.router, prefix=settings.API_V1_PREFIX)
app.include_router(research.router, prefix=settings.API_V1_PREFIX)

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "FINN Backend Gateway"}

# Serve the built frontend when it exists, so one service can host the whole app
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"
if FRONTEND_DIST.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
else:
    @app.get("/")
    def root():
        return {
            "agent": "FINN",
            "description": "Financial Investment Agent for Indian Equities",
            "docs": "/docs",
            "status": "online"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

