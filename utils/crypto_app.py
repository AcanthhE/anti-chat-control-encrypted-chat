#!/usr/bin/env python3
"""
Local Encrypted Message Tool
=============================
A simple, fully offline desktop app for encrypting and decrypting text
using AES-256-GCM with a password-derived key (PBKDF2HMAC, 600k iterations).

No network access is required or performed by this application.
"""

import os
import base64
import tkinter as tk
from tkinter import filedialog, messagebox

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ---------------------------------------------------------------------------
# Crypto logic
# ---------------------------------------------------------------------------

SALT_SIZE = 16
NONCE_SIZE = 12


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt(message: str, password: str) -> str:
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, message.encode("utf-8"), None)
    payload = salt + nonce + ciphertext
    return base64.b64encode(payload).decode("utf-8")


def decrypt(message_b64: str, password: str) -> str:
    payload = base64.b64decode(message_b64.strip().encode("utf-8"))
    salt = payload[:SALT_SIZE]
    nonce = payload[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
    ciphertext = payload[SALT_SIZE + NONCE_SIZE:]
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode("utf-8")


# ---------------------------------------------------------------------------
# Dark theme palette
# ---------------------------------------------------------------------------

BG = "#1e1e24"
BG_PANEL = "#262631"
BORDER = "#3a3a46"
FG = "#e6e6e9"
FG_MUTED = "#9a9aa5"
ACCENT = "#7c5cff"
ACCENT_HOVER = "#9179ff"

FONT_UI = ("Segoe UI", 10)
FONT_MONO = ("Consolas", 11)


class CryptoApp(tk.Tk):
    """Main application window.

    Layout uses the grid geometry manager so that:
      - the window can be resized to any shape (including very wide and
        short) without hiding buttons or the status bar
      - only the text area grows/shrinks with the window
      - a minimum size guarantees every control stays visible
    """

    def __init__(self):
        super().__init__()
        self.title("Local Encrypted Message Tool")
        self.configure(bg=BG)

        # Wide-and-short default window, as requested.
        self.geometry("980x300")

        # Make the single column stretch horizontally.
        self.columnconfigure(0, weight=1)

        self._build_header()      # row 0 - fixed height
        self._build_key_row()     # row 1 - fixed height
        self._build_message_area()  # row 2 - the ONLY row that grows
        self._build_actions()     # row 3 - fixed height
        self._build_status_bar()  # row 4 - fixed height

        # Only the message row is allowed to expand.
        self.grid_rowconfigure(2, weight=1)

        # Compute a safe minimum size so fixed rows are never clipped.
        self.update_idletasks()
        min_width = 640
        min_height = self.winfo_reqheight()
        self.minsize(min_width, min_height)

    # -- UI blocks ------------------------------------------------------

    def _build_header(self):
        header = tk.Frame(self, bg=BG)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 6))

        tk.Label(
            header, text="Local Encrypted Message Tool",
            font=("Segoe UI", 15, "bold"), bg=BG, fg=FG,
        ).pack(anchor="w")
        tk.Label(
            header,
            text="100% offline — no data ever leaves this computer.",
            font=FONT_UI, bg=BG, fg=FG_MUTED,
        ).pack(anchor="w")

    def _build_key_row(self):
        row = tk.Frame(self, bg=BG)
        row.grid(row=1, column=0, sticky="ew", padx=20, pady=(10, 0))
        row.columnconfigure(0, weight=1)

        tk.Label(row, text="Secret key", font=FONT_UI, bg=BG, fg=FG).grid(
            row=0, column=0, columnspan=2, sticky="w"
        )

        self.key_var = tk.StringVar()
        self.key_entry = tk.Entry(
            row, textvariable=self.key_var, show="*",
            font=FONT_UI, bg=BG_PANEL, fg=FG, insertbackground=FG,
            relief="flat", highlightthickness=1,
            highlightbackground=BORDER, highlightcolor=ACCENT,
        )
        self.key_entry.grid(row=1, column=0, sticky="ew", ipady=6, pady=(4, 0), padx=(0, 8))

        self.show_key = tk.BooleanVar(value=False)
        tk.Checkbutton(
            row, text="Show", variable=self.show_key,
            command=self._toggle_key_visibility,
            font=FONT_UI, bg=BG, fg=FG_MUTED, selectcolor=BG_PANEL,
            activebackground=BG, activeforeground=FG, relief="flat",
        ).grid(row=1, column=1, sticky="e", pady=(4, 0))

    def _toggle_key_visibility(self):
        self.key_entry.config(show="" if self.show_key.get() else "*")

    def _build_message_area(self):
        wrap = tk.Frame(self, bg=BG)
        wrap.grid(row=2, column=0, sticky="nsew", padx=20, pady=(14, 0))
        wrap.columnconfigure(0, weight=1)
        wrap.rowconfigure(1, weight=1)

        tk.Label(wrap, text="Message", font=FONT_UI, bg=BG, fg=FG).grid(
            row=0, column=0, sticky="w"
        )

        text_frame = tk.Frame(wrap, bg=BORDER, bd=0)
        text_frame.grid(row=1, column=0, sticky="nsew", pady=(4, 0))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        self.text = tk.Text(
            text_frame, wrap="word", font=FONT_MONO,
            bg=BG_PANEL, fg=FG, insertbackground=FG,
            relief="flat", padx=10, pady=10, undo=True,
            height=3,  # small minimum; the row grows via weight anyway
        )
        self.text.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)

        scrollbar = tk.Scrollbar(text_frame, command=self.text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=1)
        self.text.configure(yscrollcommand=scrollbar.set)

    def _build_actions(self):
        wrap = tk.Frame(self, bg=BG)
        wrap.grid(row=3, column=0, sticky="ew", padx=20, pady=14)

        self._make_button(wrap, "Encrypt", ACCENT, self.on_encrypt).pack(side="left", padx=(0, 8))
        self._make_button(wrap, "Decrypt", BORDER, self.on_decrypt).pack(side="left", padx=(0, 8))
        self._make_button(wrap, "Copy", BORDER, self.on_copy).pack(side="left", padx=(0, 8))
        self._make_button(wrap, "Open .txt", BORDER, self.on_load).pack(side="right", padx=(8, 0))
        self._make_button(wrap, "Save .txt", BORDER, self.on_save).pack(side="right")

    def _make_button(self, parent, text, color, command):
        return tk.Button(
            parent, text=text, command=command, font=FONT_UI,
            bg=color, fg=FG, activebackground=ACCENT_HOVER, activeforeground=FG,
            relief="flat", padx=14, pady=8, cursor="hand2", bd=0,
        )

    def _build_status_bar(self):
        self.status_var = tk.StringVar(value="Ready.")
        tk.Label(
            self, textvariable=self.status_var, anchor="w",
            font=("Segoe UI", 9), bg=BG_PANEL, fg=FG_MUTED, padx=12, pady=6,
        ).grid(row=4, column=0, sticky="ew")

    # -- Actions ----------------------------------------------------------

    def _set_status(self, message: str):
        self.status_var.set(message)

    def _get_message(self) -> str:
        return self.text.get("1.0", "end-1c")

    def _set_message(self, content: str):
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content)

    def on_encrypt(self):
        password = self.key_var.get().strip()
        message = self._get_message()
        if not password:
            messagebox.showwarning("Missing key", "Enter a secret key before encrypting.")
            return
        if not message.strip():
            messagebox.showwarning("Empty message", "Write a message to encrypt.")
            return
        try:
            result = encrypt(message, password)
            self._set_message(result)
            self._set_status("Message encrypted successfully.")
        except Exception as exc:
            messagebox.showerror("Error", f"Encryption failed: {exc}")

    def on_decrypt(self):
        password = self.key_var.get().strip()
        message = self._get_message()
        if not password:
            messagebox.showwarning("Missing key", "Enter the secret key before decrypting.")
            return
        if not message.strip():
            messagebox.showwarning("Empty message", "Paste the encrypted text to decrypt.")
            return
        try:
            result = decrypt(message, password)
            self._set_message(result)
            self._set_status("Message decrypted successfully.")
        except Exception:
            messagebox.showerror("Error", "Wrong key or corrupted data.")
            self._set_status("Decryption failed.")

    def on_copy(self):
        self.clipboard_clear()
        self.clipboard_append(self._get_message())
        self._set_status("Content copied to clipboard.")

    def on_load(self):
        path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # Supports both a plain text file and the original
            # MODE:/CLE:/MESSAGE: file format.
            if "MESSAGE:" in content:
                _, message_part = content.split("MESSAGE:", 1)
                self._set_message(message_part.strip())
            else:
                self._set_message(content)
            self._set_status(f"Loaded file: {os.path.basename(path)}")
        except Exception as exc:
            messagebox.showerror("Error", f"Could not open the file: {exc}")

    def on_save(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text files", "*.txt")]
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self._get_message())
            self._set_status(f"Saved: {os.path.basename(path)}")
        except Exception as exc:
            messagebox.showerror("Error", f"Could not save the file: {exc}")


if __name__ == "__main__":
    app = CryptoApp()
    app.mainloop()
