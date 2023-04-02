from app import *
from app_gradio import *

uvicorn.run(app, host="0.0.0.0", port=8000)
demo.launch(share=True)