# Git Mirror

Mirror all of your projects between GitHub and GitLab with ease.

## Installation

1) Clone repository:

```sh
git clone https://git.douglas-parker.com/douglasparker/git-mirror.git /opt/git-mirror
```

2) Install Python Package Manager:
```sh
sudo apt install python3-pip
```

3) Install Python requests:
```sh
pip install requests
```

## Usage

1) Make executable:
```sh
chmod +x /opt/git-mirror/git-mirror.py
```

2) Run Git Mirror (Generate configuration):
```sh
/opt/git-mirror/git-mirror.py
```

3) Edit configuration:
```sh
nano /opt/git-mirror/cfg.py
```

4) Run Git Mirror:
```sh
/opt/git-mirror/git-mirror.py
```