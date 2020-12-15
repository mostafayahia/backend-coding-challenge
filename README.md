# Backend-Coding-Challenge
It is a [backend-coding-challenge](https://github.com/gemography/backend-coding-challenge). My task was to implement an endpoint api to get trending repos in github and classify them by language.

### Getting Started

#### Run app locally
- install all packages needed to run the app `pip3 install -r requirements.txt`
- then you can run the following commands (from the root directory)
```
export FLASK_APP=app.py 
export FLASK_ENV=development
flask run
```
The default url: `http://localhost:5000`

#### Tests
- you can run the following command (from the root directory)
```
python3 test_app.py
```

### API Reference
#### Getting Started
Base URL: you can run locally `http://localhost:5000`
<br>
Authentication: No authentication needed at the current point.
#### Error Handling
Errors are returned as JSON objects in the following format:
```
{
  "success": false,
  "error": 404,
  "message": "Resource Not Found"
}
```
types of errors:
- 404: Resource Not Found
- 500: Internal Server Error

### Endpoints
#### GET /trending_repos
- ##### General:
  - Return a list of repos classified by each language and a success value.
  - `repos_num` is a query param to control the number of repos which will get classified.
  - `repos_num` query param can **not** exceed the `MAX_PER_PAGE` value which exists in `github_query_params.py`.
  - if `repos_num` is not given, the default value will be `PER_PAGE` value which exists in `github_query_params.py`
- `curl -X GET 'http://localhost:5000/trending_repos?repos_num=10'`
```
{
  "repos": [
    {
      "count": 3, 
      "language": "python", 
      "repos": [
        "https://github.com/beurtschipper/Depix", 
        "https://github.com/benwilber/boltstream", 
        "https://github.com/r0ysue/r0capture"
      ]
    }, 
    {
      "count": 1, 
      "language": "yara", 
      "repos": [
        "https://github.com/fireeye/red_team_tool_countermeasures"
      ]
    }, 
    {
      "count": 1, 
      "language": "css", 
      "repos": [
        "https://github.com/bradtraversy/50projects50days"
      ]
    }, 
    {
      "count": 1, 
      "language": "typescript", 
      "repos": [
        "https://github.com/getmeli/meli"
      ]
    }, 
    {
      "count": 1, 
      "language": "html", 
      "repos": [
        "https://github.com/bobbyiliev/introduction-to-bash-scripting"
      ]
    }
  ], 
  "success": true
}
```
