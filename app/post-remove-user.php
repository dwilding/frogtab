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

// Get API key
if (!array_key_exists('api_key', $request_body)) {
  respond_with_failure();
}
$api_key = $request_body['api_key'];

// Connect to database
$db = new PDO('sqlite:' . $_SERVER['APP_DIR_DATA'] . '/sqlite.db');

// Try to remove user
$delete_user = $db->prepare('DELETE FROM users WHERE user_id = :user_id AND api_key = :api_key');
$delete_user->bindParam(':user_id', $user_id);
$delete_user->bindParam(':api_key', $api_key);
$delete_user->execute();
if ($delete_user->rowCount() == 0) {
  respond_with_failure();
}

// Respond with success
echo json_encode([
  'success' => true
]);

?>