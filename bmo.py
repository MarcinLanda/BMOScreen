import tkinter as tk
from datetime import datetime

class BMOApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("480x320")
        self.overrideredirect(True) # Removes borders for full-screen arcade feel
        self.configure(bg="#36AE7C") # Classic BMO Green

        self.container = tk.Frame(self, bg="#36AE7C")
        self.container.pack(fill="both", expand=True)

        self.show_idle_screen()

    def clear_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # --- 1. IDLE SCREEN ---
    def show_idle_screen(self):
        self.clear_screen()
        
        canvas = tk.Canvas(self.container, width=480, height=200, bg="#36AE7C", highlightthickness=0)
        canvas.pack(pady=10)

        # BMO Face
        canvas.create_oval(130, 60, 170, 110, fill="black") # Left Eye
        canvas.create_oval(310, 60, 350, 110, fill="black") # Right Eye
        canvas.create_arc(200, 90, 280, 140, start=0, extent=-180, fill="black") # Mouth

        # Navigation Buttons
        btn_frame = tk.Frame(self.container, bg="#36AE7C")
        btn_frame.pack(side="bottom", pady=20)

        cal_btn = tk.Button(btn_frame, text="📅 Calendar", command=self.show_calendar_screen, font=("Arial", 11), bg="#EB5353", fg="white")
        cal_btn.pack(side="left", padx=15)

        sports_btn = tk.Button(btn_frame, text="⚾ Chicago Sports", command=self.show_sports_screen, font=("Arial", 11), bg="#F9D923", fg="black")
        sports_btn.pack(side="left", padx=15)

    # --- 2. CALENDAR MODE ---
    def show_calendar_screen(self):
        self.clear_screen()
        
        tk.Label(self.container, text=datetime.now().strftime("%B %Y"), font=("Arial", 14, "bold"), bg="#36AE7C", fg="white").pack(pady=5)

        grid_frame = tk.Frame(self.container, bg="#36AE7C")
        grid_frame.pack()

        for i in range(1, 32):
            day_btn = tk.Button(grid_frame, text=str(i), width=3, height=1, 
                                command=lambda d=i: self.open_day_view(d))
            day_btn.grid(row=(i-1)//7, column=(i-1)%7, padx=2, pady=2)

        tk.Button(self.container, text="🔙 Back", command=self.show_idle_screen, bg="#EB5353", fg="white", font=("Arial", 10)).pack(side="bottom", pady=10)

    def open_day_view(self, day):
        top = tk.Toplevel(self)
        top.geometry("300x180")
        top.title(f"Day {day}")
        tk.Label(top, text=f"Events / Notes for Day {day}", font=("Arial", 11)).pack(pady=20)
        tk.Button(top, text="Close", command=top.destroy).pack()

    # --- 3. SPORTS SCHEDULE MODE ---
    def show_sports_screen(self):
        self.clear_screen()
        
        tk.Label(self.container, text="Chicago Sports Schedule", font=("Arial", 13, "bold"), bg="#36AE7C", fg="white").pack(pady=5)

        score_text = tk.Text(self.container, width=45, height=8, bg="#2d9167", fg="white", font=("Arial", 9))
        score_text.pack(pady=5)
        score_text.insert("1.0", "Loading Chicago Teams...\n- Cubs / White Sox: Check ESPN API\n- Bulls / Blackhawks: Upcoming Games")
        score_text.config(state="disabled")

        tk.Button(self.container, text="🔙 Back", command=self.show_idle_screen, bg="#EB5353", fg="white", font=("Arial", 10)).pack(side="bottom", pady=5)

if __name__ == "__main__":
    app = BMOApp()
    app.mainloop()
