import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
import pygame
from keyboard import add_hotkey, remove_hotkey
import os
import pickle
import math


class SoundboardApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Soundboard")
        # Center the window on the screen
        width = 1000
        height = 700
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialize pygame mixer with optimal settings
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        # Initialize storage
        self.sounds = {}  # {file_path: pygame.mixer.Sound}
        self.channels = {}  # {file_path: channel}
        self.ui_elements = {}  # {file_path: {'button': button, 'indicator': indicator}}
        self.loop_vars = {}  # {file_path: BooleanVar}
        self.fade_vars = {}  # {file_path: BooleanVar}
        self.volume_vars = {}  # Store volume values

        self.setup_ui()

    def setup_ui(self):
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header with title and add button
        header = ctk.CTkFrame(main_frame)
        header.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(header, text="Soundboard", font=("Arial", 24, "bold")).pack(side="left")

        # Master volume control
        master_volume_frame = ctk.CTkFrame(header, fg_color="transparent")
        master_volume_frame.pack(side="left", padx=20)
        ctk.CTkLabel(master_volume_frame, text="Master Volume:").pack(side="left", padx=5)
        self.master_volume = ctk.CTkSlider(
            master_volume_frame,
            from_=0,
            to=100,
            command=self.set_master_volume,
            width=200
        )
        self.master_volume.set(100)
        self.master_volume.pack(side="left")

        ctk.CTkButton(header, text="Save", command=self.save_state).pack(side="right", padx=(5, 0))
        ctk.CTkButton(header, text="Load", command=self.load_state).pack(side="right", padx=(5, 0))
        ctk.CTkButton(header, text="+ Add Sound", command=self.add_sound).pack(side="right", padx=(5, 0))

        # Scrollable sound list
        self.sound_frame = ctk.CTkScrollableFrame(main_frame)
        self.sound_frame.pack(fill="both", expand=True)

    def save_state(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".sb",
            filetypes=[("Soundboard Files", "*.sb")]
        )
        if not file_path:
            return

        try:
            state = {
                'sounds': [(fp, vars['volume'].get(), self.loop_vars[fp].get(), self.fade_vars[fp].get()) for fp, vars in self.ui_elements.items()],
                'master_volume': self.master_volume.get()
            }
            with open(file_path, 'wb') as f:
                pickle.dump(state, f)
            messagebox.showinfo("Success", "State saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save state: {str(e)}")

    def load_state(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Soundboard Files", "*.sb")]
        )
        if not file_path:
            return

        try:
            with open(file_path, 'rb') as f:
                state = pickle.load(f)

            # Clear existing sounds
            for file_path in list(self.sounds.keys()):
                self.remove_sound(file_path, None, self.ui_elements[file_path]['button'].master)

            # Restore state
            self.master_volume.set(state['master_volume'])

            for file_path, volume, loop, fade in state['sounds']:
                hotkey = simpledialog.askstring("Hotkey", f"Assign hotkey for {os.path.basename(file_path)}:")
                if not hotkey:
                    continue

                try:
                    remove_hotkey(hotkey)  # Remove existing hotkey if any
                except Exception:
                    pass

                add_hotkey(hotkey, lambda fp=file_path: self.toggle_play(fp))

                sound = pygame.mixer.Sound(file_path)
                self.sounds[file_path] = sound

                card = self.create_sound_card(file_path, hotkey)
                self.volume_vars[file_path].set(volume)
                self.loop_vars[file_path].set(loop)
                self.fade_vars[file_path].set(fade)

            messagebox.showinfo("Success", "State loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load state: {str(e)}")

    # Other methods from the original implementation go here

    def create_sound_card(self, file_path, hotkey):
        try:
            # Create card frame
            card = ctk.CTkFrame(self.sound_frame)
            card.pack(fill="x", pady=5, padx=10)

            # Sound name and hotkey
            name_frame = ctk.CTkFrame(card, fg_color="transparent")
            name_frame.pack(fill="x", padx=10, pady=5)

            indicator = ctk.CTkLabel(name_frame, text="●", text_color="gray70", width=20)
            indicator.pack(side="left")

            ctk.CTkLabel(
                name_frame,
                text=f"{os.path.basename(file_path)} ({hotkey})",
                font=("Arial", 12)
            ).pack(side="left")

            # Controls frame
            controls = ctk.CTkFrame(card, fg_color="transparent")
            controls.pack(fill="x", padx=10, pady=5)

            # Left controls (Play + Volume)
            left_controls = ctk.CTkFrame(controls, fg_color="transparent")
            left_controls.pack(side="left", fill="x", expand=True)

            play_button = ctk.CTkButton(
                left_controls,
                text="Play",
                width=100,
                command=lambda: self.toggle_play(file_path)
            )
            play_button.pack(side="left", padx=5)

            # Volume control
            ctk.CTkLabel(left_controls, text="Volume:").pack(side="left", padx=(20, 5))
            volume = ctk.CTkSlider(
                left_controls,
                from_=0,
                to=100,
                command=lambda v, fp=file_path: self.set_volume(fp, v),
                width=200
            )
            volume.set(100)
            volume.pack(side="left", padx=5)
            self.volume_vars[file_path] = volume

            # Right controls (Loop, Fade, Stop All)
            right_controls = ctk.CTkFrame(controls, fg_color="transparent")
            right_controls.pack(side="right")

            # Loop checkbox
            loop_var = ctk.BooleanVar(value=False)
            loop_check = ctk.CTkCheckBox(
                right_controls,
                text="Loop",
                variable=loop_var,
                command=lambda: self.handle_loop_change(file_path)
            )
            loop_check.pack(side="left", padx=5)
            self.loop_vars[file_path] = loop_var

            # Fade checkbox
            fade_var = ctk.BooleanVar(value=False)
            fade_check = ctk.CTkCheckBox(
                right_controls,
                text="Fade",
                variable=fade_var
            )
            fade_check.pack(side="left", padx=5)
            self.fade_vars[file_path] = fade_var

            # Remove button
            ctk.CTkButton(
                right_controls,
                text="Remove",
                width=100,
                command=lambda: self.remove_sound(file_path, hotkey, card),
                fg_color="red",
                hover_color="darkred"
            ).pack(side="left", padx=5)

            # Store UI references
            self.ui_elements[file_path] = {
                'button': play_button,
                'indicator': indicator,
                'volume': volume
            }

            return card

        except Exception as e:
            print(f"Error creating sound card: {e}")
            return None

    def convert_volume(self, slider_value):
        """Convert linear slider value (0-100) to logarithmic volume (0-1)"""
        if slider_value <= 0:
            return 0

        # Convert percentage to logarithmic scale
        min_db = -40  # Minimum decibel level
        normalized_value = slider_value / 100

        if normalized_value < 0.01:
            return 0

        db = min_db * (1 - normalized_value)
        return pow(10, db / 20)

    def set_master_volume(self, value):
        """Set master volume for all playing sounds"""
        master_volume = self.convert_volume(value)
        for file_path in self.channels:
            if self.channels[file_path].get_busy():
                individual_volume = self.volume_vars[file_path].get()
                final_volume = self.convert_volume(individual_volume) * master_volume
                self.channels[file_path].set_volume(final_volume)

    def handle_loop_change(self, file_path):
        """Handle loop checkbox changes"""
        if file_path in self.channels and self.channels[file_path].get_busy():
            self.stop_sound(file_path)
            self.play_sound(file_path)

    def add_sound(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Audio files", "*.mp3 *.wav *.ogg *.flac")]
            )
            if not file_path:
                return

            hotkey = simpledialog.askstring(
                "Hotkey",
                "Enter hotkey (e.g., 'f1', 'ctrl+1', 'a'):"
            )
            if not hotkey:
                return

            # Check if hotkey is already in use
            try:
                # First try to remove any existing hotkey
                remove_hotkey(hotkey)
            except Exception:
                pass  # Ignore if hotkey doesn't exist

            try:
                # Register new hotkey
                add_hotkey(hotkey, lambda: self.toggle_play(file_path))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to register hotkey: {str(e)}")
                return

            # Load sound
            try:
                sound = pygame.mixer.Sound(file_path)
                self.sounds[file_path] = sound
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load sound: {str(e)}")
                # Clean up hotkey if sound loading fails
                try:
                    remove_hotkey(hotkey)
                except Exception:
                    pass
                return

            # Create UI
            if self.create_sound_card(file_path, hotkey):
                return
            else:
                # Clean up if UI creation fails
                self.sounds.pop(file_path, None)
                try:
                    remove_hotkey(hotkey)
                except Exception:
                    pass

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add sound: {str(e)}")

    def toggle_play(self, file_path):
        try:
            # If currently playing, stop it
            if file_path in self.channels and self.channels[file_path].get_busy():
                self.stop_sound(file_path)
                return

            self.play_sound(file_path)

        except Exception as e:
            print(f"Error toggling play: {e}")

    def play_sound(self, file_path):
        try:
            sound = self.sounds[file_path]
            loops = -1 if self.loop_vars[file_path].get() else 0

            channel = pygame.mixer.find_channel()
            if channel:
                channel.play(sound, loops)
                self.channels[file_path] = channel

                # Set initial volume
                volume = self.volume_vars[file_path].get()
                master_volume = self.master_volume.get()
                final_volume = self.convert_volume(volume) * self.convert_volume(master_volume)
                channel.set_volume(final_volume)

                # Update UI
                self.ui_elements[file_path]['button'].configure(text="Stop")
                self.ui_elements[file_path]['indicator'].configure(text_color="green")

                # Set up callback for when sound finishes (if not looping)
                if loops != -1:
                    self.root.after(100, self.check_sound_finished, file_path)

        except Exception as e:
            print(f"Error playing sound: {e}")

    def check_sound_finished(self, file_path):
        """Check if sound has finished playing and update UI accordingly"""
        if file_path in self.channels:
            channel = self.channels[file_path]
            if not channel.get_busy():
                self.update_ui_stopped(file_path)
                self.channels.pop(file_path, None)
            else:
                # Check again in 100ms
                self.root.after(100, self.check_sound_finished, file_path)

    def stop_sound(self, file_path):
        try:
            if file_path in self.channels:
                channel = self.channels[file_path]

                # Apply fade if enabled
                if self.fade_vars[file_path].get():
                    channel.fadeout(500)  # 500ms fade
                    self.root.after(500, lambda: self.update_ui_stopped(file_path))
                else:
                    channel.stop()
                    self.update_ui_stopped(file_path)

                self.channels.pop(file_path, None)

        except Exception as e:
            print(f"Error stopping sound: {e}")
            self.update_ui_stopped(file_path)

    def update_ui_stopped(self, file_path):
        """Update UI elements to stopped state"""
        if file_path in self.ui_elements:
            self.ui_elements[file_path]['button'].configure(text="Play")
            self.ui_elements[file_path]['indicator'].configure(text_color="gray70")

    def set_volume(self, file_path, volume):
        try:
            if file_path in self.channels:
                master_volume = self.master_volume.get()
                final_volume = self.convert_volume(volume) * self.convert_volume(master_volume)
                self.channels[file_path].set_volume(final_volume)
        except Exception as e:
            print(f"Error setting volume: {e}")

    def remove_sound(self, file_path, hotkey, card):
        try:
            # Stop if playing
            if file_path in self.channels:
                self.stop_sound(file_path)

            # Remove hotkey first
            try:
                remove_hotkey(hotkey)
            except Exception as e:
                print(f"Error removing hotkey: {e}")

            # Clean up resources
            self.sounds.pop(file_path, None)
            self.loop_vars.pop(file_path, None)
            self.fade_vars.pop(file_path, None)
            self.ui_elements.pop(file_path, None)
            self.volume_vars.pop(file_path, None)
            card.destroy()

        except Exception as e:
            print(f"Error removing sound: {e}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SoundboardApp()
    app.run()
