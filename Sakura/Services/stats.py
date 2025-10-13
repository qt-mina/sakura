# Sakura/Services/stats.py
import time
import psutil
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, LinkPreviewOptions
from pyrogram.enums import ParseMode
from Sakura.Core.helpers import log_action
from Sakura import state

async def send_stats(chat_id: int, client: Client, is_refresh: bool = False):
    """Send or update stats message with current data"""
    try:
        ping_start = time.time()
        try:
            await client.get_me()
            ping_ms = round((time.time() - ping_start) * 1000, 2)
        except Exception:
            ping_ms = "Error"

        process = psutil.Process()
        process_start = process.create_time()
        uptime_seconds = time.time() - process_start
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        uptime_str = f"{days}d {hours}h {minutes}m"

        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()

        db_stats = {
            'users_count': len(state.user_ids),
            'groups_count': len(state.group_ids),
            'total_purchases': 0,
            'total_revenue': 0
        }

        if state.db_pool:
            try:
                async with state.db_pool.acquire() as conn:
                    purchase_stats = await conn.fetchrow("""
                        SELECT COUNT(*) as total_purchases, COALESCE(SUM(amount), 0) as total_revenue
                        FROM purchases
                    """)
                    if purchase_stats:
                        db_stats['total_purchases'] = purchase_stats['total_purchases']
                        db_stats['total_revenue'] = purchase_stats['total_revenue']
            except Exception as e:
                log_action("ERROR", f"Error getting database stats: {e}", {})

        stats_message = f"""<b>Statistics and info</b> 🌸

<blockquote>🏓 <b>Bot Performance</b>
├ Uptime: {uptime_str}
└ Ping: {ping_ms}ms</blockquote>
<blockquote>👥 User Statistics
├ Total Users: {db_stats['users_count']}
├ Total Groups: {db_stats['groups_count']}
├ Total Purchases: {db_stats['total_purchases']}
└ Total Revenue: {db_stats['total_revenue']} ⭐</blockquote>
<blockquote>📡 System Resources
├ CPU Usage: {cpu_percent}%
└ Memory: {memory.percent}% ({memory.used // (1024 ** 3)}GB / {memory.total // (1024 ** 3)}GB)</blockquote>"""

        keyboard = [[InlineKeyboardButton("☘️ Refresh", callback_data="refresh_stats")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if is_refresh:
            return stats_message, reply_markup
        else:
            await client.send_message(
                chat_id=chat_id,
                text=stats_message,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
                link_preview_options=LinkPreviewOptions(is_disabled=True)
            )

    except Exception as e:
        log_action("ERROR", f"❌ Error generating stats message: {e}", {})
        if not is_refresh:
            await client.send_message(chat_id, "❌ Error generating statistics!")