<?php

header('Content-Type: application/json');

function respond_with_failure() {
  echo json_encode([
    'success' => false
  ]);
  exit();
}

// Get request body
$request_body_json = file_get_contents('php://input');
if ($request_body_json === false) {
  respond_with_failure();
}
$request_body = json_decode($request_body_json, true);
if ($request_body === null) {
  respond_with_failure();
}

// Get user ID
if (!array_key_exists('user_id', $request_body)) {
  respond_with_failure();
}
$user_id = $request_body['user_id'];

// Get message
if (!array_key_exists('message', $request_body)) {
  respond_with_failure();
}
$message = $request_body['message'];
if (!str_starts_with($message, '-----BEGIN PGP MESSAGE-----')) {
  respond_with_failure();
}

// Load config
$users = json_decode(file_get_contents($_SERVER['APP_DIR_CONFIG'] . '/users.json'), true);

// Verify user ID
if (!array_key_exists($user_id, $users)) {
  respond_with_failure();
}

// Update messages
$db = new PDO('sqlite:' . $_SERVER['APP_DIR_DATA'] . '/sqlite.db');
$sql_insert = $db->prepare('INSERT INTO messages (for, message) VALUES (:for, :message)');
$sql_insert->bindParam(':for', $user_id);
$sql_insert->bindParam(':message', $message);
$sql_insert->execute();

// Respond with success
echo json_encode([
  'success' => true
]);

?>