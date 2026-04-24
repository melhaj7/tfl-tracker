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

## Example Outputs

### Preview of the final gold table
Here is an example of the final gold-layer table that was produced by the pipeline (limit 5).

|snapshot_observed_at|snapshot_date|line_id|line_name|naptan_id|station_name|common_name|direction|zone|lat|lon|stop_type|is_active|has_lifts|has_wifi|has_toilets|has_car_park|has_waiting_room|help_points|prediction_count|distinct_vehicle_count|avg_time_to_station_sec|median_time_to_station_sec|min_time_to_station_sec|max_time_to_station_sec|distinct_destinations|has_active_disruption|active_disruption_count|disruption_categories|disruption_types|disruption_descriptions|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|2026-04-21T14:37:00.000Z|2026-04-21|jubilee|Jubilee|940GZZLUWHM|West Ham Underground Station|West Ham Underground Station|outbound|2/3|51.528136|0.005055|NaptanMetroStation|true|false|true|false|false|false|0 on platforms, 0 in ticket halls, 0 elsewhere|18|1|808.7|659|178|1439|1|true|6|["RealTime"]|["lineInfo"]|["Jubilee Line: Service is operating at a reduced frequency on the entire line every 6 minutes due to strike action. Services will finish early tonight so please complete your journey by 20:00."]|
|2026-04-21T14:37:00.000Z|2026-04-21|lioness|Lioness|910GWMBY|Wembley Central Rail Station|Wembley Central Rail Station|inbound|4|51.552325|-0.296433|NaptanRailStation|true|false|true|false|false|true|6 on platforms, 0 in ticket halls, 0 elsewhere|24|8|3370.8|2852|222|6512|1|false|0|null|null|null|
|2026-04-21T14:37:00.000Z|2026-04-21|bakerloo|Bakerloo|940GZZLUCHX|Charing Cross Underground Station|Charing Cross Underground Station|inbound|1|51.50741|-0.127277|NaptanMetroStation|true|false|true|false|false|false|0 on platforms, 0 in ticket halls, 0 elsewhere|12|4|726|546|306|1206|1|true|12|["RealTime"]|["lineInfo","routeInfo"]|["Bakerloo Line: Service is operating at a reduced frequency between Elephant & Castle and Queen's Park every 8 minutes, and between Queen's Park and Harrow & Wealdstone every 15 minutes due to strike action. Services will finish early tonight so please complete your journey by 20:00."]|
|2026-04-21T14:37:00.000Z|2026-04-21|central|Central|940GZZLUBKE|Barkingside Underground Station|Barkingside Underground Station|outbound|4|51.585689|0.088585|NaptanMetroStation|true|false|true|false|true|true|0 on platforms, 0 in ticket halls, 0 elsewhere|12|4|883.5|898|119|1439|1|true|12|["RealTime"]|["routeBlocking","lineInfo"]|["Central Line: Service is operating at a reduced frequency between White City and Ealing Broadway / West Ruislip every 10 minutes, between Liverpool Street and Leytonstone every 5 minutes and between Leytonstone and Hainault / Epping every 10 minutes. No service on the rest of the line due to strike action. Services will finish early tonight so please complete your journey by 20:00."]|
|2026-04-21T14:37:00.000Z|2026-04-21|victoria|Victoria|940GZZLUWWL|Walthamstow Central Underground Station|Walthamstow Central Underground Station|null|3|51.582965|-0.019885|NaptanMetroStation|true|false|true|false|false|false|0 on platforms, 0 in ticket halls, 0 elsewhere|54|9|852.4|776|25|1676|1|true|6|["RealTime"]|["lineInfo"]|["Victoria Line: Service is operating at a reduced frequency on the entire line every 5 minutes due to strike action. Services will finish early tonight so please complete your journey by 20:00."]|




### Most Active Stations in the Captured Snapshots
This is a list of the most active line and station combinations across the captured snapshots (limit 5).


|snapshot_observed_at|line_id|station_name|direction|prediction_count|distinct_vehicle_count|avg_time_to_station_sec|has_active_disruption|
|---|---|---|---|---|---|---|---|
|2026-04-21T14:43:00.000Z|elizabeth|Whitechapel Rail Station||246|82|3833|false|
|2026-04-21T14:37:00.000Z|elizabeth|Whitechapel Rail Station||243|81|3894.1|false|
|2026-04-21T14:43:00.000Z|elizabeth|Farringdon Rail Station||237|79|3714.3|false|
|2026-04-21T14:37:00.000Z|elizabeth|Farringdon Rail Station||237|79|3814.3|false|
|2026-04-21T14:43:00.000Z|windrush|Shoreditch High Street Rail Station|outbound|141|47|3550.3|true|



### Disrupted lines in the captured snapshots
Lines that have been affected by disruptions in the snapshots, along with the number of related disruption records (limit 5).

|line_id|rows_on_disrupted_snapshots|disruption_count|
|---|---|---|
|piccadilly|210|12|
|district|184|12|
|central|179|12|
|metropolitan|159|12|
|hammersmith-city|134|12|
|bakerloo|90|12|
|northern|194|6|
|windrush|174|6|
|jubilee|166|6|
|victoria|59|6|
|circle|39|6|
|waterloo-city|3|6|
|mildmay|73|2|
