import customtkinter as ctk
from lorem_text import lorem


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        self.title("Typing Speed Test Application")
        self.geometry("800x350")

        self.text = self.get_random_text(length=15)
        self.time_left = 30
        self.mistakes = 0
        self.wpm = 0
        self.start_timer = False

        self.title_text = ctk.CTkLabel(
            master=self, text="Typing Speed Test Game.", font=("Cascadia Code Bold", 24)
        )
        self.title_text.grid(row=0, column=0, padx=20, pady=10)

        self.frame = ctk.CTkFrame(self)

        self.time_left_label = ctk.CTkLabel(
            master=self.frame,
            text=f"Time left: {self.time_left}s |",
            font=("Cascadia Mono", 16),
        )
        self.time_left_label.grid(row=0, column=0, padx=10)
        self.mistake_label = ctk.CTkLabel(
            master=self.frame,
            text=f"Mistakes: {self.mistakes} |",
            font=("Cascadia Mono", 16),
        )
        self.mistake_label.grid(row=0, column=1, padx=10)
        self.wpm_label = ctk.CTkLabel(
            master=self.frame, text=f"WPM: {self.wpm} |", font=("Cascadia Mono", 16)
        )
        self.wpm_label.grid(row=0, column=2, padx=10)
        self.cpm_label = ctk.CTkLabel(
            master=self.frame, text=f"CPM: 0 |", font=("Cascadia Mono", 16)
        )
        self.cpm_label.grid(row=0, column=3, padx=10)

        self.reset_btn = ctk.CTkButton(
            master=self.frame, text="Try Again", command=self.reset
        )
        self.reset_btn.grid(row=0, column=4)

        self.frame.grid(row=1, column=0, padx=20, pady=10)

        self.display_text = ctk.CTkTextbox(
            master=self,
            width=600,
            height=100,
            font=("Cascadia Code SemiLight", 20),
            wrap="word",
        )
        self.display_text.grid(row=2, column=0, padx=50, pady=10, sticky="nsew")
        self.display_text.insert("1.0", text=self.text)
        self.display_text.configure(state="disabled")

        self.typing_area = ctk.CTkEntry(
            master=self, width=600, font=("Cascadia Mono", 16)
        )
        self.typing_area.grid(row=3, column=0)
        self.typing_area.bind("<KeyRelease>", self.start_time)

        self.mainloop()

    def start_time(self, event):
        if not self.start_timer:
            self.start_timer = True
            self.update_timer()

        self.typing_check(event)

    def update_timer(self):
        if self.start_timer and self.time_left > 0:
            self.time_left -= 1
            self.time_left_label.configure(text=f"Time Left: {self.time_left}s |")
            self.after(1000, self.update_timer)
        else:
            self.typing_area.configure(state="disabled")

    def typing_check(self, event):
        input_text = self.typing_area.get()

        if input_text and event.keysym not in [
            "Shift_L",
            "Shift_R",
            "Control_L",
            "Control_R",
            "Alt_L",
            "Alt_R",
            "Caps_Lock",
        ]:
            self.display_text.tag_remove("correct", "1.0", "end")
            self.display_text.tag_remove("wrong", "1.0", "end")
            self.mistakes = 0
            correct_chars = 0

            for i in range(min(len(input_text), len(self.text))):
                char = input_text[i]
                if char == self.text[i]:
                    self.display_text.tag_add("correct", f"1.{i}", f"1.{i+1}")
                    correct_chars += 1
                else:
                    self.mistakes += 1
                    self.mistake_label.configure(text=f"Mistakes: {self.mistakes}|")
                    self.display_text.tag_add("wrong", f"1.{i}", f"1.{i+1}")

            self.display_text.tag_config(tagName="correct", foreground="green")
            self.display_text.tag_config(tagName="wrong", foreground="red")

            words_typed = len(input_text.split())
            self.wpm = (words_typed / (30 - self.time_left)) * 60
            self.wpm_label.configure(text=f"WPM: {int(self.wpm)}")

            cpm = (correct_chars / (30 - self.time_left)) * 60
            self.cpm_label.configure(text=f"CPM: {int(cpm)}")

            # Disable typing area if the whole text is typed
            if len(input_text) >= len(self.text):
                self.typing_area.configure(state="disabled")
                self.time_left_label.configure(text=f"Time Left: {self.time_left}s |")
                self.time_left = 0

    def get_random_text(self, length: int):
        random_text = lorem.words(length)
        return random_text

    def reset(self):
        self.time_left = 30
        self.mistakes = 0
        self.wpm = 0
        self.start_timer = False

        self.time_left_label.configure(text=f"Time Left: {self.time_left}s |")
        self.mistake_label.configure(text=f"Mistakes: {self.mistakes} |")
        self.wpm_label.configure(text=f"WPM: {self.wpm} |")
        self.cpm_label.configure(text="CPM: 0 |")

        self.typing_area.configure(state="normal")
        self.typing_area.delete(0, "end")
        self.display_text.tag_remove("correct", "1.0", "end")
        self.display_text.tag_remove("wrong", "1.0", "end")


App()
