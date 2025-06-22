# unicleandiscord plugin app for Alliance Auth

A simple task app that cleans up uni discord

Add to Installed Apps
```python
    'unicleandiscord',
```


Add to local.py
```python
CELERYBEAT_SCHEDULE["discord_cleanup_fetch_messages"] = {
    "task": "unicleandiscord.tasks.fetch_discord_messages",
    "schedule": crontab(minute="*/10"),
}
```
