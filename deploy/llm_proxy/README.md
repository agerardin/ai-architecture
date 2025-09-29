# LLM_PROXY

Gateway to centralized all llms calls.
Add keys management, metering, budget etc...

## Setup

rename `.env.sample` to `.env` and provide missing values

Spin the proxy

```sh
docker compose up
```

## Test

Load all env

```sh
export $(grep -v '^#' .env | xargs)
```

Test using the proxy to make the request:
```sh
curl --location 'http://0.0.0.0:4000/chat/completions' \
  --header 'Content-Type: application/json' \
  --header "Authorization: Bearer $LITELLM_MASTER_KEY" \
  --data '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

Test the raw openai endpoint :
```sh
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

Generate a virtual key so we dont use the master:

```sh
export VIRTUAL_KEY=$(curl -s 'http://0.0.0.0:4000/key/generate' \
  --header 'Content-Type: application/json' \
  --header "Authorization: Bearer $LITELLM_MASTER_KEY" \
  --data-raw '{"models": ["gpt-4"], "metadata": {"user": "antoine.gerardin@gmail.com"}}' | jq -r '.key')
```

Can now run our model with the virtual key 

```sh
curl --location 'http://0.0.0.0:4000/chat/completions' \
  --header 'Content-Type: application/json' \
  --header "Authorization: Bearer $VIRTUAL_KEY" \
  --data '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

Cannot run uanallowed endpoint:

```sh
curl --location 'http://0.0.0.0:4000/chat/completions' \
  --header 'Content-Type: application/json' \
  --header "Authorization: Bearer $VIRTUAL_KEY" \
  --data '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```


Check spending for this key:


```sh
curl "http://0.0.0.0:4000/key/info?key=$VIRTUAL_KEY" \
     -X GET \
     -H "Authorization: Bearer $LITELLM_MASTER_KEY"
```

Delete the virtual key:

```sh
curl 'http://0.0.0.0:4000/key/delete' \
  --header 'Content-Type: application/json' \
  --header "Authorization: Bearer $LITELLM_MASTER_KEY" \
  --data-raw "{\"keys\": [\"$VIRTUAL_KEY\"]}"
```