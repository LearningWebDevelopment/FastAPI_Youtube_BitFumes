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
