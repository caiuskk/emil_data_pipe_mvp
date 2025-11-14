# EMIL Data Pipe MVP

Small reusable Python client + scripts for pulling ERCOT EMIL reports via the Public API.
Current focus: `NP3-911-ER` 2-Day Aggregated AS Offers (`2d_agg_as_offers_ecrsm`).

This project has been tested with **Python 3.10+**.

## 1. Setup

```bash
git clone <this repo>
cd emil_data_pipe_mvp
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Set up config

make a copy of `.env.exmaple` and save as `.env`
fill in required keys in the `.env`, which requires your own registration from ERCOT

## 3. Mvp run

```bash
python -m tests.test_token # test if your keys ready
python -m scripts.fetch_np3_agg_as_offers --from-date 2025-01-01 --to-date 2025-01-02 -o out/offers_20250101_02.csv # simple test, saved as csv for furture connecting to Palentier usage
```

## Mermaid notes

flowchart TD

    %% Entry point
    A[CLI Script\nscripts/fetch_np3_agg_as_offers.py]
        -->|Parse CLI args\n(from-date, to-date, hour filters)|
        B[ercot_emil.api\nget_np3_agg_as_offers_ecrsm()]

    %% Config & Auth Module
    subgraph CONFIG[Config & Authentication]
        C[config.py\n- Load .env\n- BASE_URL\n- TOKEN_URL\n- CLIENT_ID\n- SUB_KEY]
        D[auth.py\nget_id_token()\n- Build token payload\n- POST token URL\n- Cache token]
    end

    %% API layer
    B -->|Build params dict\n(deliveryDateFrom/To, HE ranges, etc.)|
         E[ercot_emil.client\nget_report_df(path, params)]

    E --> C
    E --> D

    %% HTTP call to ERCOT
    E -->|GET BASE_URL + path\nHeaders: Bearer Token + SUB_KEY\nParams: Query filters|
         F[(ERCOT Public API\n/public-reports/np3-911-er/2d_agg_as_offers_ecrsm)]

    %% JSON returned
    F -->|JSON Response:\n_meta, report, fields, data, links|
         G[ercot_emil.parse\nemil_json_to_df()]

    %% Parsing layer
    G -->|Use 'fields' → column names\nUse 'data' → rows\n(list-of-lists or list-of-dicts)|
         H[(pandas DataFrame)]

    %% Output layer
    H -->|Script prints DF head or saves CSV|
         I[Terminal Output / CSV File]

    %% Dependencies
    C -->|Provide BASE_URL & SUB_KEY| E
    C -->|Provide Token URL / Client ID| D
