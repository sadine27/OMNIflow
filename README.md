# OMNIflow

Small Python pipeline that feeds product data into an n8n workflow.

- `retailer_product_extractor.py` — authenticates with the CJ Dropshipping API, pages through search results (e.g. keyword "Laptop") and saves them to CSV.
- `webhook.py` — uploads that CSV to an n8n webhook for downstream processing.

## Setup
```bash
pip install requests pandas python-dotenv
```
Create a `.env` with `apiKey_CJ_dropshipping`, `CJ_Access_Token` and `n8n_web_hook_URL`, then run the extractor followed by `webhook.py`.

> Note: `webhook.py` currently reads the CSV from a hard-coded local path (`D:/scripts/...`); change it to match your machine.
