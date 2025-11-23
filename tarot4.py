import tkinter as tk
from tkinter import messagebox, Frame, Canvas, Scrollbar
from  PIL import Image, ImageTk, ImageDraw
import random
import os

# ---------------------------------------
# YOUR IMAGE FOLDER (Tarot JPG location)
# ---------------------------------------
IMAGE_FOLDER = r"C:\Users\Dell\OneDrive\my folder\images"

# ---------------------------------------
# Tarot card image map (JPG version)
# ---------------------------------------
IMAGE_MAP = {
    "The Fool": "RWS_Tarot_00_Fool.jpg",
    "The Magician": "RWS_Tarot_01_Magician.jpg",
    "The High Priestess": "RWS_Tarot_02_High_Priestess.jpg",
    "The Empress": "RWS_Tarot_03_Empress.jpg",
    "The Emperor": "RWS_Tarot_04_Emperor.jpg",
    "The Hierophant": "RWS_Tarot_05_Hierophant.jpg",
    "The Lovers": "RWS_Tarot_06_Lovers.jpg",
    "The Chariot": "RWS_Tarot_07_Chariot.jpg",
    "Strength": "RWS_Tarot_08_Strength.jpg",
    "The Hermit": "RWS_Tarot_09_Hermit.jpg",
    "Wheel of Fortune": "RWS_Tarot_10_Wheel_of_Fortune.jpg",
    "Justice": "RWS_Tarot_11_Justice.jpg",
    "The Hanged Man": "RWS_Tarot_12_Hanged_Man.jpg",
    "Death": "RWS_Tarot_13_Death.jpg",
    "Temperance": "RWS_Tarot_14_Temperance.jpg",
    "The Devil": "RWS_Tarot_15_Devil.jpg",
    "The Tower": "RWS_Tarot_16_Tower.jpg",
    "The Star": "RWS_Tarot_17_Star.jpg",
    "The Moon": "RWS_Tarot_18_Moon.jpg",
    "The Sun": "RWS_Tarot_19_Sun.jpg",
    "Judgement": "RWS_Tarot_20_Judgement.jpg",
    "The World": "RWS_Tarot_21_World.jpg"
}

# ---------------------------------------
# Tarot meanings (base meanings)
# ---------------------------------------
TAROT_MEANINGS = {
    "The Fool": "A fresh start, innocence, leap of faith.",
    "The Magician": "Manifestation, action, power.",
    "The High Priestess": "Intuition, hidden wisdom.",
    "The Empress": "Nurturing, abundance, creativity.",
    "The Emperor": "Authority, structure, stability.",
    "The Hierophant": "Learning, tradition, guidance.",
    "The Lovers": "Relationships, alignment, choices.",
    "The Chariot": "Determination, victory, control.",
    "Strength": "Courage, compassion, inner power.",
    "The Hermit": "Introspection, soul-searching.",
    "Wheel of Fortune": "Change, destiny, timing.",
    "Justice": "Truth, consequences, fairness.",
    "The Hanged Man": "New perspective, letting go.",
    "Death": "Transformation and new beginnings.",
    "Temperance": "Balance, harmony, moderation.",
    "The Devil": "Temptation, bondage, shadow self.",
    "The Tower": "Sudden change, breakthrough.",
    "The Star": "Hope, clarity, inspiration.",
    "The Moon": "Illusion, hidden truth, intuition.",
    "The Sun": "Joy, success, happiness.",
    "Judgement": "Spiritual awakening, evaluation.",
    "The World": "Completion, fulfillment, harmony."
}

# ---------------------------------------
# Create tarot back image with pattern
# ---------------------------------------
def make_back_image(size=(90, 150), base_color="#4a2c6b", pattern_color="#6b4a8d"):
    img = Image.new("RGBA", size, base_color)
    draw = ImageDraw.Draw(img)

    # Border
    border_width = 4
    draw.rectangle([border_width, border_width, size[0]-border_width, size[1]-border_width],
                   outline=pattern_color, width=2)

    # Vertical & horizontal lines
    for x in range(10, size[0]-10, 6):
        draw.line([(x, 10), (x, size[1]-10)], fill=pattern_color, width=1)
    for y in range(10, size[1]-10, 6):
        draw.line([(10, y), (size[0]-10, y)], fill=pattern_color, width=1)

    # Center diamond
    cx, cy = size[0]//2, size[1]//2
    ds = 20
    draw.polygon([(cx, cy - ds), (cx + ds, cy), (cx, cy + ds), (cx - ds, cy)],
                 outline=pattern_color, width=2)
    # Smaller surrounding diamonds
    for dx, dy in [(-15, -30), (15, -30), (-15, 30), (15, 30)]:
        s = 10
        draw.polygon([(cx + dx, cy + dy - s), (cx + dx + s, cy + dy),
                      (cx + dx, cy + dy + s), (cx + dx - s, cy + dy)],
                     outline=pattern_color, width=1)
    return img

# ---------------------------------------
# Check available images
# ---------------------------------------
def get_available_cards(folder, image_map):
    available, missing = {}, []
    for name, filename in image_map.items():
        path = os.path.join(folder, filename)
        if os.path.exists(path):
            available[name] = filename
        else:
            missing.append(f"{name} -> {filename}")
    if missing:
        print("⚠️ Missing images:")
        for m in missing: print(f" - {m}")
        print(f"✅ Found {len(available)} out of {len(image_map)} cards")
    return available

# ---------------------------------------
# Dynamic, human-like prediction generator
# ---------------------------------------
def generate_dynamic_prediction(question, selected_cards):
    cards = [card for _, card in selected_cards]
    
    CARD_TEMPLATES = {
        "The Fool": [
            "A leap of faith is suggested. New opportunities await if you embrace the unknown.",
            "Consider starting fresh; boldness may serve you well.",
            "Excitement and curiosity guide you, but watch for impulsive decisions."
        ],
        "The Magician": [
            "You have the power to shape events. Focus your actions carefully.",
            "Manifest your desires through confidence and intention.",
            "Your skills and talents are highlighted; use them wisely."
        ],
        "The High Priestess": [
            "Trust your intuition; answers are within you.",
            "Hidden factors influence your situation; observe and reflect.",
            "Patience and inner wisdom will guide your next move."
        ],
        "The Lovers": [
            "Choices in relationships are important; align your heart with your values.",
            "A meaningful connection may require careful consideration.",
            "Harmony is possible, but clarity in decision-making is key."
        ],
        "Death": [
            "Transformation is coming; endings lead to fresh starts.",
            "Let go of old patterns to embrace renewal.",
            "Change is inevitable; view it as an opportunity for growth."
        ],
        "The Moon": [
            "Situations may be unclear; trust your instincts.",
            "Hidden truths may reveal themselves; beware illusions.",
            "Emotions are heightened; introspection will illuminate the path."
        ],
        "The Sun": [
            "Success, joy, and clarity are ahead; positive outcomes are likely.",
            "Happiness and confidence guide you now.",
            "Radiance and optimism surround your situation."
        ],
        "The Tower": [
            "Unexpected events may shake things up, but bring revelation.",
            "Change is sudden but clears the path for growth.",
            "Disruption may feel uncomfortable but leads to clarity."
        ],
        # Add more cards as needed
    }

    reading_lines = [f"Regarding your question: '{question}', here's what the cards reveal:\n"]
    for card in cards:
        templates = CARD_TEMPLATES.get(card, [TAROT_MEANINGS.get(card, "Significant card appears.")])
        reading_lines.append(f"• {card}: {random.choice(templates)}")

    # Optional combined insights
    combined_msg = ""
    if "The Fool" in cards and "The Magician" in cards:
        combined_msg = "A bold start meets your inner skills. New journeys are ready to manifest."
    elif "Death" in cards and "The Moon" in cards:
        combined_msg = "Transformation is underway; trust intuition as hidden changes occur."
    elif "The Lovers" in cards and "The Sun" in cards:
        combined_msg = "Love or partnership prospects are bright. Positive developments are likely."

    if combined_msg: reading_lines.append("\n💫 Combined insight: " + combined_msg)

    # Final reflective advice
    final_lines = [
        "Take time to reflect on these insights before deciding.",
        "Trust yourself and your instincts as you move forward.",
        "The universe offers guidance — listen carefully.",
        "Awareness and reflection are key in decision-making."
    ]
    reading_lines.append("\n" + random.choice(final_lines))

    return "\n".join(reading_lines)

# ---------------------------------------
# Tarot App Class
# ---------------------------------------
class TarotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tarot Reading App")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2d1b4e")

        self.available_cards = get_available_cards(IMAGE_FOLDER, IMAGE_MAP)
        if len(self.available_cards) < 3:
            messagebox.showerror("Not Enough Images",
                                 f"Only {len(self.available_cards)} card images found. Need at least 3 cards.")
            root.quit()
            return

        back_img = make_back_image()
        self.BACK_IMAGE = ImageTk.PhotoImage(back_img)
        self.deck = list(self.available_cards.keys())
        random.shuffle(self.deck)
        self.selected_cards = []
        self.card_labels = []

        # Question input
        tk.Label(root, text="💬 Ask Your Question:", font=("Georgia", 16, "bold"),
                 bg="#2d1b4e", fg="white").pack(pady=10)
        self.question_entry = tk.Entry(root, font=("Georgia", 14), width=50)
        self.question_entry.pack(pady=5)

        # Title
        tk.Label(root, text="🔮 Choose Any 3 Cards From The Deck 🔮", font=("Georgia", 24, "bold"),
                 bg="#2b1d33", fg="white").pack(pady=15)
        self.counter_label = tk.Label(root, text="Cards Selected: 0/3", font=("Georgia", 14, "bold"),
                                      bg="#2b1d33", fg="#ffd700")
        self.counter_label.pack(pady=5)

        # Buttons
        btn_frame = Frame(root, bg="#2b1d33")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="🔄 Shuffle Deck", font=("Georgia", 12, "bold"),
                  bg="#8b4789", fg="white", command=self.shuffle_deck,
                  cursor="hand2", padx=20, pady=8).pack(side="left", padx=10)
        tk.Button(btn_frame, text="🔁 New Reading", font=("Georgia", 12, "bold"),
                  bg="#6a4c93", fg="white", command=self.reset_reading,
                  cursor="hand2", padx=20, pady=8).pack(side="left", padx=10)

        # Canvas for cards
        container = Frame(root, bg="#2d1b4e")
        container.pack(fill="both", expand=True, padx=20, pady=10)
        self.canvas = Canvas(container, bg="#2d1b4e", highlightthickness=0, width=1000, height=500)
        scrollbar = Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self.draw_cards_circular()

    def draw_cards_circular(self):
        import math
        self.canvas.delete("all")
        self.card_labels = []
        self.card_images = []

        num_cards = len(self.deck)
        start_x, start_y = 50, 250
        card_spacing = 45
        max_y_offset = 100

        for i, card_name in enumerate(self.deck):
            x = start_x + i*card_spacing
            normalized_pos = (i - (num_cards-1)/2) / ((num_cards-1)/2)
            y_offset = max_y_offset*(1 - normalized_pos**2)
            y = start_y - y_offset
            rotation_angle = normalized_pos*25
            rotated_img = self.rotate_image(rotation_angle)
            self.card_images.append(rotated_img)
            card_id = self.canvas.create_image(x, y, image=rotated_img, anchor="center",
                                              tags=("card", f"card_{i}"))
            self.canvas.tag_bind(f"card_{i}", "<Button-1>", lambda e, idx=i: self.reveal_card(idx))
            self.card_labels.append((card_id, rotation_angle))

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def rotate_image(self, angle):
        img = make_back_image()
        rotated = img.rotate(-angle, expand=True)
        return ImageTk.PhotoImage(rotated)

    def shuffle_deck(self):
        if len(self.selected_cards) > 0:
            if not messagebox.askyesno("Shuffle Deck", "This will reset your current selection. Continue?"):
                return
        random.shuffle(self.deck)
        self.draw_cards_circular()
        self.selected_cards = []
        self.counter_label.config(text="Cards Selected: 0/3")
        messagebox.showinfo("Shuffled", "✨ The deck has been shuffled!")

    def reset_reading(self):
        if len(self.selected_cards) > 0:
            if not messagebox.askyesno("New Reading", "Start a new reading? This will clear your current selection."):
                return
        self.question_entry.delete(0, tk.END)
        random.shuffle(self.deck)
        self.draw_cards_circular()
        self.selected_cards = []
        self.counter_label.config(text="Cards Selected: 0/3")
        messagebox.showinfo("Ready", "🔮 Ready for your new question!")

    def reveal_card(self, index):
        if len(self.selected_cards) >= 3:
            messagebox.showinfo("Complete", "You've already selected 3 cards!")
            return
        if index in [i[0] for i in self.selected_cards]: return

        card_name = self.deck[index]
        img_path = os.path.join(IMAGE_FOLDER, self.available_cards[card_name])
        try:
            img = Image.open(img_path).resize((110, 180))
            photo = ImageTk.PhotoImage(img)
            self.card_images.append(photo)

            card_id, angle = self.card_labels[index]
            x = self.canvas.coords(card_id)[0]
            self.canvas.itemconfig(card_id, image=photo)
            self.canvas.coords(card_id, x, 350)
            self.canvas.tag_raise(f"card_{index}")
            self.selected_cards.append((index, card_name))
            self.counter_label.config(text=f"Cards Selected: {len(self.selected_cards)}/3")

            if len(self.selected_cards) == 3:
                self.show_reading()
        except Exception as e:
            messagebox.showerror("Error Loading Image", f"Failed to load: {card_name}\n{e}")

    def show_reading(self):
        question = self.question_entry.get().strip() or "(No question provided)"
        reading_text = generate_dynamic_prediction(question, self.selected_cards)

        reading = tk.Toplevel(self.root)
        reading.title("Your Tarot Reading")
        reading.geometry("700x750")
        reading.configure(bg="#1a272e")

        tk.Label(reading, text="✨ Your Tarot Reading ✨", font=("Georgia", 22, "bold"),
                 fg="#ffd700", bg="#241a2e").pack(pady=15)
        tk.Label(reading, text=reading_text, font=("Georgia", 13),
                 fg="white", bg="#241a2e", wraplength=650, justify="left").pack(pady=20)

        tk.Button(reading, text="Close", font=("Georgia", 12, "bold"),
                  bg="#5d3b85", fg="white", command=reading.destroy, cursor="hand2").pack(pady=10)
        tk.Button(reading, text="🔁 Start New Reading", font=("Georgia", 12, "bold"),
                  bg="#6a4c93", fg="white",
                  command=lambda: [reading.destroy(), self.reset_reading()], cursor="hand2").pack(pady=5)

# ---------------------------------------
# Run App
# ---------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    TarotApp(root)
    root.mainloop()
