<?php
declare(strict_types=1);

// Temporäre Diagnosedatei. Nach der Prüfung sofort vom Server löschen.
const PHPINFO_ACCESS_KEY = '382ab51086bd921710383a57fe28010da364eacb47818869';

header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
header('Pragma: no-cache');
header('Expires: 0');
header('X-Robots-Tag: noindex, nofollow, noarchive', true);
header('X-Content-Type-Options: nosniff', true);
header('Content-Security-Policy: default-src \'none\'; style-src \'unsafe-inline\'; img-src data:', true);

$providedKey = isset($_GET['key']) && is_string($_GET['key']) ? $_GET['key'] : '';

if ($providedKey === '' || !hash_equals(PHPINFO_ACCESS_KEY, $providedKey)) {
    http_response_code(404);
    header('Content-Type: text/plain; charset=utf-8');
    echo "Not Found\n";
    exit;
}

// Bewusst ohne INFO_ENVIRONMENT und INFO_VARIABLES, damit keine Cookies,
// Request-Header oder Umgebungsvariablen angezeigt werden.
phpinfo(INFO_GENERAL | INFO_CONFIGURATION | INFO_MODULES);
