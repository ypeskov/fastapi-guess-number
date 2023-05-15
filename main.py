from pprint import pprint

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')

MIN_NUMBER = 1
MAX_NUMBER = 100
INITIAL_ATTEMPT = 1
number_of_attempts: int = INITIAL_ATTEMPT
current_number: int = round(MAX_NUMBER / 2)

@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    context = { 'request': request}
    return templates.TemplateResponse('home.html', context=context)

@app.get('/attempt', response_class=HTMLResponse)
async def make_attempt_to_guess(request: Request, guessed: str = None):
    global number_of_attempts, current_number
    context = { 'request': request }
    
    if guessed == 'yes':
        tpl = 'victory.html'
    else:
        tpl = 'attempt_failed.html'
        if number_of_attempts > INITIAL_ATTEMPT:
            current_number = round(current_number / 2)
        number_of_attempts += 1

    context['number'] = current_number

    return templates.TemplateResponse(tpl, context=context)
