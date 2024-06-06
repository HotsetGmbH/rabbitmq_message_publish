---
checksum: 99a407107870c16fd79d043307b8ac043cf073d789a7e6c554e1689cc8132d52
---

# Overview

The app basically provides 2 functions for sending JSON messages to the Messagebroker and for sending messages to Kibana.

To be able to call the functions, they must be imported:

```Python
from rabbitmq_message_publish.events import log_to_kibana
```

The configuration is done through [RabbitMQ Settings](RabbitMqSettings.md).

## log_to_kibana()

```Python
log_to_kibana(loglevel, message, offset = 0)
```

This function writes a log entry to Kibana logging. Here are the key pieces of information:

| Column          | Meaning                                                         |
|-----------------|-------------------------------------------------------------------|
| `timestamp`     | Time of the message                                              |
| `log_level`     | Severity (`debug`/`info`/`warning`/`error`)                      |
| `message`       | Message text                                                    |
| `code_position` | Position in the source code from which the message was sent      |
| `session_id`    | Unique ID of the session                                         |
| `user`          | Name of the user logged in during the session                    |

The optional parameter `offset` can be used to "shift" the code position that is logged in the call stack.

This can be particularly useful in central functions that are called from various places: In this case, the line from which this function was called is logged rather than the line in the central function.

## doctype_change()

```Python
doctype_change(doc, event)
```

An instance of a Doctype and an event (e.g. `"on_update"`) are passed to this function.

The content of the Doctype is taken as `content` in the message, and the event is taken as `operation`. The overall structure of the message follows the basic [Message Structure](MessageStructure.md).