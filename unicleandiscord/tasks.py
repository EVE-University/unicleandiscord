import time

import requests
from celery import shared_task

from django.conf import settings

from allianceauth.services.hooks import get_extension_logger

from .models import DiscordChannel, MessageFilter

logger = get_extension_logger(__name__)

DISCORD_API_BASE = "https://discord.com/api"


@shared_task
def fetch_discord_messages():
    headers = {"Authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"}

    logger.info("Starting Discord Cleanup")

    for channel in DiscordChannel.objects.select_related("guild"):
        logger.info(f"Checking channel {channel.channel_id}")

        filters = list(
            MessageFilter.objects.filter(channel=channel).values_list(
                "filter_text", flat=True
            )
        )

        if not filters:
            continue

        url = f"{DISCORD_API_BASE}/channels/{channel.channel_id}/messages"
        try:
            response = requests.get(url, headers=headers, params={"limit": 100})
            response.raise_for_status()
            messages = response.json()

            for msg in messages:
                time.sleep(1)
                content = msg.get("content", "")
                msg_id = msg.get("id")

                for filter_text in filters:
                    if filter_text in content:
                        logger.info(
                            f"[MATCH] Deleting message {msg_id} in channel {channel.channel_id}: '{content}'"
                        )
                        delete_url = f"{DISCORD_API_BASE}/channels/{channel.channel_id}/messages/{msg_id}"
                        del_resp = requests.delete(delete_url, headers=headers)

                        if del_resp.status_code in (204, 200):
                            logger.info(f"Deleted message {msg_id}")
                        else:
                            logger.warning(
                                f"Failed to delete message {msg_id}: {del_resp.status_code} - {del_resp.text}"
                            )
                        break  # One match is enough — stop checking other filters
        except requests.HTTPError as e:
            logger.error(
                f"HTTP error for channel {channel.channel_id}: {e.response.status_code} - {e.response.text}"
            )
        except Exception as e:
            logger.exception(
                f"Unexpected error for channel {channel.channel_id} error {e}"
            )
