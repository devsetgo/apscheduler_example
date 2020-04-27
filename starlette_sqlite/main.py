from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, WebSocketRoute

import math_func
import scheduled_tasks


async def homepage(request):
    result: dict = {
        "status": "hello world",
        "method": request.method,
        "url_path": request.url.path,
        "client_host": request.client.host,
    }
    return JSONResponse(result)


async def math_page(request):
    stats = await math_func.run_stats()

    return JSONResponse(stats)


async def websocket_endpoint(websocket):
    await websocket.accept()
    await websocket.send_text("Hello, websocket!")
    await websocket.close()


def startup():
    print("Ready to go")
    # add tasks on startup
    scheduled_tasks.start_jobs()


def shutdown():

    # remove scheduled tasks on shutdown
    scheduled_tasks.shut_down_schedule()
    print("and we are done")


routes = [
    Route("/", homepage),
    Route("/math", math_page),
    WebSocketRoute("/ws", websocket_endpoint),
    # Mount("/static", StaticFiles(directory="static")),
]

app = Starlette(debug=True, routes=routes, on_startup=[startup], on_shutdown=[shutdown])


if __name__ == "__main__":
    import uvicorn

    # APScheduler is limited to running on a single worker at this this time (v3.6.3)
    # see https://github.com/agronholm/apscheduler/issues/218#issuecomment-559951948 for more information
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="debug", workers=1)
    # or use in the command prompt 'uvicorn main:app --port 5000 --reload --log-level debug'
