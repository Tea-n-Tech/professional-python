
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

Networking has a lot of layers but we won't go into that here as it is a book
on its own.
All you need to know for the moment is, that almost the entire communication
you will deal with is based on TCP/IP (or in rare cases UDP).
On top of that usually starts the fun with different protocols.

### HTTP

If you don't deal with fileservers (FTP) or emails (IMAP) you will most likely
end up with HTTP as workhorse or rather its bigger extension HTTPS.

Just as general info for sparing some pain, HTTP has three major versions.
The first one is super simple but limited in performance.
The second one relies on multiplexing to speed things up, but as you guess it
also got more complicated.
While HTTP/1 and HTTP/2 rely on TCP underneath, HTTP/3 relies on QUIC, just that
you heard the names.
As you guessed, HTTP/3 provides drastic performance improvements thanks to QUIC
and other changes.
In message headers, the clients usually define the standard they use and offer.
So in case your performance is f...bad you might want to check which HTTP
version is used and served.

HTTP provdes different methods to interact with resources:

- GET
  - As you guessed this method gets a resource, website or file
- POST
  - Submits a resource entity to change to the server
- PATCH
  - Submits a partial modification of a resource entity
  - Rather rare encountered as POST is mostly offered already
- PUT
  - Uploads an entirely new resource entity and possibly replaces an existing
    entity
- DELETE
  - Obiously delete a resource enitity
- HEAD
  - Do a get request but just ask for the header
  - Helpful to get information about the payload such as how big it is to check
    for storage

There are more but for simplicity, these are all you will need for a long time.
So anytime you want to interact with a resource you do this through these
methods.
For example a GET on `../users` gives you a list of all users but a DELETE
will remove a specified user (if permissions match).

Another thing actually important to know are HTTP codes.
Pleae don't learn them like at school, but be aware of the ranges.
A few will stick after a while ... trust me.

- 1XX Information (very rarely encountered)
- 2XX Success
- 3XX Redirection
- 4XX Client errors
- 5XX Server errors

You will be mostly dealing with responses in the 2XX, 4XX and maybe sometimes
5XX range.
Some of the most important codes are:

- 2XX
  - 200 Ok (with payload)
  - 201 Created
  - 204 Ok (no payload)
- 3XX
  - 301 Stuff Moved
  - 304 Not Modified (caching fun ...)
  - 307/308 Redirection
- 4XX
  - 400 Bad Request (client sent a malformed request)
  - 401 Unauthorized (this fellow will haunt you)
  - 403 Forbidden (another friend you will see often)
  - 418 I'm a teapot
  - ... a lot more but you will meet them eventually
- 5XX
  - 500 Internal Server Error (Something is broken)
  - 502 Bad Gateway (Networking is screwed)
  - 503 Service Unavailable (Another bad day fellow)

### HTTPS

Nowadays no one does HTTP really anymore.
The reason is that HTTP is entirely unencrypted so everyone between you and the
receiver in the internet can read and manipulate the message.
Yeah it is really bad.
This goes so far that even traffic within a companies microservice architecture
is entirely encrypted.

#### What is it briefly put?

HTTPS is the safe version of HTTP by using TLS (or SSL) to encrypt requests.
Why will you hate HTTPS as a developer?
Certificates are a blessing for security but a big pain for development.
Many companies have expiring certificates after 1 or 2 years and often there
is not yet an automated way to exchange these.
I saw many companies where services went down from time to time just because
no one payed attention to the certificates.
Another pain point is handing certificates around such as including them in
docker images etc.
Not that it all is hard but "just" adding certificates often complicates things
by a lot.
Nonetheless don't even think about going HTTP.
Just accept it and do the job.

#### How does it work in short?

Certificates in its largest form have three participants.
A certificate authority (CA), public key certificate (CRT) and private key
(PEM).
The authority is a certificate widely distributed.
For example your browser has CA from a lot of companies such as google.
A customer of a CA can ask to give them a CRT and PEM ... often against money.
Therefore they send them once a Certificate Signing Request (CSR).
These companies then create a CRT for you but you can also use
[Let's Encrypt][lets-encrypt] which does it for free and there are tools to
renew certificates automatically.
Once you have a CRT and PEM you can install it in your service.
Note the PEM must stay with you!
If someone visits your website or API, they retrieve your CRT and can verify
cryptographically if a CA such as google created the certificate.
By this they know if you are truly legit or just a fake.
I won't go into detail here but your communication will be encrypted from then
on.
A little note, you can also create just a CRT and PEM and forego a CA which is
sometimes a use-case for use-cases with limited scope where a CA is not present.

[lets-encrypt]: https://letsencrypt.org/

## More Protocols ... JSON, HTML and others

On top of HTTPS usually starts the action.
You could send plain text now but we want to exchange data and data always has
a format and that is most definitely not excel or something related.
Responses most commonly return:

- Text-based:
  - HTML/JS/CSS (websites)
  - JSON
  - XML
  - Base64 (bytes encoded as strings)
- Media
  - Images (jpeg, ...)
  - Videos (mp4, webm, ...)
- Binary
  - Plain files (blob)
  - Protobuf
  - Cap'n Proto
  - Flatbuffers
  - ...

Most APIs you will encounter usually work with JSON although XML is presumably
more common thanks to e.g. banking.
Base64 is nothing else but bytes encoded as a string.
Emails often do this to encode appended content.
Note text-based formats are extremely inefficient to put it friendly.
It is dangerous to say this generally, but you can expect lower performance
and higher memory usage compared to binary protocols.
Why is this important?
Because especially ingress and egress (traffic) is very, very expensive.
You will recognize it on your AWS bill quickly.
Protobuf from Google is maybe the most famous binary protocol out there.
It is not the most efficient but has a very good sweetspot, a large support in
languages, many tools surrounding it and is well-established.
There are still faster alternatives such as flatbuffers but they are less
popular and suffer from related problems so don't go into those rabbit holes
if you don't need it.

## Frameworks

Let's get finally to business.
As expected, there are a lot of frameworks.
The most famous ones are probably [FastAPI] and [Flask].
Having used both, I can generally recommend FastAPI.
You will have a great experience with it.
It is quite fast for a Python API and the comfort of using it is very very good.
So lets install it:

```bash
poetry add fastapi uvicorn[standard]
```

Note that we build the API with FastAPI but it will be served by [uvicorn].
Before we can interact with our data we need some first.
Data is never held inside the API (stateless!) but within a database.
Nonetheless this is a tutorial so lets fake a real database.
To do this we create a file `deathstar/database.py`:

```python
from abc import ABC
from typing import Dict, Union
from pydantic import BaseModel


class Planet(BaseModel):
    """Class with information about the planet"""

    name: str


class PlanetDatabase(ABC):
    """This class represents a generic planet database interface"""

    async def get_planet(self, name: str) -> Union[Planet, None]:
        """Get a planet from the database

        Args:
            name: Name of the planet to retrieve
        """
        raise NotImplementedError()

    async def remove_planet(self, name: str) -> bool:
        """Removes a planet from the database

        Args:
            name: Name of the planet to remove
        """
        raise NotImplementedError()


class FakePlanetDatabase(PlanetDatabase):
    planets: Dict[str, Planet]

    def __init__(self):
        # Create fake data
        self.planets = {
            "alderaan": Planet(name="Alderaan"),
            "tatooine": Planet(name="Tatooine"),
            "naboo": Planet(name="Naboo"),
            "tython": Planet(name="Tython"),
            "dantooine": Planet(name="Dantooine"),
            "yavin4": Planet(name="Yavin4"),
        }

    async def get_planet(self, name: str) -> Union[Planet, None]:
        return self.planets.get(name.lower())

    async def remove_planet(self, name: str) -> bool:
        name = name.lower()
        if name in self.planets:
            self.planets.pop(name)
            return True

        return False
```

Be aware of a few explicit things:

- We define a generic interface description with `abc.ABC` to make sure
  we abstract away the concrete implementation underneath.
  With this we could easily add a real database interface underneath.
- We use `pydantic.BaseModel` to define the `Planet` class.
  `pydantic` comes along with `fastapi` and helps to serialize or deserialize
  the class instances so we can simply return them in the API as you will see
  later.
- Recognize how we return a `bool` if a planet was removed in case of
  success or how we return `None` if a planet did not exist.
  This is important since you will see later a resource is not found, which
  is a planet here, we will notify the user with a HTTP 404 (Not Found).

Now it is API time baby, lets create a file `deathstar/api.py` with the
following content:

```python
from fastapi import FastAPI, HTTPException, status

from .database import FakePlanetDatabase, Planet


app = FastAPI()
db = FakePlanetDatabase()


@app.delete("/api/v1/planets/{target}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy_planet(target: str):
    """Shoot a laser at a planet

    Args:
        target: Planet name to destroy
    """
    success = await db.remove_planet(target)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Planet {target} does not exist",
        )


@app.get("/api/v1/planets/{name}", response_model=Planet)
async def get_planet(name: str) -> Planet:
    """Get info about a planet

    Args:
        name: Name of the planet
    """
    planet = await db.get_planet(name)
    if planet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Planet {name} does not exist",
        )

    return planet
```

Again here are a few important things to realize:

- The basic route is `api/v1` which allows us to revamp our api entirely
  under a new version without breaking other peoples systems who interfaced
  us.
- We use `DELETE` method for destroying a planet.
  If the planet is not found we return a classic 404 and in case of success
  it is a 204 (No Content) since we don't have anything to say.
- The route resource type is the planet name.
  Imagine for destroying a planet we could also make a `POST` method on
  for example `/api/v1/planets/{target}/destroy` but this feels a lot less
  natural than the current solution.
- When retrieving a planet we define `response_model=Planet` which allows us to
  simply perform `return planet` without having to convert the class manually
  into a proper response type such as JSON.
  Really Sweet.
- All functions so far were defined `async` which roughly put allows things to
  run more efficiently in parallel (I most definitely won't go into this but
  parallelization and Python including the GIL are a huge topic on its own).
  Different threads could basically then handle multiple requests in parallel
  (I feel very bad having to put it like that cause in Detail things don't go
  exactly like that).

[fastapi]: https://fastapi.tiangolo.com/
[flask]: https://flask.palletsprojects.com/
[uvicorn]: https://www.uvicorn.org/

## Performance

To make it brief, APIs with python are not exactly efficient compared to other
languages such as golang or rust.
Nonetheless they are easy and fast to create, and if built right you can simply
compensate the lack of performance with more instances running in parallel.
In the end you will pay more but for many if not most companies this cost is
not really an issue.
The bigger issue is usually the cost of maintainability of python.
