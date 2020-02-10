# tinyhttp

> Performant static file HTTP server using Nim for speed.

### Features

* High performance
* Extremely lightweight (~1MB once compiled)
* Render Markdown as HTML ([MarkDeep](https://casual-effects.com/markdeep/))

### Description

tinyhttp gets its speed from [Nim](https://nim-lang.org/).
Nim is a powerful language with the speed of C
and the expressiveness of Python. [Fabio Cevasco](https://h3rald.com/) created a
tiny HTTP server in Nim called [nimhttpd](https://github.com/h3rald/nimhttpd).
Make sure to head over to his repository and star it 🙂. Nimporter (a library
that allows you to directly-import Nim files), made the porting process almost
effortless.

### Installation

In order to run tinyhttp, you must install:

* The Nim programming language
* Nimpy (`nimble install nimpy`)
* Nimporter (`pip install nimporter`)

```bash
$ pip install git+https://github.com/Pebaz/tinyhttp
```

## Usage

You can use tinyhttp in 3 different ways:

* As a library, for an ultra-lightweight HTTP server
* As a runnable module
* From the CLI

#### Library

```python
import time
from tinyhttp import HttpServer

server = HttpServer(log=True)
server.start()
time.sleep(10)  # Do other things while serving in background
server.stop()
```

#### Runnable Module

```bash
$ python3 -m tinyhttp --host "0.0.0.0" --port 9090 --dir ../../
```

#### CLI

```bash
$ tinyhttp --host "0.0.0.0" --port 9090 --dir ../../
```
