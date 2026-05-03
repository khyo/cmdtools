# Command-Line Tools and Helpers

Use them if they are helpful. Ignore them if they arent.

## SD (Systemctl Daemon Helper)

`sd` allows easier systemctl daemon usage patterns. For instance

- `sd siapi -r` restarts the siapi service with sudo privileges.
- `sd siapi -p` stop the service with sudo privileges
- since the verb acting on the service is the final argument, it is more ergonmic to swap out the verb with a single backspace and character press.

## XG (git commandline helper)

`xg` helps speed up routine git commands. For example:

- `xg p any thing you want` translates to `git add . && git commit -m"any thing you want" && git push`

# URL Dispatcher

```bash
chmod +x cmdtools/url_dispatcher.py
# replace Exec=/home/xerous/subinitial/git/khyo/cmdtools/cmdtools/url_dispatcher.py with proper path
cp cmdtools/url_dispatcher.desktop ~/.local/share/applications
chmod +x ~/.local/share/applications/url_dispatcher.desktop
sudo update-desktop-database
xdg-mime default url_dispatcher.desktop x-scheme-handler/http
xdg-mime default url_dispatcher.desktop x-scheme-handler/https
```

# Brave Browser Router

## Setup

```bash
cp cmdtools/brave-browser-router.desktop ~/.local/share/applications
update-desktop-database ~/.local/share/applications
xdg-settings set default-web-browser brave-browser-router.desktop
xdg-mime default brave-browser-router.desktop x-scheme-handler/http
xdg-mime default brave-browser-router.desktop x-scheme-handler/https
```

## Verification

```bash
# Check the router is registered
xdg-settings get default-web-browser
# → brave-browser-router.desktop

xdg-mime query default x-scheme-handler/https
# → brave-browser-router.desktop

# Test routing directly
~/.local/bin/brave-browser-router https://netflix.com       # should open Brave
~/.local/bin/brave-browser-router https://news.ycombinator.com  # should open Zen
~/.local/bin/brave-browser-router --app=https://chat.openai.com # should open Brave as webapp
~/.local/bin/brave-browser-router                           # should open Zen (no URL)

# Test via xdg-open (simulates link clicks from other apps)
xdg-open https://github.com

# Test Omarchy webapp install (Super+Alt+Space → Install → Web App)
# The generated .desktop should call omarchy-launch-webapp, which reads
# xdg default (brave-browser-router), matches the brave-browser* glob,
# and invokes your router with --app=URL.
```
