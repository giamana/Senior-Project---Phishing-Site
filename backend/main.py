
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ package-relative imports
from .database import Base, engine
from .auth import router as auth_router
from .routers.employees import router as employees_router
from .routers.employers import router as employers_router
from .routers.developers import router as developers_router
from .routers.stats import router as stats_router
from .routers.tracking import router as tracking_router



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Phishing Campaign Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(employees_router, prefix="/api", tags=["employees"])
app.include_router(employers_router, prefix="/api", tags=["employers"])
app.include_router(developers_router, prefix="/api", tags=["developers"])
app.include_router(stats_router, prefix="/api", tags=["stats"])
app.include_router(tracking_router, prefix="/api", tags=["tracking"])
