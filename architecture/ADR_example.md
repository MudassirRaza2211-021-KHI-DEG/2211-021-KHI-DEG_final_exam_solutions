Title: Choosing a Persistence Layer for the Customer Service System

Context:

We are building a new customer service system that will allow our customers to view their account information and submit support requests online. We need to choose a persistence layer for storing and retrieving customer data.

Decision:

A relational database management system (RDBMS) will be used as the persistence layer for the customer service system.

Reasoning:

Several options were considered for the persistence layer, including a NoSQL database, file storage, and in-memory storage. After evaluating the pros and cons of each option, RDBMS was determined as the best fit for the needs because it:
- Provides strong consistency and transactional support
- Offers robust query capabilities
- The data comes highly structured, well fitting the tabular form of RDBMS.
- Has a proven track record of scalability and reliability in enterprise applications

Consequences:

- Need to choose an RDBMS and set up the necessary infrastructure to host it.
- Need to design the database schema and implement the data access layer of the customer service system.
- Additional costs for licenses and maintenance of the RDBMS may be incurred. 

Follow-up:

- Research and compare different RDBMS options to determine the best fit for our needs.
- Set up the RDBMS and necessary infrastructure.
- Design the database schema and implement the data access layer.