import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.app import get_application

app = get_application()

# Add a root endpoint to redirect to Swagger documentation
@app.get("/", include_in_schema=False)  # Exclude this route from Swagger docs
def redirect_to_docs():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run("main:app", debug=True, reload=True, port=8080)
