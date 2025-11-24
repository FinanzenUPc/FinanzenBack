from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.database import engine, Base
from app.routers import auth, transactions, dataset_router, graph_router, algorithms_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend de Finanzen con algoritmos de grafos para análisis financiero",
    version="2.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Host Middleware (Security)
if not settings.DEBUG:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1"]
    )

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(transactions.router, prefix=settings.API_V1_STR)
app.include_router(dataset_router.router, prefix=settings.API_V1_STR)
app.include_router(graph_router.router, prefix=settings.API_V1_STR)
app.include_router(algorithms_router.router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Finanzen API",
        "version": "1.0.0",
        "docs": f"{settings.API_V1_STR}/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get(f"{settings.API_V1_STR}/info")
async def api_info():
    """API information endpoint."""
    return {
        "name": settings.PROJECT_NAME,
        "version": "2.0.0",
        "api_prefix": settings.API_V1_STR,
        "description": "Backend de Finanzen con algoritmos de grafos",
        "features": {
            "authentication": "JWT",
            "database": "PostgreSQL",
            "algorithms": [
                "BFS", "DFS", "Dijkstra", "Bellman-Ford", "Floyd-Warshall",
                "MST (Kruskal & Prim)", "Dynamic Programming (Knapsack)", "Union-Find"
            ],
            "graph_types": ["GT (Transacciones)", "GC (Categorías)", "GUC (Usuario-Categoría)"]
        },
        "endpoints": {
            "dataset": ["/dataset/upload", "/dataset/schema", "/dataset/normalize"],
            "graphs": ["/graphs/build", "/graphs/{type}", "/graphs/stats"],
            "algorithms": [
                "/algorithms/bfs", "/algorithms/dfs", "/algorithms/dijkstra",
                "/algorithms/bellman-ford", "/algorithms/floyd-warshall",
                "/algorithms/mst/prim", "/algorithms/mst/kruskal",
                "/algorithms/dp-mochila"
            ],
            "transactions": ["/transactions", "/transactions/{id}"],
            "auth": ["/auth/register", "/auth/login"]
        }
    }


# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
