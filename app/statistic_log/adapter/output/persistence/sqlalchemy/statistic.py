from app.statistic_log.domain.repository.statistic import StatisticRepo
from core.db.clickhouse_db import clickhouse_manager
from datetime import datetime
import json


class StatistisLogRepo(StatisticRepo):
    async def create_log(self, *, data) -> None:
        try:
            # clickhouse_manager = ClickHouse()
            # Insert the data into ClickHouse
            record = {
                "user": data.user,
                "message_id": data.message_id,
                "conversation_id": data.conversation_id,
                "timestamp_chat": datetime.now(),
                "statistic_data_url": data.statistic_data.url,
                "statistic_data_page_title": data.statistic_data.page_title,
                "statistic_data_page_metadata": json.dumps(data.statistic_data.page_metadata),
                "statistic_data_page_keywords": data.statistic_data.page_keywords,
                "statistic_data_session_history_url": data.statistic_data.session_history_url,
                "statistic_data_focus_content_snippet": json.dumps(data.statistic_data.focus_content_snippet),
                "statistic_data_reading_duration_ms": data.statistic_data.reading_duration_ms,
                "statistic_data_cookies": json.dumps(data.statistic_data.cookies),
                "error_message": data.error_message,
            }
            await clickhouse_manager.insert_many("statistic_logs", [record])
            
        except Exception as e:
            raise Exception(str(e))