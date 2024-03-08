import os


SERVICE_NAME = "auth"
API_SERVER_INFO = {
    "host": os.getenv("AUTH_API_SERVICE_HOST"),
    "port": int(os.getenv("AUTH_API_SERVICE_PORT")),
    "prefix": "/auth",
}
GRPC_SERVER_INFO = {
    "host": os.getenv("AUTH_GRPC_SERVICE_HOST"),
    "port": int(os.getenv("AUTH_GRPC_SERVICE_PORT")),
}
SESSION_TIMEOUT = 60 * 60 * 7


KAFKA_CONFIGS = {
    "bootstrap.servers": os.getenv("KAFKA_SERVER"),
    "group.id": "auth_service",
    "auto.offset.reset": os.getenv("KAFKA_AUTO_OFFSET_RESET"),
}
