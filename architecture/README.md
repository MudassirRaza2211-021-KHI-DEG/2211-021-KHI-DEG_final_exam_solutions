# Architecture task

You are working for a client in the E-Commerce industry who has ~20 online shops, daily visited by around 1 million customers. Your Data Engineering Team is currently working together with a Data Science Team on a recommendation engine.

Your task is to propose an architecture of the solution meeting requirements given by stakeholders.

Your team needs to collect following data:
* Product views (50 000 events/minute)
* Product added to basket (1000 events/minute)
* Searched products (30 000 events/minute)
* Purchased products (800 events/minute)

This data will be collected by already working services and sent to your data pipeline in a way you decide on.

Data Science Team requirements:
* Data needs to be delivered with a maximum delay of 1 hour
* Data needs to be filtered (deleted bots actions etc.)

Product Team requirements:
* Very high availability
* Mitigate the risk of losing any data in case of partial system failure
* Cost optimization


The output of your tasks should be:
* Diagram of the proposed architecture – submitted as an image file.
* Justification of at least 3 technology choices (why this technology? which requirement made you choose it? how it helps satisfy requirements?) – submitted as a pdf file.
