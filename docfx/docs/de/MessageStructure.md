# Inhalt und Aufbau der Nachrichten

## Grundlagen

Nachrichten sind strukturierte Informationen im JSON-Format.

Eine Nachricht soll vollständig sein. Das bedeutet, sie enthält alle notwendigen Informationen für die Verarbeitung. Dies stellt sicher, dass konsistente Daten verarbeitet werden und Schnittstellenprozesse keine zusätzlichen Daten aus dem Quellsystem lesen müssen, um eine Nachricht zu verarbeiten, da diese Daten inzwischen möglicherweise bereits geändert wurden.

Alle Informationen eines Datensatzes aus dem Quellsystem sollen in einer Nachricht enthalten sein. Die Schnittstellen können entscheiden, welche Informationen benötigt werden und welche ignoriert werden können.

## Kopfzeileninformationen

Alle Nachrichten haben eine ähnliche Struktur und enthalten diese Metadaten in ihrer Kopfzeile:

| Feld                      | Typ           | Beschreibung                                                                                                                                                                                                                                                   | Beispiel                                            |
|---------------------------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| **transaction_id**        | GUID          | Eindeutige ID der Nachricht                                                                                                                                                                                                                                    | `{D0400FFB-A302-49CF-87DF-8758C165BFF3}`            |
| **system**                | string        | Name des Quellsystems                                                                                                                                                                                                                                          | `"penta"`                                           |
| **datapool**              | string        | Welcher Datenpool im Quellsystem hat diese Nachricht gesendet?                                                                                                                                                                                                 | `de100m(svam1.hotsetgmbh.de)_D`                     |
| **language**              | string        | Welche Sprache (der Benutzeroberfläche) hat diese Nachricht (2-stelliger ISO-Code oder Windows-Kulturcode)                                                                                                                                                     | `"de"` oder `"en-us"`                               |
| **hostname**              | string        | Name des Computers, auf dem die Nachricht erstellt wurde.                                                                                                                                                                                                      |                                                     |
| **user**                  | string        | Name des Benutzers im Quellsystem, der diese Nachricht ausgelöst hat.                                                                                                                                                                                          | `"Dirk Festerling"` oder `"dfesterling@hotset.com"` |
| **session_id**            | string        | Eindeutige Sitzungs-ID, wird bei jedem Neustart der Anwendung neu erstellt.                                                                                                                                                                                    |                                                     |
| **operation**             | string        | Welche Operation hat diese Nachricht ausgelöst? <br> - Von der Benutzeroberfläche: erstellen, aktualisieren, löschen <br> - Vom Schnittstellenprozess: Antwort                                                                                                 |                                                     |
| **timestamp**             | UTC timestamp | Zeitpunkt, zu dem die Nachricht ausgelöst wurde (im JSON-kompatiblen Format: ISO8601 UTC).                                                                                                                                                                     | `2012-04-23T18:25:43.511Z`                          |
| **business_object**       | string        | Klasse des Geschäftsobjekts (Entität), die in der Nachricht enthalten ist.                                                                                                                                                                                     | `PADR`                                              |
| **primary_key**           | string        | Eindeutige ID des Datensatzes im Quellsystem.                                                                                                                                                                                                                  | `K\|59998\|10`                                      |
| **global_id**             | string        | Eindeutige systemweite ID des Datensatzes. Diese ID wird im System erstellt, in dem der Datensatz erstellt wurde. Sie wird an alle anderen Systeme übertragen.                                                                                                 | `Penta-100-PADR-K\|599998\|10`                      |
| **correlation_id**        | GUID          | *Nur für Antwortnachrichten (Antwort)!* Transaktions-ID der ursprünglichen Nachricht, zu der diese Antwort gehört. Mit dieser ID ist es möglich, festzustellen, ob eine bestimmte Nachricht verarbeitet wurde.                                                 |                                                     |
| **correlation_timestamp** | UTC timestamp | *Nur für Antwortnachrichten (Antwort)!* Zeitpunkt der ursprünglichen Nachricht, zu der diese Antwort gehört. Mit diesem Zeitstempel ist es möglich festzustellen, ob ein Datensatz im Quellsystem nach dem Senden der ursprünglichen Nachricht geändert wurde. |                                                     |
| **correlation_operation** | string        | *Nur für Antwortnachrichten (Antwort)!* Operation der ursprünglichen Nachricht, zu der diese Antwort gehört.                                                                                                                                                   |                                                     |
| **correlation_system**    | string        | *Nur für Antwortnachrichten (Antwort)!* Quellsystem (System), das die ursprüngliche Nachricht gesendet hat.                                                                                                                                                    |                                                     |
| **log_level**             | string        | *Nur für Protokollnachrichten!* Schweregrad einer Protokollnachricht (`debug`/`info`/`warning`/`error`)                                                                                                                                                        |                                                     |
| **message**               | string        | *Nur für Protokollnachrichten!* Nachrichtentext                                                                                                                                                                                                                |                                                     |
| **milliseconds**          | number        | *Nur für Protokollnachrichten!* Anzahl der Millisekunden, die der protokollierte Prozess gedauert hat (Es liegt in der Verantwortung der Anwendung, hier eine sinnvolle Zeitmessung durchzuführen).                                                            |                                                     |

## Inhaltsstruktur

Der Inhalt ist der eigentliche Nachrichtentext. Er wird im Datenformat des Quellsystems gesendet (Feldnamen und Darstellung der Werte). Im Idealfall ist es eine einfache Liste von Feldern und ihren Werten. Es kann jedoch auch verschachtelte Informationen geben, z. B. um den Inhalt anderer Objekte zu referenzieren.

Die Schnittstellen müssen dieses Format interpretieren und die Nachricht im Zielsystem verarbeiten.

## Zusätzliche Strukturen

Zu Debugging-Zwecken oder zur Unterstützung von Schnittstellenprozessen können zusätzliche Strukturen dem Inhalt einer Nachricht folgen.

## Beispiel

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
>Der Artikel wurde aus [Confluence](https://hotset.atlassian.net/wiki/spaces/ITGLOB/pages/249790468/Inhalt+und+Aufbau+der+Nachrichten) übernommen.
