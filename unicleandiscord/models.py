"""Models."""

from django.db import models


class General(models.Model):
    """A meta model for app permissions."""

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (("basic_access", "Can access this app"),)


class DiscordGuild(models.Model):
    guild_id = models.BigIntegerField(unique=True)

    def __str__(self):
        return f"Guild {self.guild_id}"


class DiscordChannel(models.Model):
    channel_id = models.BigIntegerField(unique=True)
    guild = models.ForeignKey(
        DiscordGuild, related_name="channels", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Channel {self.channel_id} (Guild {self.guild.guild_id})"


class MessageFilter(models.Model):
    channel = models.ForeignKey(
        DiscordChannel, related_name="filters", on_delete=models.CASCADE
    )
    filter_text = models.CharField(max_length=1024)

    def __str__(self):
        return f"Filter '{self.filter_text}' in Channel {self.channel.channel_id}"
