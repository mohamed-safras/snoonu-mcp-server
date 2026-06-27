FROM postgres:16
# /docker-entrypoint-initdb.d/*.sql runs automatically on first start against an
# empty PGDATA — which is every cold start here, since the container has no
# persistent volume. Schema + read-only catalog data only; no orders/order_items,
# those should start empty on every fresh instance.
COPY 01-schema.sql /docker-entrypoint-initdb.d/01-schema.sql
COPY 02-seed-data.sql /docker-entrypoint-initdb.d/02-seed-data.sql
