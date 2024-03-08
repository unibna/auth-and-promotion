docker run \
--name redis-cake \
-p 6379:6379 \
-d redis redis-server --appendonly yes --requirepass redis