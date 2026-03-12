from __future__ import annotations

import queue
import threading
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import messagebox

from werkzeug.serving import make_server

from app import DOWNLOADS_DIR, create_app


HOST = "127.0.0.1"
PORT = 5001
APP_URL = f"http://{HOST}:{PORT}"


class DesktopServer:
    def __init__(self) -> None:
        self.app = create_app()
        self.server = make_server(HOST, PORT, self.app, threaded=True)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        self.server.shutdown()
        self.thread.join(timeout=2)


class DesktopApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Video to MP3 Studio")
        self.root.geometry("520x360")
        self.root.minsize(520, 360)
        self.root.configure(bg="#eef3f6")

        self.server: DesktopServer | None = None
        self.events: queue.Queue[str] = queue.Queue()

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.after(100, self._start_server)
        self.root.after(150, self._drain_events)

    def _build_ui(self) -> None:
        frame = tk.Frame(self.root, bg="#ffffff", padx=28, pady=28)
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.88, relheight=0.84)

        title = tk.Label(
            frame,
            text="Video to MP3 Studio",
            font=("Helvetica Neue", 24, "bold"),
            fg="#15202b",
            bg="#ffffff",
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            frame,
            text="A local Mac app that runs your converter and opens it in your browser.",
            font=("Helvetica Neue", 12),
            fg="#5d6b78",
            bg="#ffffff",
            wraplength=420,
            justify="left",
        )
        subtitle.pack(anchor="w", pady=(12, 18))

        self.status_var = tk.StringVar(value="Starting local server...")
        status = tk.Label(
            frame,
            textvariable=self.status_var,
            font=("Helvetica Neue", 12),
            fg="#1b6b67",
            bg="#e9f6f5",
            padx=14,
            pady=12,
            justify="left",
            wraplength=420,
        )
        status.pack(fill="x")

        downloads_text = f"Downloads folder:\n{DOWNLOADS_DIR}"
        downloads = tk.Label(
            frame,
            text=downloads_text,
            font=("Helvetica Neue", 11),
            fg="#4f5b66",
            bg="#ffffff",
            justify="left",
            wraplength=420,
        )
        downloads.pack(anchor="w", pady=(18, 22))

        button_row = tk.Frame(frame, bg="#ffffff")
        button_row.pack(fill="x", pady=(6, 0))

        open_button = tk.Button(
            button_row,
            text="Open Converter",
            command=self.open_browser,
            font=("Helvetica Neue", 12, "bold"),
            bg="#1e847f",
            fg="white",
            activebackground="#166762",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2",
        )
        open_button.pack(side="left")

        quit_button = tk.Button(
            button_row,
            text="Quit",
            command=self.close,
            font=("Helvetica Neue", 12),
            bg="#edf1f3",
            fg="#25313b",
            activebackground="#dfe5e9",
            activeforeground="#25313b",
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2",
        )
        quit_button.pack(side="right")

        helper = tk.Label(
            frame,
            text="Keep this window open while you use the converter.",
            font=("Helvetica Neue", 10),
            fg="#7a8792",
            bg="#ffffff",
        )
        helper.pack(anchor="w", pady=(18, 0))

    def _start_server(self) -> None:
        try:
            self.server = DesktopServer()
            self.server.start()
        except OSError:
            self.status_var.set("Port 5001 is already in use. Close the other app and reopen this one.")
            return
        except Exception as exc:
            self.status_var.set(f"Could not start the app: {exc}")
            return

        self.events.put("ready")

    def _drain_events(self) -> None:
        while not self.events.empty():
            event = self.events.get()
            if event == "ready":
                self.status_var.set("Server is ready. Opening the converter in your browser...")
                self.open_browser()

        self.root.after(150, self._drain_events)

    def open_browser(self) -> None:
        webbrowser.open(APP_URL)
        self.status_var.set("Converter is running at http://127.0.0.1:5001")

    def close(self) -> None:
        try:
            if self.server:
                self.server.stop()
        except Exception:
            pass
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    try:
        DesktopApp().run()
    except Exception as exc:
        messagebox.showerror("Video to MP3 Studio", str(exc))
