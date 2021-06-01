# Learning FastAPI from Youtube

![Logo](https://github.com/LearningWebDevelopment/FastAPI_Youtube_BitFumes/blob/main/logo.png "Logo Title Text 1")

[Youtube Link](https://www.youtube.com/watch?v=7t2alSnE2-I "Youtube link")-------[FastAPI Link](https://fastapi.tiangolo.com/ "FastApi Link")

## Getting Started  

### Setup & Install  

`$ pip install fastapi`
`$ pip install uvicorn[standard]`

Create a file **main.py**

### Run Server

`uvicorn main:app --reload`

@app.get('/') - path operation decorator
app name - operation - path
path operation function

#### Dynamic Routing

```python
@app.get('/blog/{id}')
def show(id):
    return {
        'data': id
    }
```  

### API Docs  

**Swagger Doc**
`http://127.0.0.1:8000/docs`  

**ReDoc**  
`http://127.0.0.1:8000/redoc`

Path parameter, Query Parameter, Optional Parameter

Post requires a data model and function parameter is model instance

### Change Port

```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run:
`python3 main.py`

### Pydantic Schema & SQL Alchemy

[SQL_Alchemy Link](https://docs.sqlalchemy.org/en/14/tutorial/engine.html)
Create connection to DB SQLite

### Model & Table  

1. created database.py - connection to db
2. models.py - table name and structure
3. main.py - model db creation

#### Store data to DB

### Exception & Status Code

### Relationship

### API Router
