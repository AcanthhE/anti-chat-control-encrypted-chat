# Local Encrypted Message Tool

A small, fully offline desktop app to encrypt and decrypt text messages using
**AES-256-GCM** with a password-derived key. No server, no network calls,
no telemetry — everything happens on your machine.

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## Features

- **AES-256-GCM encryption** with message authentication (tamper detection)
- **PBKDF2HMAC key derivation** (600,000 iterations) — brute-forcing the
  password is computationally infeasible
- Fresh random salt and nonce on every encryption — encrypting the same
  message twice produces two completely different outputs
- Simple, responsive dark-themed GUI (resizable window, nothing gets hidden)
- Open/save `.txt` files directly from the app
- Copy the result to your clipboard in one click
- Zero network access required or performed

## Project structure

```
.
├── crypto_app.py       # the application (GUI + crypto logic)
├── requirements.txt    # Python dependencies
├── Makefile            # install / run / build shortcuts
└── README.md
```

## Quick start

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

make install     # install dependencies
make run         # launch the app
```

No `make` on your system? See the [Windows setup guide](#windows-setup-guide) below,
or run the equivalent commands directly:

```bash
python -m pip install -r requirements.txt
python crypto_app.py
```

## Building a standalone executable

To turn the app into a single double-clickable file that doesn't require
Python to be installed:

```bash
make build
```

or manually:

```bash
python -m pip install pyinstaller
python -m PyInstaller --onefile --windowed --name "EncryptedMessageTool" crypto_app.py
```

The executable will be in the `dist/` folder (`EncryptedMessageTool.exe` on
Windows, a `.app`-less binary on macOS/Linux). Build on the target OS —
PyInstaller does not cross-compile.

## Usage

1. Launch the app.
2. Type or paste your message in the text box.
3. Enter a secret key (shared only with the recipient).
4. Click **Encrypt** or **Decrypt**.
5. Use **Copy** to copy the result, or **Save .txt** to write it to a file.

The app is also compatible with the original `MODE:` / `CLE:` / `MESSAGE:`
file format if you open such a file with **Open .txt**.

## Windows setup guide

Most end users will be on Windows, where `pip` and `make` aren't always
available out of the box. Here's how to get everything running.

### 1. Install Python

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Windows installer
3. **Important:** check **"Add python.exe to PATH"** before clicking
   "Install Now"

### 2. Install Git Bash

Git Bash gives you a Linux-like terminal on Windows, so every command in
this README works as-is.

1. Go to [git-scm.com/downloads](https://git-scm.com/downloads)
2. Download and run the Windows installer
3. Keep the default options (just click "Next" through the wizard)
4. Right-click inside the project folder and choose **"Git Bash Here"**

### 3. Install Make (optional but recommended)

Git Bash doesn't ship with `make` by default.

**Option A — via Chocolatey**

1. Open PowerShell **as Administrator**
2. Install Chocolatey (command from
   [chocolatey.org/install](https://chocolatey.org/install)):
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```
3. Close and reopen PowerShell, then run:
   ```powershell
   choco install make
   ```
4. Reopen Git Bash and check with `make --version`

**Option B — standalone binary (no Chocolatey)**

1. Download "Complete package, except sources" from
   [gnuwin32 make](http://gnuwin32.sourceforge.net/packages/make.htm)
2. Install it normally ("Next, Next, Finish")
3. Add its `bin` folder (e.g. `C:\Program Files (x86)\GnuWin32\bin`) to your
   Windows PATH:
   - Search "Environment Variables" in the Start menu
   - Click "Environment Variables"
   - Under "System variables", select `Path` → "Edit" → "New"
   - Paste the `bin` folder path, confirm with "OK" everywhere
4. Reopen Git Bash and check with `make --version`

### 4. Run the project

```bash
make install
make run
```

If `make` still isn't cooperating, just use the direct commands from
[Quick start](#quick-start) instead — no `make` required.

## Troubleshooting

**`pip : the term 'pip' is not recognized...`**
Use `python -m pip install ...` instead of `pip install ...`. `make install`
already does this for you.

**`python : the term 'python' is not recognized...`**
Python isn't on your PATH. Reinstall it from
[python.org/downloads](https://www.python.org/downloads/) and check
**"Add python.exe to PATH"**.

**`No module named PyInstaller`**
The `python -m pip install pyinstaller` step failed or wasn't run. Re-run it
and make sure it completes without errors before building.

**`make : the term 'make' is not recognized...`**
`make` isn't installed (this is normal on Windows by default). Follow the
[Windows setup guide](#windows-setup-guide) above, or use the direct
commands from [Quick start](#quick-start), which don't need `make`.

## Security notes

- The secret key never leaves your machine and is never stored anywhere.
- Losing the key means the message cannot be recovered — there is no backdoor.
- This tool protects the confidentiality of a message's content; it does not
  hide the fact that you sent one, nor does it protect metadata.

## License

This project is not yet licensed. Consider adding a license (e.g. MIT) so
others know how they're allowed to use, modify, and distribute the code —
see [choosealicense.com](https://choosealicense.com/) for guidance.
