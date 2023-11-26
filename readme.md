# Football manager app project

## How to start

1. Start your virutal enviroment with `source Scripts\activate` command
2. Run `pip install -r requirements.txt` command
3. Finally run `python fapp/manage.py runserver`

## Database connection

To connect project to database you need to create `fapp\secrets.json` file and add there:
`{
  "DB_PASSWORD": "db_api"
}`
