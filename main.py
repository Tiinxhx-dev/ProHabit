from fastapi import FastAPI, Request, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from controler.user import User
from lib.check_user import check_user

app = FastAPI()

template = Jinja2Templates(directory="./view")

@app.api_route("/",  methods=["GET", "POST"], response_class=HTMLResponse)
def root(req: Request):
    if req.method == "POST":
        
        return RedirectResponse(url="/", status_code=303)
    
    return template.TemplateResponse("index.html", {"request": req})

@app.get("/signup", response_class=HTMLResponse)
def singup(req: Request):
    return template.TemplateResponse("signup.html", {"request": req})


@app.get("/user", response_class=HTMLResponse)
def user(req: Request):
    return RedirectResponse("/")
    #return template.TemplateResponse("user.html", {"request": req, "data_user": req})

@app.post("/user", response_class=HTMLResponse)
def user(req: Request, email: str = Form(),password: str = Form()):
    verify = check_user(email, password)
    if verify:
        return template.TemplateResponse("user.html", {"request": req, "data_user": req, "data_user": verify})
    return RedirectResponse("/") 


@app.post("/data-processing")
def data_processing(firstname: str = Form(), lastname: str = Form(), email: str = Form(), password: str = Form()):
    data_user = {
       "firstname": firstname,
       "lastname": lastname,
       "email": email,
       "password": password
    }
    db = User(data_user)
    db.create_user()
   
    return RedirectResponse("/")