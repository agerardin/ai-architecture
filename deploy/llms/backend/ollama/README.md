# Ollama

## Setup

rename `.env.sample` to `.env` and provide missing values

Make sure the shared network has been created (for integration with other running containers)
`docker network create shared_net`

Spin the proxy

```sh
docker compose up
```

## Test

Pull a model


```sh
OLLAMA_HOST="http://localhost:11433" ollama pull mistral:7b
```

Call the newer endpoint (careful about legacy api)

```sh
curl http://ollama:11434/api/generate -d '{
  "model": "mistral:7b",
  "prompt": "Why is the sky blue?"
}'
```