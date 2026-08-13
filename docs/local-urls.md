# Local URLs

| URL | What it serves |
|---|---|
| `http://localhost:8080/petstore/` | Petstore web UI |
| `http://localhost:8000/docs` | REST API |
| `http://localhost:8001/graphql` | GraphQL app |
| `http://localhost:50051` | Native gRPC |
| `http://localhost:8081/grpcui/` | gRPC-Web UI |
| `http://localhost:9901/` | Envoy admin UI |
| `postgresql://localhost:5432/petstore` | PostgreSQL database |

Use `docker compose up -d --wait` if you want Compose to block until the services with healthchecks are ready.

## Port overrides

These host ports can be changed with compose environment variables:

- `HOST_GRPC_PORT`
- `HOST_GRPC_WEB_PORT`
- `HOST_GRAPHQL_PORT`
- `HOST_ENVOY_ADMIN_PORT`
