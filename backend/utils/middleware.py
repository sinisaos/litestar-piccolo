from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig

from config.base import settings

# CSRF
csrf_config = CSRFConfig(
    secret=str(settings.secret_key),
    safe_methods={
        "GET",
        "POST",
        "DELETE",
        "PUT",
        "PATCH",
        "OPTIONS",
    },
)

# CORS
cors_config = CORSConfig(
    allow_origins=["http://localhost:5173"],
    allow_methods=[
        "GET",
        "POST",
        "DELETE",
        "PUT",
        "PATCH",
        "OPTIONS",
    ],
    allow_headers=["Origin", "Content-Type", "X-CSRFToken"],
    allow_credentials=True,
)
