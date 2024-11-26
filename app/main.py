import uvicorn

from app import models
from app.database import engine
from app.config.config import settings
from app.create_app import create_app


# Create tables using Alembic for migrations (instead of using Pydantic)
models.Base.metadata.create_all(bind=engine)


app = create_app()


def main():
    """Main function."""
    rc = 0

    try:
        uvicorn.run(app, host=settings.host, port=settings.port)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(f'Error: {exc}')
        rc = -1

    return rc


if __name__ == '__main__':
    main()
