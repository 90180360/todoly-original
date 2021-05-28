* Clone/Download the project

* Create a database and add the tables
  ``` 
  createdb -h localhost -p 5432 -U postgres todoly
  psql -h localhost -p 5432 -U postgres -d todoly -f pg.sql
  ```

* Create a virtual environment
  ```
  python -m venv venv
  source venv/bin/activate
  ```
  
* Install all the requirements
  ``` 
  pip install -r requirements.txt
  ```

* Set the environment variables
  ``` 
  export DATABASE_URL=postgresql://USERNAME:PASSWORD@HOST/todoly
  export SECRET_KEY=YOUR_SECRET_KEY
  ```

* Run the project
  ```
  python run.py
  ```
