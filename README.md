TO RUN:
1) Create a schema in your MySQL server named 'dtbank'
2) pip install -r requirements.txt
3) run the command "set FLASK_ENV=development" for Windows "export FLASK_ENV=development" for Mac and Linux
4) run the command "set FLASK_APP=main" for Windows "export FLASK_APP=main" for Mac and Linux
5) configure the lines between 10-13 according to your local MySQL server.
6) create a schema named "dtbank"
7) select "dtbank" as a default schema.
8) run the command "flask run"
9) send a get request to localhost:5000/add-data-to-db
10) wait before data is imported to MySQL server.
11) go to http://localhost:5000/