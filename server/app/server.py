from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain_core.runnables import chain
from graph.app import app as graph_app
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Edit this to add the chain you want to add
@chain
def custom_chain(text):
  input = {"question": text}
  return graph_app.invoke(input)["generation"]
add_routes(
    app,
    custom_chain.with_types(input_type=str, output_type=str),
    path="/openai",
    
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
