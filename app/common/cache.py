from functools import wraps
import hashlib
import json
from loguru import logger
import pickle
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)

from app.common.configs import REDIS_DSN

REDIS_PORT = (
    int(REDIS_DSN['port'])
    if REDIS_DSN and REDIS_DSN['port']
    else 6379
)
REDIS_DB = (
    int(REDIS_DSN['path'].split("/")[1])
    if REDIS_DSN and REDIS_DSN['path']
    else 0
)
USERNAME = REDIS_DSN['user'] if REDIS_DSN else ""
PASSWORD = REDIS_DSN['password'] if REDIS_DSN else ""
HOST = REDIS_DSN['host'] if REDIS_DSN else ""
DEFAULT_TIMEOUT = 60 * 60 * 24

text_type = str
string_types = (str,)
integer_types = (int,)


def iteritems(d, *args, **kwargs):  # type: ignore
    return iter(d.items(*args, **kwargs))


def _items(mappingorseq):  # type: ignore
    if hasattr(mappingorseq, "items"):
        return iteritems(mappingorseq)
    return mappingorseq


def dump_object(value: Any) -> bytes:
    t = type(value)
    if t in integer_types:
        return str(value).encode("ascii")
    try:
        return b"!" + pickle.dumps(value)
    except Exception as e:
        logger.error(e)
        return b""


def load_object(value: bytes) -> Any:
    if value is None:
        return None
    if value.startswith(b"!"):
        try:
            return pickle.loads(value[1:])
        except pickle.PickleError:
            return None
    try:
        return int(value)
    except ValueError as e:
        logger.error(e)
        return value


class Cache:
    def __init__(  # type: ignore
        self,
        host=HOST,
        port=REDIS_PORT,
        password=PASSWORD,
        db=REDIS_DB,
        username=USERNAME,
        default_timeout=DEFAULT_TIMEOUT,
        key_prefix=None,
        **kwargs,
    ):
        self.default_timeout = default_timeout
        if host is None:
            raise ValueError("RedisCache host parameter may not be None")
        if isinstance(host, string_types):
            try:
                import redis
            except ImportError:
                raise RuntimeError("no redis module found")
            if kwargs.get("decode_responses", None):
                raise ValueError("decode_responses is not supported by RedisCache.")
            self._client: redis.StrictRedis = redis.StrictRedis(
                # username=username,
                host=host,
                port=port,
                password=password,
                db=db,
                **kwargs,
            )
            self._pubsub = self._client.pubsub()
        else:
            self._client = host
        self.key_prefix = key_prefix or ""

    def _normalize_timeout(self, timeout):  # type: ignore
        if timeout is None:
            timeout = self.default_timeout
            if timeout == 0:
                timeout = -1
        return timeout

    def get(self, key):  # type: ignore
        return load_object(self._client.get(self.key_prefix + key))

    def get_with_ttl(self, key: str) -> Tuple[int, str]:
        with self._client.pipeline(transaction=True) as pipe:
            ttl, value = pipe.ttl(key).get(key).execute()
            return ttl, load_object(value)

    def get_many(self, *keys):  # type: ignore
        if self.key_prefix:
            keys = [self.key_prefix + key for key in keys]
        return [load_object(x) for x in self._client.mget(keys)]

    def hgetall(self, pattern):  # type: ignore
        return self._client.hgetall(pattern)

    def hget(self, name, key):  # type: ignore
        value = self._client.hget(name, key)
        if value:
            return value.decode("utf")
        else:
            return None

    def keys(self, pattern):  # type: ignore
        return self._client.keys(pattern)

    def get_by_pattern(self, pattern):  # type: ignore
        keys = self._client.keys(pattern)
        return [load_object(x) for x in self._client.mget(keys)]

    def set(self, key: str, value: Any, timeout=None):  # type: ignore
        timeout = self._normalize_timeout(timeout)
        dump = dump_object(value)
        if timeout == -1:
            result = self._client.set(name=self.key_prefix + key, value=dump)
        else:
            result = self._client.setex(
                name=self.key_prefix + key, value=dump, time=timeout
            )
        return result

    def set_to_dict(self, key: str, value: dict, timeout: int = None):  # type: ignore
        timeout = self._normalize_timeout(timeout)
        cache_value = self.get(key=key)
        if isinstance(cache_value, dict):
            value = {**cache_value, **value}
        dump = dump_object(value)
        if timeout == -1:
            result = self._client.set(name=self.key_prefix + key, value=dump)
        else:
            result = self._client.setex(
                name=self.key_prefix + key, value=dump, time=timeout  # type: ignore
            )
        return result

    def add(self, key: str, value: Any, timeout: int = None) -> None:  # type: ignore
        timeout = self._normalize_timeout(timeout)
        dump = dump_object(value)
        return self._client.setnx(  # type: ignore
            name=self.key_prefix + key, value=dump
        ) and self._client.expire(
            name=self.key_prefix + key, time=timeout  # type: ignore
        )

    def set_many(self, mapping: Dict[str, Any], timeout=None):  # type: ignore
        timeout = self._normalize_timeout(timeout)
        pipe = self._client.pipeline(transaction=False)

        for key, value in _items(mapping):
            dump = dump_object(value)
            if timeout == -1:
                pipe.set(name=self.key_prefix + key, value=dump)
            else:
                pipe.setex(name=self.key_prefix + key, value=dump, time=timeout)
        return pipe.execute()

    def delete(self, key):  # type: ignore
        return self._client.delete(self.key_prefix + key)

    def delete_many(self, *keys):  # type: ignore
        if not keys:
            return
        if self.key_prefix:
            keys = [self.key_prefix + key for key in keys]
        return self._client.delete(*keys)

    def delete_by_pattern(self, pattern):  # type: ignore
        keys = self._client.keys(pattern)
        if not keys:
            logger.info(
                f"There is no key matches pattern {pattern} in Redis. Nothing to delete"
            )
            return True
        if self.key_prefix:
            keys = [self.key_prefix + key for key in keys]
        return self._client.delete(*keys)

    def has(self, key: str) -> bool:  # type: ignore
        return bool(self._client.exists(self.key_prefix + key))

    def clear(self):  # type: ignore
        status = False
        if self.key_prefix:
            keys = self._client.keys(self.key_prefix + "*")
            if keys:
                status = self._client.delete(*keys)
        else:
            status = self._client.flushdb()
        return status

    def publish(self, channel: str, message: Any) -> None:  # type: ignore
        return self._client.publish(channel, json.dumps(message))  # type: ignore

    def inc(self, key, delta=1):  # type: ignore
        return self._client.incr(name=self.key_prefix + key, amount=delta)

    def dec(self, key, delta=1):  # type: ignore
        return self._client.decr(name=self.key_prefix + key, amount=delta)

    def resource_cache(
        self,
        timeout: int = None,
        per_user: bool = False,
    ) -> Any:
        def wrapper(func):  # type: ignore
            @wraps(func)
            async def inner(*args, **kwargs):  # type: ignore
                nonlocal timeout
                copy_kwargs = kwargs.copy()
                timeout = timeout = self._normalize_timeout(timeout)
                request = copy_kwargs.pop("request", None)
                response = copy_kwargs.pop("response", None)
                force = copy_kwargs.pop("force", None)

                if not per_user:
                    copy_kwargs.pop("current_user", None)

                cache_key = (
                    self.key_prefix
                    + "_resource_cached_"
                    + hashlib.md5(  # nosec:B303
                        f"{func.__module__}:{func.__name__}:{args}:{copy_kwargs}".encode()
                    ).hexdigest()
                )

                if (
                    force
                    or request
                    and (request.headers.get("Cache-Control") == "no-store" or request.headers.get("Cache-Control") == "no-cache")
                ):
                    res = await func(*args, **kwargs)
                    cache_value = res
                    self.set(cache_key, cache_value, timeout)

                    return res

                ttl, cache_value = self.get_with_ttl(cache_key)
                if request is None:
                    if cache_value is not None and cache_value:
                        return cache_value
                    res = await func(*args, **kwargs)
                    cache_value = res
                    self.set(cache_key, cache_value, timeout)
                    return res

                if request.method != "GET":
                    return await func(*args, **kwargs)

                if_none_match = request.headers.get("if-none-match")
                if cache_value is not None and cache_value:
                    if response:
                        response.headers["Cache-Control"] = f"max-age={ttl}"
                        hash_value = hash(f"{cache_value}")
                        etag = f"W/{hash_value}"
                        if if_none_match == etag:
                            response.status_code = 304
                            return response
                        response.headers["ETag"] = etag
                    return cache_value
                res = await func(*args, **kwargs)
                self.set(cache_key, res, timeout)
                return res

            return inner

        return wrapper

    def pubsub_channels(self, pattern) -> List[str]:  # type: ignore
        return self._client.pubsub_channels(pattern=pattern)
    
    def pubsub_subscribe(self, channel) -> Any:
        ch = self._pubsub.subscribe(channel)
        return ch

    def pubsub_numsub(self, channels) -> List[Tuple[str, int]]:  # type: ignore
        return self._client.pubsub_numsub(*channels)
    
    
cache = Cache()
