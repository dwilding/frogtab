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

// Load config
$users = json_decode(file_get_contents($_SERVER['APP_DIR_CONFIG'] . '/users.json'), true);

// Verify user ID
if (!array_key_exists($user_id, $users)) {
  respond_with_failure();
}

// Verify API key
if ($users[$user_id]['api_key'] != $api_key) {
  respond_with_failure();
}

// Remove messages
$messages = [];
$db = new PDO('sqlite:' . $_SERVER['APP_DIR_DATA'] . '/sqlite.db');
$sql_select = $db->prepare('SELECT * FROM messages WHERE for = :for ORDER BY id ASC');
$sql_select->bindParam(':for', $user_id);
$sql_select->execute();
$results = $sql_select->fetchAll(PDO::FETCH_ASSOC);
foreach ($results as $result) {
  $id = $result['id'];
  $message = $result['message'];
  array_push($messages, $message);
  $sql_delete = $db->prepare('DELETE FROM messages WHERE id = :id');
  $sql_delete->bindParam(':id', $id, PDO::PARAM_INT);
  $sql_delete->execute();
}

// Respond with messages
echo json_encode([
  'success' => true,
  'messages' => $messages
]);

?>