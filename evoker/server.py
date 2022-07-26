from os import getenv
import asyncio
import concurrent.futures
from time import thread_time

from sanic import Sanic, json

import errors

print("loading model...")
import predict

app = Sanic("evoker")
app.config.FALLBACK_ERROR_FORMAT = "json"

thread_pool = concurrent.futures.ProcessPoolExecutor()

@app.route("/")
async def index(request):
    return json({
        "Hello": "World"
    })

@app.route("/predict", methods=["POST"])
async def predict_prompt(request):
    loop = asyncio.get_event_loop()

    if "prompt" not in request.json:
        raise errors.InvalidRequest(extra={"missing": "prompt"})

    if "amount" not in request.json:
        request.json["amount"] = 1
    elif request.json["amount"] < 1 or request.json["amount"] > 10:
        raise errors.InvalidAmountError()

    # start the blocking call
    result = await loop.run_in_executor(thread_pool, predict.predict, request.json["prompt"], request.json["amount"])
    return json({
        "predictions": result
    })

def main():
    app.run(host=getenv("HOST", "0.0.0.0"), port=int(getenv("PORT", "8000")), debug=getenv("DEBUG", None) is not None)