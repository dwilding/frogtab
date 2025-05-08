<?php

header('Content-Type: application/json');

function respond_with_failure() {
  echo json_encode([
    'success' => false,
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

// Connect to database
if (file_exists($_SERVER['FILE_SQLITEDB'])) {
  $db = new PDO('sqlite:' . $_SERVER['FILE_SQLITEDB']);
}
else {
  respond_with_failure();
}

// Check whether user exists
$select_user = $db->prepare('SELECT user_id FROM users WHERE user_id = :user_id');
$select_user->bindParam(':user_id', $user_id);
$select_user->execute();
$select_user_result = $select_user->fetch(PDO::FETCH_ASSOC);
if (!$select_user_result) {
  respond_with_failure();
}

// Update messages
$insert_message = $db->prepare('INSERT INTO messages (for, message) VALUES (:for, :message)');
$insert_message->bindParam(':for', $user_id);
$insert_message->bindParam(':message', $message);
$insert_message->execute();

// Respond with success
echo json_encode([
  'success' => true,
]);

?>
