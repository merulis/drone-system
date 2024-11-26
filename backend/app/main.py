from fastapi import FastAPI

from app.core.settings import settings
from app.api.main import router as api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
)

app.include_router(router=api_router, prefix=settings.API_PREFIX)


def main():
    import uvicorn

    uvicorn.run(app="main:app", reload=True)


if __name__ == "__main__":
    main()
