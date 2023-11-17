import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import threading
from main import VoiceAssistant

class VoiceAssistantGUI:
    def __init__(self, master):
        self.master = master
        master.title("Voice Assistant")

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=40, height=10)
        self.text_area.pack(padx=10, pady=10)

        self.listen_button = ttk.Button(master, text="Listen", command=self.listen_thread)
        self.listen_button.pack(pady=5)

        self.stop_button = ttk.Button(master, text="Stop", command=self.stop_listening)
        self.stop_button.pack(pady=5)
        self.stop_button["state"] = "disabled"

        self.voice_assistant = VoiceAssistant()

    def listen_thread(self):
        self.listen_button["state"] = "disabled"
        self.stop_button["state"] = "normal"
        threading.Thread(target=self.voice_assistant.listen).start()

    def stop_listening(self):
        self.voice_assistant.stop_listening()
        self.listen_button["state"] = "normal"
        self.stop_button["state"] = "disabled"

    def listen(self):
        statement = self.voice_assistant.take_command()
        self.text_area.insert(tk.END, f"User: {statement}\n")
        self.text_area.yview(tk.END)

        self.voice_assistant.perform_task(statement)

        self.stop_listening()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    root.mainloop()
