# Überblick

Die App stellt grundsätzlich 2 Funktionen bereit, die zum Versenden von JSON-Nachrichten an den Messagebroker und zum Senden von Meldungen an Kibana verwendet werden.

Um die Funktionen aufrufen zu können, müssen sie importiert werden:

```Python
from rabbitmq_message_publish.events import log_to_kibana
```

Die Konfiguration erfolgt über [RabbitMQ Settings](RabbitMqSettings.md).

## log_to_kibana()

```Python
log_to_kibana(loglevel, message, offset = 0)
```

Mit dieser Funktion wird ein Logeintrag in das Kibana-Logging geschrieben. Hier die wichtigsten Informationen:

| Spalte          | Bedeutung                                                         |
|-----------------|-------------------------------------------------------------------|
| `timestamp`     | Zeitpunkt der Meldung                                             |
| `log_level`     | Schweregrad (`debug`/`info`/`warning`/`error`)                    |
| `message`       | Meldungstext                                                      |
| `code_position` | Stelle im Quellcode, von der aus die Meldung gesendet worden ist. |
| `session_id`    | Eindeutige ID der Sitzung                                         |
| `user`          | Name des in der Sitzung angemeldeten Anwenders                    |

Der optionale Parameter `offset` kann dazu verwendet werden, um die Code-Position die Protokolliert wird im Call Stack zu "verschieben".

Das kann vor allem in zentralen Funktionen sinnvoll sein, die von unterschiedlichsten Stellen aus aufgerufen werden: So wird dann nicht die Code-Zeile in der zentralen Funktion protokolliert, sondern die Zeile, von der aus dieses Funktion aufgerufen wurde.

## doctype_change()

```Python
doctype_change(doc, event)
```

An diese Funktion wird eine Ausprägung eines Doctypes übergeben und ein Ergeignis (z.B. `"on_update"`).

Der Inhalt des Doctypes wird als `content` in die Nachricht übernommen und das Ereignis als `operation`. Insgesamt folgt der Aufbau der Nachricht dem grunsätzlichen [Aufbau der Nachrichten](MessageStructure.md).
