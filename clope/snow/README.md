# Dates

In Snowflake, most date columns are represented by an integer key, rather than the date itself. A couple functions are included with regards to dates. If working directly with Snowflake, you would join the date table onto the fact table you're working with. However, from what I can see the dates are largely deterministic. 1 is 1900-01-01, 2 is 1900-01-02. So I just directly translate from key to date and vice versa with some date math. Much quicker and should give same results as querying the date table itself.

# Dimensions

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

# Facts

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

# Functions

Also included in Cantaloupe's Snowflake are a couple functions. General intention seems to be gathering a subset of data from a couple core fact tables. Haven't yet implemented wrappers for these.
