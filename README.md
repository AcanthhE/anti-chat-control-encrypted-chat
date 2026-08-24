# anti-chat-control-encrypted-chat
provide a program to use to encrypt et decode a message for counter chat control UE

# FileCrypto (AES-256)

Un outil de chiffrement de texte ultra-sécurité, léger et autonome écrit en Python. Il permet de chiffrer et déchiffrer des messages directement dans un fichier texte local, sans passer par aucun serveur distant.

Projet conçu pour garantir une confidentialité totale des échanges (protection contre la surveillance de masse / Chat Control).

---

## Fonctionnalités

* **Chiffrement AES-256-GCM :** Standard militaire mondial. Authentification du message incluse (détecte toute modification du texte).
* **Protection par Seed / Mot de passe :** La clé de dérivation `PBKDF2HMAC` (600 000 itérations) rend les attaques par force brute virtuellement impossibles.
* **In-Place File Processing :** Le programme lit, chiffre (ou déchiffre) et remplace le contenu directement dans le fichier `.txt`.
* **Sécurité dynamique :** Un sel (*salt*) et un *nonce* aléatoires sont générés à chaque exécution. Deux chiffrements du même texte produisent deux résultats totalement différents (aucune possibilité de repérer des motifs ou *patterns*).

---

## Prérequis

Installez la bibliothèque cryptographique officielle :

```bash
pip install cryptography
