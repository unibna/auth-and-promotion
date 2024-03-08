docker run \
--name postgres-cake \
-p 5432:5432 \
-e POSTGRES_PASSWORD=cake \
-e POSTGRES_DB=cake \
-e POSTGRES_USER=cake \
-d postgres
