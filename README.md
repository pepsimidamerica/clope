# Overview

clope (see-lope) is a Python package for interacting with the Cantaloupe/Seed vending system. Primarily being a wrapper for their Spotlight API. It uses the pandas library to return information from a given spotlight report as a dataframe object. It also has functionality for connecting to the snowflake data warehouse Cantaloupe product as well.

## Installation

Haven't yet bothered to publish as a python package, intent is to simply add clope as a git submodule in any projects where it's needed.

## Usage

Several environment variables are required for clope to function.

| Required? | Env Variable | Description |
| --------- | ------------ | ----------- |
| Yes       | CLO_USERNAME | Username of the Spotlight API user. Should be provided by Cantaloupe. |
| Yes       | CLO_PASSWORD | Password of the Spotlight API user. Should be provided by Cantaloupe. |
| No        | CLO_BASE_URL | Not actually sure if this varies between clients. I have this as an optional variable in case it does. Default value if no env variable is <https://api.mycantaloupe.com>, otherwise can be overridden. |
| No        | CLO_ARCHIVE_FILES | Optional variable. Will archive the interim excel files that run_report() generates so can be later looked at in the Archive folder. Default behavior is to not archive and simply delete the excel files after data is pulled from them. |

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

### List Tables

Lists the tables in the Snowflake database that can be pulled from.
