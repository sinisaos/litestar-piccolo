from starlite.config.cors import CORSConfig
from starlite.config.csrf import CSRFConfig

from settings import SECRET_KEY

# CSRF
csrf_config = CSRFConfig(
    secret=SECRET_KEY,
    safe_methods=[
        "GET",
        "POST",
        "DELETE",
        "PUT",
        "PATCH",
        "OPTIONS",
    ],
)

# CORS
cors_config = CORSConfig(
    allow_origins=["http://localhost:8080"],
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
