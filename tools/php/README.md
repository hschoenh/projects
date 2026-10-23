# Secure PHP Configuration Check

`phpinfo-check.php` is a temporary diagnostic file protected by an access key. It displays the PHP version, SAPI, active configuration values, and loaded modules.

## Installation

1. Upload `phpinfo-check.php` to the web root of your domain.
2. Open the file over HTTPS only:

   ```text
   https://<yourdomain.com>/phpinfo-check.php?key=382ab51086bd921710383a57fe28010da364eacb47818869
   ```

3. Delete `phpinfo-check.php` from the server immediately after completing the check.

Without the correct access key, the script returns HTTP 404. The `X-Robots-Tag` header prevents search engine indexing, and cache headers prevent the response from being stored by the browser or an intermediary cache.

## Values to verify

| Setting | Expected value |
|---|---|
| PHP Version | 8.5.12 or newer |
| Server API | FPM/FastCGI |
| `display_errors` | Off |
| `log_errors` | On |
| `expose_php` | Off |
| `allow_url_include` | Off |
| `session.use_only_cookies` | On |
| `session.use_strict_mode` | On |
| `session.cookie_secure` | On |
| `session.cookie_httponly` | On |

`phpinfo()` often displays both a local value and a master value. The local value applies to the domain when the setting can be overridden at domain or directory level.

## Privacy and security

The script deliberately does not use `INFO_ALL`. It excludes `INFO_ENVIRONMENT` and `INFO_VARIABLES` so that environment variables, cookies, and request headers are not displayed.

The following risks remain despite the access key:

- The key appears in the browser history and the web server access log.
- The output contains detailed information about PHP, loaded modules, file paths, and server configuration.
- The file must not remain permanently on a publicly accessible server.

## Minimum result to record

Record at least the following values:

```text
PHP Version: 8.5.x
Server API: FPM/FastCGI
display_errors: Off
expose_php: Off
```

After recording the values, close the browser tab and remove the diagnostic file from the server.
