# Overview

clope is a Python package for interacting with the Cantaloupe/Seed Pro system. clope touches a couple different APIs/interfaces: the Spotlight reporting API, the Snowflake data warehouse, and the Prepick SOAP interface. All relate to Cantaloupe but have different credentials and are separate add-ons.

## Installation

Each of the three modules is separated into optional dependency groups so that you only pull in the dependencies you need. A base install will not include any dependencies (Note: this differs from previous releases where spotlight module was treated as the default).

```
# All modules/dependencies
pip install "clope[all]"

# Spotlight only
pip install "clope[spotlight]"

# Prepick and Snowflake
pip install "clope[prepick,snow]"

# etc., whatever combos
```

## Usage

Several environment variables are required for clope to function. Functionality is divided into three modules, so vars are only required if you are using functions from that particular module.

| Module | Required? | Env Variable | Description |
| --------- | --------- | ------------ | ----------- |
| Spotlight | Yes       | CLO_USERNAME | Username of the Spotlight API user. Should be provided by Cantaloupe. |
| Spotlight | Yes       | CLO_PASSWORD | Password of the Spotlight API user. Should be provided by Cantaloupe. |
| Spotlight | No        | CLO_BASE_URL | Not actually sure if this varies between clients. I have this as an optional variable in case it does. Default value if no env variable is <https://api.mycantaloupe.com>, otherwise can be overridden. |
| Snowflake | Yes | SNOWFLAKE_USER | Username of the Snowflake user |
| Snowflake | Yes | SNOWFLAKE_PRIVATE_KEY_FILE | Path pointing to the private key file for the Snowflake user. |
| Snowflake | Yes | SNOWFLAKE_PRIVATE_KEY_FILE_PWD | Password for the private key file |
| Snowflake | Yes | SNOWFLAKE_ACCOUNT | Snowflake account you're connecting to. Should be something along the lines of "{Cantaloupe account}-{Your Company Name}" |
| Snowflake | Yes | SNOWFLAKE_DATABASE | Snowflake database to connect to. Likely begins with "PRD_SEED...". |
| Snowflake | Yes | SNOWFLAKE_WAREHOUSE | Snowflake warehouse to connect to. |
| Prepick | ? | | Not yet implemented |

Quick start:

```python
from clope.spotlight import run_report
df_report = run_report(
 "123",
 [("filter0", "2024-01-01"), ("filter1", "2024-01-31")],
)

from clope.snow import facts
df_sales = facts.get_sales_revenue_by_day_fact(branch=1, location=2)

from clope.prepick import PrepickClient
cli = PrepickClient()
items = cli.load_items()
```

## Spotlight

The spotlight module involves interaction with the Cantaloupe Spotlight API. The API allows you to run a Spotlight report remotely and retrieve the raw Excel data via HTTP requests. Reports must be set up in Seed Office prior to using the API. This is quick and suited for getting data that needs to be up-to-date at that moment.

### Run Spotlight Report (run_report())

The primary function. Used to run a spotlight report, retrieve the excel results, and transform the excel file into a workable pandas dataframe. Cantaloupe's spotlight reports return an excel file with two tabs: Report and Stats. This pulls the info from the Report tab, Stats is ignored.

> Note: Make sure your spotlight report has been shared with the "Seed Spotlight API Users" security group in Seed Office. Won't be accessible otherwise.

Takes in two parameters:

*report_id*

A string ID for the report in Cantaloupe. When logged into Seed Office, the report ID can be found in the URL. E.G. <https://mycantaloupe.com/cs3/ReportsEdit/Run?ReportId=XXXXX>, XXXXX being the report ID needed.

*params*

Optional parameter, list of tuples of strings. Some Spotlight reports have required filters which must be supplied to get data back. Date ranges being a common one. Cantaloupe's error messages are fairly clear, in my experience, with telling you what parameteres are needed to run the report and in what format they should be. First element of tuple is filter name and second is filter value. Filter names are in format of "filter0", "filter1", "filter2", etc.

## Snowflake

Cantaloupe also offers a data warehouse product in Snowflake. Good for aggregating lots of information, as well as pulling historical info. However, notably, data is only pushed from Seed into the Snowflake data warehouse once a day, so it is not necessarily going to be accurate as of that moment.

Also something to keep in mind is that the system makes use of SCD (slowly changing dimension) in order to keep track of historical info vs current info. So some care should be taken when interpreting the data. For each dataset that uses SCD, a parameter has been included to restrict to current data only or include all data.

Authentication to Snowflake is handled via [key-pair authentication](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-connect#using-key-pair-authentication-and-key-pair-rotation). You'll need to create a key pair using openssl and set the snowflake user's RSA_PUBLIC_KEY.

## Prepick

Cantaloupe has a SOAP interface that allows picking software to fulfill, update, and finish prepick orders. Typically the SOAP interface would be used directly by that picking system (e.g. Lightspeed) rather than via python, but may be useful for some specific circumstances. Don't have access to the SOAP interface currently, so module is not yet fully functional.

The expected flow would be something along these lines (from Cantaloupe's documentation):
1. Pull in Master Data/lists

    a. LoadItemCategories

    b. LoadItems

    c. LoadMachineClasses

    d. LoadRoutes

2. Pull in the orders for the next day by route

    a. LoadPrepick (Date, Route)

3. Complete each pick in the warehouse then send back any updates

    a. UpdatePrepick (Schedule, Machine, Coil, Item, Quantity)

4. When each route is complete, notify Seed the schedule can be locked for that route

    a. FinishPrepickUpdate (Schedule)
