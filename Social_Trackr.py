import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests

class SocialTrackrApp:
    ACCESS_TOKEN = "EAAPlSSixUWABO1U3lBVTtjfO05ciNOIMqpPN2oTMnFbtBypDIyi4nMaHCPVsChAFZCkaZAYuSxshdnkjd2s8Jnzm8glvs64k0Rp7KbPgL3wJ7yk1Qoq17vWi0eZBYbJCYw1Rz2aoIJV61yLPXFm3iVGj0jznQvZBz3zuTaR6nzMKUuesiStNvm8JLaNr6I2iIQZDZD"

    def __init__(self, root):
        """Initialize the main application window."""
        self.root = root
        self.root.title("Social Trackr")
        self.root.geometry("600x500")

        # Load background image
        self.bg_image = Image.open("background.jpg").resize((600, 500), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Welcome Screen
        self.frame_main = ttk.Frame(root, padding=20)
        self.frame_main.pack(fill="both", expand=True)

        label_welcome = ttk.Label(self.frame_main, text="Welcome to Social Trackr!", font=("Helvetica", 18))
        label_welcome.pack(pady=10)

        label_instruction = ttk.Label(
            self.frame_main,
            text="Choose a platform below to track data:",
            font=("Helvetica", 12),
        )
        label_instruction.pack(pady=5)

        self.platforms = ["Facebook", "Instagram", "Youtube", "X (Twitter)"]
        self.combo_platform = ttk.Combobox(self.frame_main, values=self.platforms, state="readonly")
        self.combo_platform.set("Pick a Platform")
        self.combo_platform.pack(pady=10)

        btn_next = ttk.Button(self.frame_main, text="Proceed", command=self.open_platform_window)
        btn_next.pack(pady=5)

        btn_exit = ttk.Button(self.frame_main, text="Exit", command=self.exit_app)
        btn_exit.pack(pady=5)

    def fetch_data(self, platform, user_id, result_label):
        # Fetch data based on user inpu5 and update the result label
        if not user_id:
            messagebox.showerror("Error", "Please enter a User ID!")
            return

        if platform == "Facebook":
        # Graph API URL to fetch Facebook user data
            url = f"https://graph.facebook.com/v12.0/{user_id}"
            params = {
                "fields": "name,id,friends.limit(1).summary(true),posts.limit(5){message,created_time}",
                "access_token": self.ACCESS_TOKEN,
            }

            try:
                response = requests.get(url, params=params)
                response.raise_for_status()  # Raise exception for bad status codes
                data = response.json()

                # Display user stats
                name = data.get("name", "N/A")
                user_id = data.get("id", "N/A")
                friends_count = data.get("friends", {}).get("summary", {}).get("total_count", "N/A")
                posts = data.get("posts", {}).get("data", [])

                posts_text = "\n".join(
                    [f"- {post['message'][:50]}... ({post['created_time']})" for post in posts if "message" in post]
                )

                result_text = (
                    f"Name: {name}\n"
                    f"User ID: {user_id}\n"
                    f"Friends: {friends_count}\n\n"
                    f"Recent Posts:\n{posts_text if posts else 'No recent posts available.'}"
                )

                # Open a window for results
                self.show_results_window(platform, result_text)

            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Failed to fetch data: {e}")

            except KeyError:
                messagebox.showerror("Error", "Invalid response from API. Check User ID or token.")
        else:
            messagebox.showinfo("Info", f"Fetching data for {platform} is not implemented yet.")

    def show_results_window(self,platform, result_text):
        # Display the fetched results in a new window
        results_window = tk.Toplevel(self.root)
        results_window.title(f"{platform} Data Results")
        results_window.geometry("600x400")

        label_header = ttk.Label(
            results_window, text=f"{platform} Data Results", font=("Helvetica", 16), anchor="center"
        )
        label_header.pack(pady=10)

        # Create a scrollable text widget for displaying results
        text_widget = tk.Text(results_window, wrap="word", font=("Helvetica", 24))
        text_widget.insert("1.0",result_text)
        text_widget.configure(state="disabled") # Make the text widget read-only
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)

        # Add a close button
        btn_close = ttk.Button(results_window, text="Close", command=results_window.destroy)
        btn_close.pack(pady=5)

    def open_platform_window(self):
        """Open a new window based on the selected platform."""
        platform = self.combo_platform.get()

        if platform not in self.platforms:
            messagebox.showerror("Error", "Please select a valid platform!")
            return

        new_window = tk.Toplevel(self.root)
        new_window.title(f"{platform} Data Tracker")
        new_window.geometry("600x500")

        # Labels
        label_header = ttk.Label(new_window, text=f"Track {platform} Data", font=("Helvetica", 16))
        label_header.pack(pady=10)

        label_instruction = ttk.Label(
            new_window,
            text="Enter your User ID to retrieve data:",
            font=("Helvetica", 12),
        )
        label_instruction.pack(pady=5)

        # Entry Box
        entry_user_id = ttk.Entry(new_window, width=30)
        entry_user_id.pack(pady=5)

        # Result Label 
        result_label = ttk.Label(new_window, text="", font=("Helvetica", 10), justify="left")
        result_label.pack(pady=10)

        # Buttons
        btn_fetch = ttk.Button(
            new_window,
            text="Fetch Data",
            command=lambda: self.fetch_data(platform, entry_user_id.get(), new_window),
        )
        btn_fetch.pack(pady=5)

        btn_back = ttk.Button(new_window, text="Back", command=new_window.destroy)
        btn_back.pack(pady=5)

    def exit_app(self):
        # Exit the application
        confirm = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if confirm:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SocialTrackrApp(root)
    root.mainloop()