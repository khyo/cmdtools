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
