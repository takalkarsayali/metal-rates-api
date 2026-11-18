
import logging

from app.jobs.daily_rate_job import run_daily_rate_job


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


if __name__ == "__main__":
    result = run_daily_rate_job()

    print("\nMetal rates collection completed!")
    print("Business date:", result["business_date"])
    print("Total rate records:", len(result["rates"]))
