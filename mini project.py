import tkinter as tk
from tkinter import scrolledtext
import heapq
import re

# 🎨 Theme Colors (CSS-like)
BG_COLOR = "#181824"
CARD_COLOR = "#232336"
INPUT_COLOR = "#2c2c44"
ACCENT = "#00ADB5"
USER_COLOR = "#4CAF50"
TEXT_COLOR = "#ffffff"
MUTED = "#aaaaaa"

# 🧠 Stopwords
stop_words = set([
    "the","is","in","and","to","of","a","that","it","on","for","with","as","this",
    "are","was","but","be","by","or","an","at","from"
])

# 🔤 Text Processing
def split_sentences(text):
    return re.split(r'(?<=[.!?]) +', text)

def split_words(text):
    return re.findall(r'\w+', text.lower())

# 🧠 Summarizer
def summarize_text(text, num_sentences=3):
    sentences = split_sentences(text)
    words = split_words(text)

    freq_table = {}
    for word in words:
        if word not in stop_words:
            freq_table[word] = freq_table.get(word, 0) + 1

    sentence_scores = {}
    for sent in sentences:
        for word in split_words(sent):
            if word in freq_table:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + freq_table[word]

    return heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)

# 🧠 Placeholder Functions
def clear_placeholder(event):
    if input_box.get("1.0", tk.END).strip() == "Enter your text here...":
        input_box.delete("1.0", tk.END)
        input_box.config(fg="white")

def add_placeholder(event):
    if input_box.get("1.0", tk.END).strip() == "":
        input_box.insert("1.0", "Enter your text here...")
        input_box.config(fg="gray")

# 💬 Send Message
def send_message():
    text = input_box.get("1.0", tk.END).strip()

    if text == "" or text == "Enter your text here...":
        return

    # User message
    chat_area.insert(tk.END, "👩 You:\n", "user_label")
    chat_area.insert(tk.END, text + "\n\n", "user_msg")

    # Bot response
    summary = summarize_text(text)

    chat_area.insert(tk.END, "🤖 Summary:\n", "bot_label")
    for i, line in enumerate(summary, 1):
        chat_area.insert(tk.END, f"{i}. {line}\n", "bot_msg")

    chat_area.insert(tk.END, "\n" + "-"*40 + "\n\n")

    input_box.delete("1.0", tk.END)
    add_placeholder(None)
    chat_area.yview(tk.END)

# 🖼️ Window
root = tk.Tk()
root.title("🧠 Smart Note Summarizer")
root.geometry("700x700")
root.configure(bg=BG_COLOR)

# 📦 Main Frame
main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(fill="both", expand=True, padx=15, pady=15)

# 🏷️ Header
header = tk.Label(
    main_frame,
    text="🧠 Smart Note Summarizer",
    bg=BG_COLOR,
    fg=ACCENT,
    font=("Segoe UI", 18, "bold")
)
header.pack(pady=(0, 10))

# 💬 Chat Frame
chat_frame = tk.Frame(main_frame, bg=CARD_COLOR)
chat_frame.pack(fill="both", expand=True)

chat_area = scrolledtext.ScrolledText(
    chat_frame,
    wrap=tk.WORD,
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    font=("Segoe UI", 11),
    bd=0,
    padx=15,
    pady=15,
    insertbackground="white"
)
chat_area.pack(fill="both", expand=True)

# 🎨 Chat Styles
chat_area.tag_config("user_label", foreground=USER_COLOR, font=("Segoe UI", 10, "bold"))
chat_area.tag_config("user_msg", foreground="#e0e0e0")
chat_area.tag_config("bot_label", foreground=ACCENT, font=("Segoe UI", 10, "bold"))
chat_area.tag_config("bot_msg", foreground="#cccccc")

# ✍️ Input Frame
input_frame = tk.Frame(main_frame, bg=BG_COLOR)
input_frame.pack(fill="x", pady=10)

# 📝 Instruction
input_label = tk.Label(
    input_frame,
    text="Type or paste your text here 👇",
    bg=BG_COLOR,
    fg=MUTED,
    font=("Segoe UI", 10)
)
input_label.pack(anchor="w", pady=(0, 5))

# ✍️ Input Box
input_box = tk.Text(
    input_frame,
    height=4,
    bg=INPUT_COLOR,
    fg="gray",
    font=("Segoe UI", 11),
    bd=0,
    padx=10,
    pady=10,
    insertbackground="white"
)
input_box.pack(fill="x", side="left", expand=True, padx=(0, 10))

# Placeholder text
input_box.insert("1.0", "Enter your text here...")
input_box.bind("<FocusIn>", clear_placeholder)
input_box.bind("<FocusOut>", add_placeholder)

# 🔘 Button
send_btn = tk.Button(
    input_frame,
    text="➤",
    command=send_message,
    bg=ACCENT,
    fg="white",
    font=("Segoe UI", 14, "bold"),
    bd=0,
    width=4,
    height=2,
    cursor="hand2",
    activebackground="#028d92"
)
send_btn.pack(side="right")

# Hover effect
def on_enter(e):
    send_btn.config(bg="#028d92")

def on_leave(e):
    send_btn.config(bg=ACCENT)

send_btn.bind("<Enter>", on_enter)
send_btn.bind("<Leave>", on_leave)

root.mainloop()