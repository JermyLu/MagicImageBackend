from app import app, uvicorn
from app_gradio import demo

uvicorn.run(app, host="0.0.0.0", port=8000)
demo.queue()  # <-- Sets up a queue with default parameters
demo.launch(share=True)