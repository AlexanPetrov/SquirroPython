import logging
import time
from nytimes_source import NYTimesSource
from logging_config import configure_logging
import argparse
from dotenv import load_dotenv

load_dotenv()

configure_logging()

if __name__ == "__main__":
    """Command-line arguments"""
    parser = argparse.ArgumentParser(description="Fetch NYTimes Articles.")
    parser.add_argument("--max_batches", type=int, help="Maximum number of batches to fetch.", default=None)
    parser.add_argument("--show_all", action="store_true", help="Show all items in each batch.")
    parser.add_argument("--max_retries", type=int, default=5, help="Maximum number of retries for API rate-limiting.")
    parser.add_argument("--initial_delay", type=int, default=10, help="Initial delay between retries (in seconds).")
    args = parser.parse_args()

    """Configuration Parameters"""
    QUERY = "Silicon Valley"
    BATCH_SIZE = 10
    MAX_BATCHES = args.max_batches

    nyt_source = NYTimesSource()

    try:
        nyt_source.connect()

        start_time = time.time()
        total_articles = 0
        batch_count = 0
        """Batch Iterations"""
        for idx, batch in enumerate(nyt_source.getDataBatch(BATCH_SIZE)):
            batch_count += 1
            print(f"Batch {idx + 1}: {len(batch)} items")
            for item in (batch if args.show_all else batch[:3]):
                print(f" - {item.get('headline.main', 'No Headline')}")
            if len(batch) > 3 and not args.show_all:
                print(f"...and {len(batch) - 3} more items.\n")

            total_articles += len(batch)

            if MAX_BATCHES and batch_count >= MAX_BATCHES:
                logging.info(f"Reached the maximum of {MAX_BATCHES} batches. Stopping...")
                break

        elapsed_time = time.time() - start_time
        logging.info(f"\nSummary: Total batches: {batch_count}, Total articles: {total_articles}, Time: {elapsed_time:.2f}s.")

    except KeyboardInterrupt:
        logging.warning("Process interrupted by user. Disconnecting...")
        logging.info(f"Total batches fetched: {batch_count}. Total articles fetched: {total_articles}.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        nyt_source.disconnect()
        logging.info("Disconnected from the API.")
