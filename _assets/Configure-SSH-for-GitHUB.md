## Configure SSH for GitHUB

This guide shows how to set up SSH for GitHub on macOS in a compact, classic way.

## 1. Check existing SSH keys
```bash
ls -al ~/.ssh
```
If you see id_ed25519.pub or id_rsa.pub, you may reuse them. Otherwise, create a new key.

## 2. Create new ssh keys

Recommended (Ed25519):
```bash
ssh-keygen -t ed25519 -C "your-github-email@example.com" -f id_yourkey
```
Fallback (older version of mac os)
```bash
ssh-keygen -t rsa -b 4096 -C "your-github-email@example.com" -f id_yourkey
```
Press Enter to accept the default file location and optionally set a passphrase.

## 3. Start ssh-agent and configure SSH

Start the agent:

```bash
eval "$(ssh-agent -s)"
````
Edit SSH config:
```bash
vi ~/.ssh/config
```
Add:
```bash
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_yourkey
  AddKeysToAgent yes
  UseKeychain yes
```
Save and Exit, then add to the key
```bash
ssh-add --apple-use-keychain ~/.ssh/id_yourkey
# falls back if needed:
# ssh-add ~/.ssh/id_ed25519
```

## 4. Add your public key to GitHub

Show your public key:
```bash
cat ~/.ssh/id_yourkey.pub
```

Copy the full line.

On GitHub:
1.	Settings → SSH and GPG keys
2.	New SSH key
3.	Give it a title (e.g. MacBook)
4.	Paste the key
5.	Save

## 5. Test the SSH connection
```bash
ssh -T git@github.com
````
Type yes when asked about the host.
Success looks like:
```bash
Hi <your-username>! You've successfully authenticated, but GitHub does not provide shell access.```