# Rules of Rest

Let is it be known:

1) ALL data within DotzCRM + PM Software being created, updated or deleted will be passed to the system through the RestAPIs.

Therefore, if some end-point is missing in the RESTAPI, you have to create it. There will be no manual CUD operations anywhere in the system.

2) Point #1 naturally leads to: All views outside of the RestApi app can only carry out read operations on the database.

This single-point-of entry will greatly ease data-integrity and security concerns.