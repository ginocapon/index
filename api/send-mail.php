<?php
// ═══════════════════════════════════════════════════════════════
// RIGHETTO IMMOBILIARE — Email Relay PHP (cPanel)
// Riceve richieste HTTP e invia email via mail() PHP
// Upload su cPanel: public_html/api/send-mail.php
// ═══════════════════════════════════════════════════════════════

// Chiave segreta per autorizzare le richieste (CAMBIA QUESTA!)
define('API_SECRET', 'RighettoMail2026!SecretKey');

// CORS
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-API-Key');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['status' => 'error', 'error' => 'Solo POST']);
    exit;
}

// Verifica autenticazione
$headers = getallheaders();
$apiKey = $headers['X-API-Key'] ?? $headers['x-api-key'] ?? '';

if ($apiKey !== API_SECRET) {
    http_response_code(403);
    echo json_encode(['status' => 'error', 'error' => 'API key non valida']);
    exit;
}

// Leggi il body JSON
$input = json_decode(file_get_contents('php://input'), true);
if (!$input) {
    echo json_encode(['status' => 'error', 'error' => 'JSON non valido']);
    exit;
}

$action = $input['action'] ?? '';

// ═══ INVIO SINGOLA EMAIL ═══
if ($action === 'send' || $action === 'send_single' || $action === 'send_test') {
    $to = filter_var(trim($input['to_email'] ?? ''), FILTER_VALIDATE_EMAIL);
    $rawSender = trim($input['sender_email'] ?? '');
    $fromEmail = $rawSender ? filter_var($rawSender, FILTER_VALIDATE_EMAIL) : false;
    $fromName = $input['sender_name'] ?? 'Righetto Immobiliare';
    $subject = $input['subject'] ?? '';
    $htmlBody = $input['html_body'] ?? '';
    $toName = $input['to_name'] ?? '';

    if (!$to) {
        echo json_encode(['status' => 'error', 'error' => 'Email destinatario non valida: ' . ($input['to_email'] ?? '(vuoto)')]);
        exit;
    }
    // Fallback mittente se non valido o non fornito
    if (!$fromEmail) {
        $fromEmail = 'info@righettoimmobiliare.it';
    }
    $replyTo = filter_var(trim($input['reply_to'] ?? ''), FILTER_VALIDATE_EMAIL);
    if (!$replyTo) {
        $replyTo = $fromEmail;
    }
    if (!$subject || !$htmlBody) {
        echo json_encode(['status' => 'error', 'error' => 'Oggetto e corpo email obbligatori']);
        exit;
    }

    // Prefisso [TEST] se è un test
    if ($action === 'send_test' && strpos($subject, '[TEST]') === false) {
        $subject = '[TEST] ' . $subject;
    }

    $result = sendEmail($to, $toName, $fromEmail, $fromName, $subject, $htmlBody, $replyTo);

    if ($result === true) {
        echo json_encode(['status' => 'sent', 'to' => $to, 'message' => 'Email inviata a ' . $to]);
    } else {
        echo json_encode(['status' => 'error', 'error' => $result, 'to' => $to]);
    }
    exit;
}

// ═══ INVIO BATCH (multiple email) ═══
if ($action === 'send_batch') {
    $emails = $input['emails'] ?? [];
    $delay = intval($input['delay_ms'] ?? 3000); // 3 sec default tra email
    $rawSenderBatch = trim($input['sender_email'] ?? '');
    $fromEmail = $rawSenderBatch ? filter_var($rawSenderBatch, FILTER_VALIDATE_EMAIL) : false;
    $fromName = $input['sender_name'] ?? 'Righetto Immobiliare';
    if (!$fromEmail) $fromEmail = 'info@righettoimmobiliare.it';
    $replyTo = filter_var(trim($input['reply_to'] ?? ''), FILTER_VALIDATE_EMAIL);
    if (!$replyTo) $replyTo = $fromEmail;

    $sent = 0;
    $errors = 0;
    $results = [];

    // Aumenta timeout per batch grandi
    set_time_limit(600);

    foreach ($emails as $i => $em) {
        $to = filter_var($em['to_email'] ?? '', FILTER_VALIDATE_EMAIL);
        if (!$to) {
            $errors++;
            $results[] = ['email' => $em['to_email'] ?? '?', 'status' => 'error', 'error' => 'Email non valida'];
            continue;
        }

        $subject = $em['subject'] ?? $input['subject'] ?? '';
        $htmlBody = $em['html_body'] ?? $input['html_body'] ?? '';
        $toName = $em['to_name'] ?? '';

        $result = sendEmail($to, $toName, $fromEmail, $fromName, $subject, $htmlBody, $replyTo);

        if ($result === true) {
            $sent++;
            $results[] = ['email' => $to, 'status' => 'sent'];
        } else {
            $errors++;
            $results[] = ['email' => $to, 'status' => 'error', 'error' => $result];
        }

        // Pausa tra email per non sovraccaricare il server
        if ($i < count($emails) - 1 && $delay > 0) {
            usleep($delay * 1000);
        }
    }

    echo json_encode([
        'status' => 'batch_done',
        'sent' => $sent,
        'errors' => $errors,
        'total' => count($emails),
        'results' => $results
    ]);
    exit;
}

// ═══ PING / TEST CONNESSIONE ═══
if ($action === 'ping') {
    echo json_encode([
        'status' => 'ok',
        'message' => 'Email relay attivo',
        'php_version' => PHP_VERSION,
        'mail_function' => function_exists('mail') ? 'disponibile' : 'non disponibile',
        'server' => $_SERVER['SERVER_NAME'] ?? 'unknown',
        'timestamp' => date('Y-m-d H:i:s')
    ]);
    exit;
}

echo json_encode(['status' => 'error', 'error' => 'Azione non riconosciuta: ' . $action]);

// ═══════════════════════════════════════════════════════════════
// FUNZIONE INVIO EMAIL
// ═══════════════════════════════════════════════════════════════
function sendEmail($to, $toName, $fromEmail, $fromName, $subject, $htmlBody, $replyTo) {
    // Boundary per MIME
    $boundary = '----=_Part_' . md5(uniqid(mt_rand(), true));

    // Header From con nome
    $fromHeader = $fromName
        ? '=?UTF-8?B?' . base64_encode($fromName) . '?= <' . $fromEmail . '>'
        : $fromEmail;

    // Headers
    $headers = [];
    $headers[] = 'From: ' . $fromHeader;
    $headers[] = 'Reply-To: ' . ($replyTo ?: $fromEmail);
    $headers[] = 'MIME-Version: 1.0';
    $headers[] = 'Content-Type: multipart/alternative; boundary="' . $boundary . '"';
    $headers[] = 'X-Mailer: RighettoImmobiliare/1.0';
    $headers[] = 'List-Unsubscribe: <mailto:' . $fromEmail . '?subject=CANCELLAMI>';
    $headers[] = 'List-Unsubscribe-Post: List-Unsubscribe=One-Click';

    // Estrai testo plain dall'HTML
    $textBody = strip_tags(str_replace(['<br>', '<br/>', '<br />', '</p>', '</div>', '</li>'], "\n", $htmlBody));
    $textBody = html_entity_decode($textBody, ENT_QUOTES, 'UTF-8');
    $textBody = preg_replace('/\n{3,}/', "\n\n", trim($textBody));

    // Corpo MIME multipart
    $body = '';
    $body .= '--' . $boundary . "\r\n";
    $body .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $body .= "Content-Transfer-Encoding: base64\r\n\r\n";
    $body .= chunk_split(base64_encode($textBody)) . "\r\n";

    $body .= '--' . $boundary . "\r\n";
    $body .= "Content-Type: text/html; charset=UTF-8\r\n";
    $body .= "Content-Transfer-Encoding: base64\r\n\r\n";
    $body .= chunk_split(base64_encode($htmlBody)) . "\r\n";

    $body .= '--' . $boundary . "--\r\n";

    // Destinatario con nome
    $toFormatted = $toName
        ? '=?UTF-8?B?' . base64_encode($toName) . '?= <' . $to . '>'
        : $to;

    // Envelope sender (necessario su cPanel/Exim per autorizzare il From)
    $envelopeSender = '-f ' . $fromEmail;

    // Codifica oggetto in UTF-8
    $encodedSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';

    // Invio con mail() — il 5° parametro imposta il Return-Path / envelope sender
    $success = @mail($toFormatted, $encodedSubject, $body, implode("\r\n", $headers), $envelopeSender);

    if ($success) {
        return true;
    } else {
        $lastError = error_get_last();
        return 'mail() fallita: ' . ($lastError['message'] ?? 'errore sconosciuto') .
               ' | From: ' . $fromEmail . ' | To: ' . $to;
    }
}
