# Project Overview

Agentic Facebook Performance Analyst.

## Architecture

![Workflow](./media/workflow.png)  
Workflow of the system.

## Training Flow

![Prompts in Arize Pheonix](./media/pheonix_prompts.png)  
Prompts are tracked in Arize Pheonix: Open-Source AI & Agent Engineering Platform for development, observability, and evaluation.

## Deployment Diagram

![Prompt Versioning](./media/pheonix_prompts_versions.png)  
Each time a prompt is changed, its version is updated in Arize Pheonix.


## Data Layer

The project uses Supabase as the backend for storing all Facebook Ads performance data. Instead of loading local CSV files, the system fetches data directly from the Supabase database. This is handled through the `query_db` function located in `src/utils/supabase_client.py`, which provides a clean interface for executing SQL queries and retrieving results for the agentic pipeline.
