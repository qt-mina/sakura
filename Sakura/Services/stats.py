# Sakura/Services/stats.py
import time
import psutil
import datetime
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

        current_time = datetime.datetime.now()
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()

        db_stats = {
            'users_count': len(state.user_ids),
            'groups_count': len(state.group_ids),
            'total_purchases': 0,
            'total_revenue': 0,
            'active_conversations': len(state.conversation_history)
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

                    recent_users = await conn.fetchval("""
                        SELECT COUNT(*) FROM users
                        WHERE updated_at > NOW() - INTERVAL '24 hours'
                    """)
                    db_stats['recent_users'] = recent_users or 0

                    recent_purchases = await conn.fetchval("""
                        SELECT COUNT(*) FROM purchases
                        WHERE created_at > NOW() - INTERVAL '24 hours'
                    """)
                    db_stats['recent_purchases'] = recent_purchases or 0
            except Exception as e:
                log_action("ERROR", f"Error getting database stats: {e}", {})

        stats_message = f"""📊 <b>Sakura Bot Statistics</b>
<i>Last Updated: {current_time.strftime('%H:%M:%S')}</i>

🏓 <b>Bot Performance</b>
├ Uptime: <b>{uptime_str}</b>
└ Ping: <b>{ping_ms}ms</b>

👥 <b>User Statistics</b>
├ Total Users: <b>{db_stats['users_count']}</b>
├ Total Groups: <b>{db_stats['groups_count']}</b>
├ Recent Users (24h): <b>{db_stats.get('recent_users', 'N/A')}</b>
├ Active Conversations: <b>{db_stats['active_conversations']}</b>
├ Total Purchases: <b>{db_stats['total_purchases']}</b>
├ Total Revenue: <b>{db_stats['total_revenue']} ⭐</b>
└ Recent Purchases (24h): <b>{db_stats.get('recent_purchases', 'N/A')}</b>

🖥️ <b>System Resources</b>
├ CPU Usage: <b>{cpu_percent}%</b>
└ Memory: <b>{memory.percent}%</b> ({memory.used // (1024 ** 3)}GB / {memory.total // (1024 ** 3)}GB)"""

        keyboard = [[InlineKeyboardButton("🔄 Refresh", callback_data="refresh_stats")]]
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
