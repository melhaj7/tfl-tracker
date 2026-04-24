# TfL Live Data Pipeline

This project is a small end-to-end data engineering pipeline built around live TfL data.

The main goal was to build something that reflects real data engineering workflow: ingest raw API data, clean and model it through bronze, silver, and gold layers, and produce a final table that can answer a business question.

A second goal was to analyze the data and answer a business question about the TfL network. After exploring the dataset, I changed the original question to fit what the data could actually support.

## Why I Built This

I built this project to practice and show the kind of work a data engineer actually does:

- ingesting raw operational data
- designing layered data models
- cleaning and standardizing semi-structured data
- shaping raw data into tables that are easier to query and analyze
- changing the focus once I understood the limits of the data

I also wanted the project to have a business side, even if that part is smaller than the engineering side.

## Business Question

What did the TfL network look like at the captured live snapshots, and which lines and stations appeared busiest or most affected by disruptions?

## Architecture

The pipeline follows a medallion structure:

- **Bronze**: Raw API data ingested as-is for arrivals, disruptions, stop points, and timetables.
- **Silver**: Cleaned and standardized tables with parsed fields, typed columns, and basic quality filtering.
- **Gold**: A snapshot table for analysis that combines live arrivals, stop information, and disruption data.

## Gold Layer Output

Main gold table:

- `tfl_pipeline.gold.network_snapshot_summary`

Grain:

- one row per observed minute, line, station, and direction

This table includes:

- live service metrics such as prediction count and distinct vehicles
- predicted wait-time metrics
- stop metadata like zone, coordinates, and accessibility fields
- disruption information by line and snapshot date

## Focus Change

My original idea was to analyze network performance over time. After exploring the data, I changed the focus because the dataset did not support that kind of analysis strongly.

The data consisted of a small number of live snapshot pulls, and the arrivals data reflected predictions rather than confirmed train events. Because of that, I focused the gold layer on a snapshot-based view of the network instead of a trend or reliability study.

## Questions the Gold Table Supports

- Which lines and stations had the highest prediction activity at each captured snapshot?
- Which parts of the network were on disrupted lines?
- What stop features were common at those locations?
- How did the captured network state differ across the snapshot dates?

## Setup and Run

This project was built in Databricks.

### Requirements

- Databricks workspace
- access to the TfL API
- a Databricks secret scope named `tfl_scope`
- a secret key named `tfl_api_key`

### Clone the Repository

Clone the project into your Databricks workspace or Databricks Repo.

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### Project Structure
The project uses a shared src folder for configuration and reusable code.
```text
tfl-tracker/
├── notebooks/
├── src/
```
The notebooks resolve imports from src, so the folder structure should remain the same when the project is cloned into Databricks.

### Set Up the API Key
The bronze notebook reads the TfL API key from Databricks secrets:
```
APP_KEY = dbutils.secrets.get(scope="tfl_scope", key="tfl_api_key")
```
Before running the pipeline, create the following secrets in Databricks:

- **Secret scope:** `tfl_scope`
- **Secret key:** `tfl_api_key`

Then store your TfL API key there.

### Run Order
Run the notebooks in this order:

1. bronze_ingest
2. silver_transform
3. gold_transform
