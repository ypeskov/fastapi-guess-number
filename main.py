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
current_number: int = round((MAX_NUMBER - MIN_NUMBER) / 2)
prev_low: int = MIN_NUMBER
prev_high: int = MAX_NUMBER


@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    global current_number, number_of_attempts, prev_low, prev_high
    number_of_attempts = INITIAL_ATTEMPT
    current_number = round((MAX_NUMBER - MIN_NUMBER) / 2)
    prev_low = MIN_NUMBER
    prev_high = MAX_NUMBER

    context = { 'request': request}
    return templates.TemplateResponse('home.html', context=context)

@app.get('/attempt', response_class=HTMLResponse)
async def make_attempt_to_guess(request: Request, guessed: str = None):
    global number_of_attempts, current_number, prev_low, prev_high
    context = { 'request': request }
    
    if guessed == 'yes':
        tpl = 'victory.html'
        context['number_of_attempts'] = number_of_attempts
    else:
        tpl = 'attempt_failed.html'
        
        if number_of_attempts > INITIAL_ATTEMPT:
            if guessed == 'less':
                prev_high = current_number
                current_number = round((prev_high - prev_low) / 2) + prev_low
            elif guessed == 'bigger':
                prev_low = current_number
                current_number = round(prev_high - (prev_high - current_number)/2 )
    
    number_of_attempts += 1

    context['number'] = current_number

    return templates.TemplateResponse(tpl, context=context)
