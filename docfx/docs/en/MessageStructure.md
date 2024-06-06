---
checksum: 44125e2a77ad485384e6d97b33a9b0566a4868dcdc5b3779e86010a573d1f2e0
---

# Content and Structure of Messages

## Basics

Messages are structured information in JSON format.

A message should be complete. This means it contains all necessary information for processing. This ensures that consistent data is processed and interface processes do not need to read additional data from the source system to process a message, as this data may have already been changed by now.

All information of a record from the source system should be included in a message. Interfaces can decide which information is needed and which can be ignored.

## Header Information

All messages have a similar structure and contain this metadata in their header:

| Field                      | Type           | Description                                                                                                                                                                                                                                         | Example                                              |
|---------------------------|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| **transaction_id**        | GUID          | Unique ID of the message                                                                                                                                                                                                                            | `{D0400FFB-A302-49CF-87DF-8758C165BFF3}`            |
| **system**                | string        | Name of the source system                                                                                                                                                                                                                           | `"penta"`                                           |
| **datapool**              | string        | Which datapool in the source system sent this message?                                                                                                                                                                                              | `de100m(svam1.hotsetgmbh.de)_D`                     |
| **language**              | string        | Which language (of the user interface) does this message use (2-digit ISO code or Windows culture code)                                                                                                                                             | `"de"` or `"en-us"`                               |
| **hostname**              | string        | Name of the computer where the message was created                                                                                                                                                                                                  |                                                     |
| **user**                  | string        | Name of the user in the source system who triggered this message                                                                                                                                                                                    | `"Dirk Festerling"` or `"dfesterling@hotset.com"` |
| **session_id**            | string        | Unique session ID, created anew at every application restart                                                                                                                                                                                        |                                                     |
| **operation**             | string        | What operation triggered this message? <br> - From the user interface: create, update, delete <br> - From the interface process: response                                                                                                           |                                                     |
| **timestamp**             | UTC timestamp | Time at which the message was triggered (in JSON-compatible format: ISO8601 UTC)                                                                                                                                                                   | `2012-04-23T18:25:43.511Z`                          |
| **business_object**       | string        | Class of the business object contained in the message                                                                                                                                                                                               | `PADR`                                              |
| **primary_key**           | string        | Unique ID of the record in the source system                                                                                                                                                                                                         | `K\|59998\|10`                                      |
| **global_id**             | string        | Unique system-wide ID of the record. This ID is created in the system where the record was created and is transferred to all other systems.                                                                                                         | `Penta-100-PADR-K\|599998\|10`                      |
| **correlation_id**        | GUID          | *For response messages only!* Transaction ID of the original message to which this response belongs. This ID makes it possible to determine if a specific message has been processed.                                                              |                                                     |
| **correlation_timestamp** | UTC timestamp | *For response messages only!* Time of the original message to which this response belongs. This timestamp makes it possible to determine if a record in the source system was changed after the original message was sent.                        |                                                     |
| **correlation_operation** | string        | *For response messages only!* Operation of the original message to which this response belongs                                                                                                                                                       |                                                     |
| **correlation_system**    | string        | *For response messages only!* Source system that sent the original message                                                                                                                                                                          |                                                     |
| **log_level**             | string        | *For log messages only!* Severity level of a log message (`debug`/`info`/`warning`/`error`)                                                                                                                                                         |                                                     |
| **message**               | string        | *For log messages only!* Message text                                                                                                                                                                                                               |                                                     |
| **milliseconds**          | number        | *For log messages only!* Number of milliseconds the logged process took (It is the responsibility of the application to perform meaningful time measurement here)                                                                              |                                                     |

## Content Structure

The content is the actual message text. It is sent in the data format of the source system (field names and representation of values). Ideally, it is a simple list of fields and their values. However, there may also be nested information, for example, to reference the content of other objects.

Interfaces must interpret this format and process the message in the target system.

## Additional Structures

For debugging purposes or to support interface processes, additional structures may follow the content of a message.

## Example

```json
{
  "transaction_id": "{D0400FFB-A302-49CF-87DF-8758C165BFF3}",
  "datapool": "de100m(svam1.hotsetgmbh.de)_D",
  "language": "D",
  "user": "Adrian Jüttner",
  "operation": "update",
  "timestamp": "2018-07-27T12:09:10.160Z",
  "business_object": "PADR",
  "primary_key": "K|599998|10",
  "global_id": "Penta-100-PADR-K|599998|10",
  "content": {
    "ABTEILUNG": null,
    "ADRESS_ID": 599998,
    "ADRESS_STATUS": "1",
    ...
    "VS_ABGLEICHSTATUS": 0,
    "WERK": null,
    "ZUORDNUNG": "K"
  }
}
```

>[!NOTE]
>This article was adapted from [Confluence](https://hotset.atlassian.net/wiki/spaces/ITGLOB/pages/249790468/Inhalt+und+Aufbau+der+Nachrichten).