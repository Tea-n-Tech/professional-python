
# API

This lesson is about designing APIs with Python.
To be more exact, we will be focusing on the famous REST APIs.

## Abstract Principles

REST (Representational state transfer) is not a specific way of implementing an
API as largely confused, but it is guiding principles so you don't fuck up.
If you follow the principles you will get the following properties:

- (Horizontal) Scalability
  - Spawning multiple instances increases performance
  - Interaction with offer components is efficient
- Simplicity
  - The interface is concise and understandable
  - Offer only what is needed
- Modifiability
  - The interface (specs) can be extended and changed
  - The API can be extended functionally
- Transparency of communication
  - It is clear and simple to understand who communicates with who
- Portability
  - Moving the application to another machine is easily possible
- Reliability
  - Failure of API instances does not affect the entire system

These properties make limited sense to just the single component but if you add
eventually a database and other systems around their sense becomes stronger.
To get to these REST defines the following architectural constraints:

1. Client–server architecture
   - Separate server internals such as the database from the client
     interface
2. Statelessness
   - No storing data between requests within the API instance
3. Cacheability
   - Allowing traffic to be cached at several levels greatly
     increases system performance  
4. Layered system
   - The system can be put behind other layers such as network
     load balancers or proxies
5. Uniform interface
   - Simple usage and decoupling of different system components
   - Resource identification in requests
     - Different routes target different resources
     - Response formats can be varied (XML, JSON, HTML, ...)
   - Resource manipulation through representations
     - Clients can modify resources with minimal interactions
     - Update attributes (through e.g. a post request)
   - Self-descriptive messages
     - Message headers specify the data type and encoding info
   - Hypermedia
     - Links in the response can direct the client to other
       resources
6. Code on demand (not used here)
   - Load additional code extensions on demand

These formal principles hit rather hard as before once you consider
the API as a piece with other components.
Note if you don't stick to these principles you will loose previous
properties.
For example if you store data between requests within the API instance
you loose scalability since parallel running instances are not
possible as they would have different knowledge about clients.

## Network, Protocol and other Shenanigans

TODO

## Performance

To make it brief, APIs with python are not exactly efficient compared to other
languages such as golang or rust.
Nonetheless they are easy and fast to create, and if built right you can simply
compensate the lack of performance with more instances running in parallel.
In the end you will pay more but for many if not most companies this cost is
not really an issue.
The bigger issue is usually the cost of maintainability of python.
