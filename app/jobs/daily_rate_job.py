
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.services.rate_collector import collect_rates
from app.services.rate_store import save_rates

logger = logging.getLogger(__name__)

TIMEZONE = ZoneInfo("Asia/Kolkata")
MAX_LOOKBACK_DAYS = 7


def run_daily_rate_job():
    today = datetime.now(TIMEZONE).date()

    logger.info("Starting daily metal rates collection")
    logger.info("Searching for latest common date from %s", today)

    for days_back in range(MAX_LOOKBACK_DAYS + 1):
        target_date = today - timedelta(days=days_back)

        logger.info("Trying common date: %s", target_date)

        try:
            snapshot = collect_rates(target_date)

            save_rates(snapshot)

            logger.info(
                "SUCCESS: Saved common-date snapshot for %s",
                target_date,
            )

            return snapshot

        except (ValueError, RuntimeError) as exc:
            logger.warning(
                "Date %s unavailable: %s",
                target_date,
                exc,
            )

    raise RuntimeError(
        f"No complete common-date snapshot found "
        f"in the last {MAX_LOOKBACK_DAYS} days."
    )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    result = run_daily_rate_job()

    print("\nCollection completed!")
    print("Business date:", result["business_date"])
    print("Total rate records:", len(result["rates"]))
