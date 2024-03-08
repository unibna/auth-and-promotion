import grpc
from loguru import logger

from app.user import models, schemas
from app.user.pb import example_pb2, example_pb2_grpc
from app.user.configs import GRPC_SERVER_INFO
from app.utils.tortoise_utils import tortoise_to_pydantic


class UserServicer(example_pb2_grpc.UserServicer):
    async def GetUser(self, request, context):
        user = await models.User.get(request.user_id)
        response_as_dict = tortoise_to_pydantic(user, schemas.UserResponse)
        return example_pb2.GetUserResponse(**response_as_dict)
    

async def start_server():
    logger.info("start GRPC server")
    # server = grpc.server(grpc.ThreadPoolExecutor(max_workers=10))
    # example_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
    # server.add_insecure_port(f'[::]:{GRPC_SERVER_INFO.get("port")}')
    # server.start()
    # server.wait_for_termination()
    logger.success("start GRPC server successfully")


async def stop_server():
    logger.info("stop GRPC server")
    pass
    logger.success("stop GRPC server successfully")
