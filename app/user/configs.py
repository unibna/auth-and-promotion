import os


SERVICE_NAME = "user"
API_SERVER_INFO = {
    "host": os.getenv("USER_API_SERVICE_HOST"),
    "port": int(os.getenv("USER_API_SERVICE_PORT")),
    "prefix": "/users",
}
GRPC_SERVER_INFO = {
    "port": int(os.getenv("USER_GRPC_SERVICE_PORT")),
}
