# unicleandiscord plugin app for Alliance Auth

A simple task app that cleans up uni discord

CELERYBEAT_SCHEDULE["discord_cleanup_fetch_messages"] = {
    "task": "unicleandiscord.tasks.fetch_discord_messages",
    "schedule": crontab(minute="*/10"),
}
