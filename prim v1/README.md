---

### Instructions & Usage
1. Create the Input File (message.txt)

Create a text file structured as follows:

```
MODE: true
KEY: YourUniqueSeedOrPassword
MESSAGE:
Write your confidential message here...
```

* MODE: true -> Set to encrypt the text.
* MODE: false -> Set to decrypt the text.
* KEY: Your secret key/seed (shared only between you and the recipient).
* MESSAGE: The payload to process.

2. Run the Script

Execute the script by passing your text file as an argument:
Bash

`python script.py message.txt`

3. Execution Result

    The message.txt file is modified directly in place.
    The raw message is replaced by a Base64-encoded encrypted string.
    MODE automatically toggles to false to prepare for subsequent decryption.
    To decrypt: Run the exact same command (python script.py message.txt) again.

Is it truly unbreakable?

Yes. Unlike legacy ciphers (Caesar, basic XOR) or common misconceptions:

  Zero Patterns: The encrypted output is indistinguishable from mathematical white noise.
  Text Length: Whether your message is 3 words or 50 pages long, security remains at maximum strength.
  Cracking: Without the exact key, cracking the cipher would take billions of years using current supercomputers.

## Prerequisites

Install the official Python cryptography library:

```bash
pip install cryptography
