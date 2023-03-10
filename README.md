# Using Transformer Models like ChatGPT to Introspect Databases.

## Packages used

- langchain
- fastapi
- openAPI
- seraphAPI
- dotenv (environment variables)
- heroku CLI

## Use cases

1. Natural language conversation with a relational database.
2. Conversations beyond ChatGPTs programming.

## Endpoints

| `#` | `ROUTE`              | `DESCRIPTION`                                                                                      |
| --- | -------------------- | -------------------------------------------------------------------------------------------------- |
| 1   | `base/healthcheck`   | Healthcheck                                                                                        |
| 2   | `db/sql`             | Database agent with natural language understanding. No ELT needed.                                 |
| 3   | `db/kb`              | Natural language QnA on a File/Custom Knowledge base.                                              |
| 4   | `/agent`             | GPT with access to internet and current events.                                                    |
| 5   | `/agent/self`        | model asks itself follow-up questions which can consult other external models.                     |
| 6   | `/agent/react`       | chain-of-thought prompting to generate an action plan. Anticipate and act.                         |
| 7   | `/agent/mrkl`        | Modular Reasoning, Knowledge and Language (method) to select gp tools for QnA.                     |
| 8   | `/agent/ensemble`    | inference chaining to compare results of multiple models.                                          |
| 9   | `/agent/ethics`      | filter toxic outputs by self-critiquing.                                                           |
| 10  | `/agent/ethics/yoda` | regenerate filtered outputs with flair                                                             |
| 11  | `/chain`             | simple sequential forward-fed chaining of language models. Single i/o.                             |
| 12  | `/chain/multi`       | more general form sequence - allows multiple inputs or outputs                                     |
| 13  | `/chain/mem`         | general purpose sequence with memory ie. information passed as context for each stage in the pipe. |
| 14  | `/chain/pal`         | Implements Program-Aided Language Models, as in https://arxiv.org/pdf/2211.10435.pdf.              |
| 15  | `/chat/`             | GPT3a                                                                                              |
| 16  | `/chat/gptx`         | GPT based agent streamlined for conversation (not just information).                               |
| 17  | `/chat/zero`         | Zero shot chatbot.                                                                                 |

## System Design parameters

- DRY
- Containarization for scalability to multi-model clusters.
- Deploy as an interactive documented endpoint
- ~~Batteries included~~

## How to use

1. Start the container

```sh
docker-compose up --detach
```

2. `Alternatively` you can build from source

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r local.requirements.txt
uvicorn app.main:app --reload
```

3. Navigate to [Docs Playground](http://localhost:8080/docs) and try out sample queries

```sh
http://localhost:8080/docs
```

4. Deployment

```sh

heroku create <appName> # First time only
heroku git:remote -a <appName> # add remote config for heroku
heroku config:set OPENAI_API_KEY='sk-2344720uu23d0u29384274b840c' # set environment variables
git add -A && git commit -m 'msg' # git lifecycle
heroku stack:set container
git push heroku main # push to heroku
heroku apps:destroy --app <appName>

```
