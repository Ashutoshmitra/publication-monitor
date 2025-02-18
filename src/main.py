import logging
import os
from datetime import datetime
import tempfile
from typing import Dict, Any
from .config import load_config
from .monitors.issuu import IssuuMonitor
from .storage.gdrive import GoogleDriveStorage
from .notifiers.email import EmailNotifier

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def setup_components(config: Dict[str, Any]):
    monitors = []
    if config["monitors"]["issuu"]["enabled"]:
        monitors.append(IssuuMonitor(config["monitors"]["issuu"]))
        
    storage = GoogleDriveStorage(config["storage"])
    
    notifiers = []
    if config["notifications"]["email"]["enabled"]:
        notifiers.append(EmailNotifier(config["notifications"]["email"]))
        
    return monitors, storage, notifiers

def process_publications(monitors, storage, notifiers):
    new_publications = []
    
    # Check for new publications
    for monitor in monitors:
        publications = monitor.check_new_publications()
        new_publications.extend(publications)
        
    if not new_publications:
        logging.info("No new publications found")
        return
        
    logging.info(f"Found {len(new_publications)} new publications")
    
    # Download and upload publications
    successful_publications = []
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for pub in new_publications:
            local_path = os.path.join(temp_dir, f"{pub['publication_id']}.pdf")
            
            # Download publication
            monitor = next(m for m in monitors if isinstance(m, type(pub["monitor"])))
            if monitor.download_publication(pub, local_path):
                # Upload to storage
                remote_id = storage.upload_file(
                    local_path,
                    f"{pub['publisher']}_{pub['title']}_{pub['date']}.pdf"
                )
                
                if remote_id:
                    pub["remote_id"] = remote_id
                    successful_publications.append(pub)
                else:
                    logging.error(f"Failed to upload {pub['title']} to storage")
            else:
                logging.error(f"Failed to download {pub['title']}")

    # Send notifications
    if successful_publications:
        for notifier in notifiers:
            notifier.notify(successful_publications)

def main():
    try:
        config = load_config()
        monitors, storage, notifiers = setup_components(config)
        process_publications(monitors, storage, notifiers)
    except Exception as e:
        logging.error(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    main()
