# Overview

clope (see-lope) is a Python package for interacting with the Cantaloupe/Seed vending system. Primarily being a wrapper for their Spotlight API. It uses the pandas library to return information from a given spotlight report as a dataframe object. clope also has functionality for connecting to the snowflake data warehouse Cantaloupe product as well.

## Installation

`pip install clope`

## Usage

Several environment variables are required for clope to function. Functionality is divided into two modules, so vars are only required if you are using functions from that particular module.

| Module | Required? | Env Variable | Description |
| --------- | --------- | ------------ | ----------- |
| Spotlight | Yes       | CLO_USERNAME | Username of the Spotlight API user. Should be provided by Cantaloupe. |
| Spotlight | Yes       | CLO_PASSWORD | Password of the Spotlight API user. Should be provided by Cantaloupe. |
| Spotlight | No        | CLO_BASE_URL | Not actually sure if this varies between clients. I have this as an optional variable in case it does. Default value if no env variable is <https://api.mycantaloupe.com>, otherwise can be overridden. |
| Spotlight | No        | CLO_ARCHIVE_FILES | Optional variable. Will archive the interim excel files that run_report() generates so can be later looked at in the Archive folder. Default behavior is to not archive and simply delete the excel files after data is pulled from them. |
| Snowflake | Yes | SNOWFLAKE_USER | Username of the Snowflake user |
| Snowflake | Yes | SNOWFLAKE_PASSWORD | Password of the snowflake user |
| Snowflake | Yes | SNOWFLAKE_ACCOUNT | Snowflake account you're connecting to. Should be something along the lines of "{Cantaloupe account}-{Your Company Name}" |
| Snowflake | Yes | SNOWFLAKE_DATABASE | Snowflake database to connect to. Likely begins with "PRD_SEED...". |

## Spotlight

The spotlight module invloves interaction with the Cantaloupe Spotlight API. The API essentially allows remotely run a spotlight report and getting the raw excel data via HTTP requests. Reports must be set up in the browser prior to using the API. Fairly quick and suited for getting data that needs to be up-to-date at that moment.

### Run Spotlight Report (run_report())

The primary function. Used to run a spotlight report, retrieve the excel results, and transform the excel file into a workable pandas dataframe. Cantaloupe's spotlight reports return an excel file with two tabs: Report and Stats. This pulls the info from the Report tab, Stats is ignored.

> Note: Make sure your spotlight report has been shared with the "Seed Spotlight API Users" security group in Seed Office. Won't be accessible otherwise.

Takes in two parameters:

*report_id*

A string ID for the report in Cantaloupe. When logged into Seed Office, the report ID can be found in the URL. E.G. <https://mycantaloupe.com/cs3/ReportsEdit/Run?ReportId=XXXXX>, XXXXX being the report ID needed.

*params*

Optional parameter, list of tuples of strings. Some Spotlight reports have required filters which must be supplied to get data back. Date ranges being a common one. Cantaloupe's error messages are fairly clear, in my experience, with telling you what parameteres are needed to run the report and in what format they should be. First element of tuple is filter name and second is filter value. Filter names are in format of "filter0", "filter1", "filter2", etc.

Example call

```python
# Import package
from clope import run_report

# Run report with a report_id and additional parameters
df_report = run_report('123', [('filter0', '2024-01-01'), ('filter0', '2024-01-31')])
```

## Snowflake

Cantaloupe also offers a data warehouse product in Snowflake. Good for aggregating lots of information, as well as pulling historical information. However, notably, data is only pushed from Seed into the Snowflake data warehouse once a day, so it is not necessarily going to be accurate as of that moment.

Also something to keep in mind is that the system makes use of SCD (slowly changing dimension) in order to keep track of historical info vs current info. So some care should be taken when interpreting the data.

For each dataset that uses SCD, a parameter has been included to restrict to current data only or include all data.

### Dates

In Snowflake, most date columns are represented by an integer key, rather than the date itself. A couple functions are included with regards to dates. If working directly with Snowflake, you would join the date table onto the fact table you're working with. However, from what I can see the dates are largely deterministic. 1 is 1900-01-01, 2 is 1900-01-02. So I just directly translate from key to date and vice versa with some date math. Much quicker and should give same results as querying the date table itself.

### Dimensions

Dimensions describe facts. The location something happened in. The route it happened on. Dimensions generally change over time and make the most use of the SCD schema.

- Barcodes (for each pack)
- Branches
- Coils (planogram slots)
- Customers
- Devices (telemetry)
- Item Packs (UOMs)
- Items
- Lines of Business
- Locations
- Machines
- Micromarkets
- Operators
- Routes
- Supplier Branch
- Supplier Items (Not yet used seemingly)
- Suppliers
- Warehouses
- Machine Alerts

### Facts

A fact is the central information being stored. Generally, things that are not changing. A sale, an inventory, a product movement.

- Cashless Vending Tranaction
- Collection Micromarket Sales
- Order to Fulfillment (Delivery)
- Order to Fulfillment (Vending and Micromarket)
- Delivery Order Receive
- Sales Revenue By Day
- Sales Revenue By Visit
- Sales By Coil
- Scheduling Machine
- Scheduling Route Summary
- Telemetry Sales
- Vending Micromarket Visit
- Warehouse Inventory
- Warehouse Observed Inventory
- Warehouse Product Movement
- Warehouse Purchase
- Warehouse Receive

### Functions

Also included in Cantaloupe's Snowflake are a couple functions. General intention seems to be gathering a subset of data from a couple core fact tables. Haven't yet implemented wrappers for these.
