import toga
from toga.style import Pack
from toga.style.pack import COLUMN
import threading
import uvicorn
import time
from wmax.app import app

class WMAX(toga.App):
    def startup(self):
        # Start uvicorn server in the background
        self.server_thread = threading.Thread(target=self.start_server, daemon=True)
        self.server_thread.start()
        
        main_box = toga.Box(style=Pack(direction=COLUMN))
        self.webview = toga.WebView(style=Pack(flex=1))
        main_box.add(self.webview)
        
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
        
        # Add background task to load the UI once the server starts
        self.add_background_task(self.load_url)

    def start_server(self):
        config = uvicorn.Config(app, host="127.0.0.1", port=8372, log_config=None)
        server = uvicorn.Server(config)
        server.run()
        
    async def load_url(self, widget, **kwargs):
        import asyncio
        await asyncio.sleep(1.5)
        self.webview.url = "http://127.0.0.1:8372"

def main():
    return WMAX()
