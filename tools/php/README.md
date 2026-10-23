# PHP-Konfiguration sicher prüfen

`phpinfo-check.php` ist eine temporäre, mit einem Zugriffsschlüssel geschützte Diagnosedatei. Sie zeigt PHP-Version, SAPI, aktive Konfigurationswerte und geladene Module an.

## Installation

1. `phpinfo-check.php` in das Webverzeichnis von LakeDiver hochladen.
2. Die Datei ausschließlich über HTTPS aufrufen:

   ```text
   https://lakediver.ch/phpinfo-check.php?key=382ab51086bd921710383a57fe28010da364eacb47818869
   ```

3. Nach der Prüfung `phpinfo-check.php` sofort wieder vom Server löschen.

Ohne den korrekten Schlüssel antwortet das Skript mit HTTP 404. Suchmaschinen werden über `X-Robots-Tag` ausgeschlossen und die Antwort darf nicht zwischengespeichert werden.

## Zu prüfende Werte

| Einstellung | Erwarteter Wert |
|---|---|
| PHP Version | 8.5.12 oder neuer |
| Server API | FPM/FastCGI |
| `display_errors` | Off |
| `log_errors` | On |
| `expose_php` | Off |
| `allow_url_include` | Off |
| `session.use_only_cookies` | On |
| `session.use_strict_mode` | On |
| `session.cookie_secure` | On |
| `session.cookie_httponly` | On |

Bei PHP-Konfigurationswerten zeigt `phpinfo()` häufig einen lokalen und einen globalen Wert. Für die Domain ist der lokale Wert maßgeblich, sofern die Einstellung dort überschrieben werden darf.

## Datenschutz und Sicherheit

Das Skript verwendet bewusst nicht `INFO_ALL`. Die Bereiche `INFO_ENVIRONMENT` und `INFO_VARIABLES` werden ausgeschlossen, damit Umgebungsvariablen, Cookies und Request-Header nicht angezeigt werden.

Trotz Zugriffsschutz bleiben folgende Risiken:

- Der Schlüssel erscheint in Browser-Verlauf und Server-Access-Log.
- Die Ausgabe enthält detaillierte Informationen über PHP, Module, Dateipfade und Serverkonfiguration.
- Die Datei darf nicht dauerhaft auf einem öffentlich erreichbaren Server liegen.

## Ergebnis kompakt abfragen

Für die Sicherheitsprüfung werden mindestens diese Angaben benötigt:

```text
PHP Version: 8.5.x
Server API: FPM/FastCGI
display_errors: Off
expose_php: Off
```

Nach Übernahme der Werte die Browserseite schließen und die Diagnosedatei vom Server entfernen.
