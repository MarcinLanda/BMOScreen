import tkinter as tk
import urllib.request
import json
import threading
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
        
        tk.Label(self.container, text="Chicago Sports Schedule", font=("Arial", 12, "bold"), bg="#36AE7C", fg="white").pack(pady=2)

        # Create the text widget to display scores
        self.score_text = tk.Text(self.container, width=50, height=8, bg="#2d9167", fg="white", font=("Arial", 9))
        self.score_text.pack(pady=2)
        
        self.score_text.insert("1.0", "Fetching live Chicago sports data...\nPlease wait...")
        self.score_text.config(state="disabled")

        tk.Button(self.container, text="🔙 Back", command=self.show_idle_screen, bg="#EB5353", fg="white", font=("Arial", 9, "bold")).pack(side="bottom", pady=5)

        # Start background thread so the UI doesn't freeze during the web request
        threading.Thread(target=self.fetch_chicago_sports, daemon=True).start()

def fetch_chicago_sports(self):
    try:
        # Using ESPN's public scoreboard feeds (Cubs/Sox/Bulls/Blackhawks)
        urls = {
            "MLB": "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard",
            "NBA": "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard",
            "NHL": "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard"
        }
        
        chicago_teams = ["Cubs", "White Sox", "Bulls", "Blackhawks"]
        results = []

        for league, url in urls.items():
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                
                for event in data.get("events", []):
                    name = event.get("name", "")
                    # Check if any Chicago team is playing in this event
                    if any(team in name for team in chicago_teams):
                        status = event["status"]["type"]["description"]
                        results.append(f"• {name} [{status}]")

        if not results:
            output = "No live Chicago games found right now.\nCheck back later for upcoming schedules!"
        else:
            output = "\n".join(results[:5]) # Limit lines to fit 3.5" screen

    except Exception as e:
        output = f"Could not load sports data.\nCheck Raspberry Pi internet connection."

    # Safely update the Tkinter Text widget from the main UI thread
    self.after(0, lambda: self.update_score_display(output))

def update_score_display(self, text):
    self.score_text.config(state="normal")
    self.score_text.delete("1.0", tk.END)
    self.score_text.insert("1.0", text)
    self.score_text.config(state="disabled")

if __name__ == "__main__":
    app = BMOApp()
    app.mainloop()
