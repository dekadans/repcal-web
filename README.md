
The source of the [repcal.info](https://repcal.info) website and REST API.

For the Python script for converting dates to the French Republican calendar, see [Repcal](https://github.com/dekadans/repcal).

## Build, Run & Test

Install and run the API:

```shell
python3 -m venv venv

source ./venv/bin/activate

pip install -r requirements.txt

flask --app main run --debug --port 8080
```

Install and build frontend code:

```shell
npm install --include=dev

npm run build
```

Run API tests:

```shell
REPCAL_HOST=http://localhost:8080 npm test
```