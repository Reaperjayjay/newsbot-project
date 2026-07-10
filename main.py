#!/usr/bin/env python3
import sys
from typing import List

import config
from models import NewsArticle
from database import NotionManager
from clients import GNewsClient, MediaStackClient, CurrentsClient

class NewsAggregatorEngine:
    """Orchestrates ingestion routines and state modification pipelines across runtime objects."""
    
    def __init__(self):
        self.logger = config.setup_logging()
        
        if not config.NOTION_TOKEN or not config.DATABASE_ID:
            self.logger.critical("Initialization Error: Found null config references for NOTION_TOKEN or DATABASE_ID.")
            sys.exit(1)
            
        self.notion_manager = NotionManager(config.NOTION_TOKEN, config.DATABASE_ID, self.logger)
        self.api_clients = []
        
        # Instantiate clients depending on active token configurations
        if config.GNEWS_API_KEY:
            self.api_clients.append(GNewsClient(config.GNEWS_API_KEY, self.logger))
        else:
            self.logger.warning("Configuration token GNEWS_API_KEY missing. Pipeline tracking skipped.")
            
        if config.MEDIASTACK_API_KEY:
            self.api_clients.append(MediaStackClient(config.MEDIASTACK_API_KEY, self.logger))
        else:
            self.logger.warning("Configuration token MEDIASTACK_API_KEY missing. Pipeline tracking skipped.")
            
        if config.CURRENTS_API_KEY:
            self.api_clients.append(CurrentsClient(config.CURRENTS_API_KEY, self.logger))
        else:
            self.logger.warning("Configuration token CURRENTS_API_KEY missing. Pipeline tracking skipped.")
            
    def execute(self) -> None:
        """Process synchronous extraction routines, model mapping, and system validation checks."""
        self.logger.info("Launching System Pipeline Engine Operations...")
        
        if not self.api_clients:
            self.logger.critical("Termination: Operating state cannot continue with empty active ingestion engines.")
            sys.exit(1)
            
        if not self.notion_manager.ensure_database_properties():
            self.logger.error("Database connection constraints validation failure. Stopping process.")
            sys.exit(1)
            
        extracted_records = self._gather_all_records()
        if not extracted_records:
            self.logger.warning("Pipeline execution finalized with 0 runtime records managed.")
            return
            
        self.logger.info(f"Aggregate processing batch array loaded with {len(extracted_records)} items")
        
        committed, skipped, processing_faults = self.notion_manager.add_articles(extracted_records)
        self._generate_summary_report(committed, skipped, processing_faults, len(extracted_records))
        self.logger.info("Process pipeline closed safely.")

    def _gather_all_records(self) -> List[NewsArticle]:
        aggregated_items = []
        for integration_client in self.api_clients:
            try:
                dataset = integration_client.fetch_articles()
                aggregated_items.extend(dataset)
            except Exception as fatal_exception:
                client_type_name = integration_client.__class__.__name__
                self.logger.error(f"Critical operational error processing driver client {client_type_name}: {fatal_exception}")
                continue
        return aggregated_items

    def _generate_summary_report(self, added: int, skipped: int, errors: int, total: int) -> None:
        print("\n" + "="*60)
        print("PIPELINE TASK EXECUTION SUMMARY METRICS")
        print("="*60)
        print(f"Total Article Nodes Fetched: {total}")
        print(f"Documents Committed to Database: {added}")
        print(f"Entities Filtered (Invalid Schema/Duplicate): {skipped}")
        print(f"Transaction Write Failures: {errors}")
        print(f"Execution Accuracy Threshold Percentage: {(added / (total or 1)) * 100:.1f}%")
        print("="*60 + "\n")

def main():
    try:
        engine = NewsAggregatorEngine()
        engine.execute()
    except KeyboardInterrupt:
        print("\nProcess execution forced to close by explicit terminal interrupt signal.")
        sys.exit(1)
    except Exception as runtime_fault:
        print(f"Fatal System Context Interruption: {runtime_fault}")
        sys.exit(1)

if __name__ == "__main__":
    main()