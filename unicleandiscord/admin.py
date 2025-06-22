"""Admin site."""

from django.contrib import admin

from .models import DiscordChannel, DiscordGuild, MessageFilter

# Register your models for the admin site here.


@admin.register(DiscordGuild)
class DiscordGuildAdmin(admin.ModelAdmin):
    list_display = ("guild_id",)
    search_fields = ("guild_id",)


@admin.register(DiscordChannel)
class DiscordChannelAdmin(admin.ModelAdmin):
    list_display = ("channel_id", "guild")
    search_fields = ("channel_id", "guild__guild_id")
    list_filter = ("guild",)


@admin.register(MessageFilter)
class MessageFilterAdmin(admin.ModelAdmin):
    list_display = ("filter_text", "channel")
    search_fields = ("filter_text", "channel__channel_id")
    list_filter = ("channel",)
