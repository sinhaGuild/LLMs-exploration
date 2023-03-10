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
git push heroku main # push to heroku
heroku apps:destroy --app <appName>

```

## Sample Queries

### Basic

How many unique business names are registered with San Francisco Food health investigation organization ?

_Projected Query_

```sql
 COUNT(DISTINCT(name)) as "unique resturant name count" FROM businesses
```

How many businesses are there in San Francisco where their owners live in the same area (postal code/ zip code) as the business is located?

_Projected Query_

```sql
SELECT COUNT(business_id) from businesses WHERE postal_code = owner_zip
```

What is the earliest and latest date a health investigation is recorded in this database.

_Projected Query_

```sql
SELECT MIN(date), MAX(date) FROM inspections
```

### Aggregation

Find the restaurant owners (owner\*name) that own the most restaurants, and the number of restaurants (num_restaurants) they own. Return the top 10 owners, ordered by descending order using the number of restaurants.

_Projected Query_

```sql
SELECT
        owner_name, COUNT(business_id) as "num_restaurants"
    FROM
        businesses
    GROUP BY
        owner_name
    ORDER BY
        num_restaurants DESC
    LIMIT 10
```

What is the average score given to restaurants based on the type of inspection? Based on the results, identify the types of inspections that are not scored (NULL). The 'average_score' is rounded to one decimal. The results are sorted in ascending order based on the average score.

_Projected Query_

```sql
SELECT
        type, ROUND(AVG(score), 1) as "average score"
    FROM
        inspections
    WHERE
       score <> 'None'
    GROUP BY
        type
    ORDER BY
        "average score"
```

### Joins

From the businesses table, selects the top 10 most popular postal_codes.They are filtered to only count the restaurants owned by people/entities that own 5 or more restaurants. The result returns a row (postal_code, frequency) for each 10 selections, sorted by descending order to get the most relevant zip codes.

_Projected Query_

```sql
 SELECT
        b1.postal_code, COUNT(b1.business_id) as "count"
    FROM
        businesses as b1
    WHERE
        b1.owner_name IN
    (
    SELECT
        b2.owner_name
    FROM
        businesses as b2
    GROUP BY
        b2.owner_name
    HAVING COUNT(b2.business_id) > 4
    )
    GROUP BY
        b1.postal_code
    ORDER BY
        count DESC
    LIMIT 10
```

How many times restaurants in Market street (postal_code: 94103) have committed health violations? Group them based on their risk category. The output is (risk_category, count as frequency) sorted in descending order by frequency.

_Projected Query_

```sql
SELECT
        risk_category, COUNT(v.business_id) as "frequency"
    FROM
        violations as v
    INNER JOIN
        businesses as b
    ON
        v.business_id = b.business_id

    WHERE (postal_code = '94103')
    GROUP BY
        risk_category
    ORDER BY
        frequency DESC
```
