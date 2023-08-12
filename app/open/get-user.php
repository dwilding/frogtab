<?php

header('Content-Type: application/json');

function respond_with_failure() {
  echo json_encode([
    'success' => false
  ]);
  exit();
}

// Get user ID from request
if (empty($_GET['user_id'])) {
  respond_with_failure();
}
$user_id = $_GET['user_id'];

// Load config
$users = json_decode(file_get_contents($_SERVER['APP_DIR_CONFIG'] . '/users.json'), true);

// Verify user ID
if (!array_key_exists($user_id, $users)) {
  respond_with_failure();
}

// Respond with user
echo json_encode([
  'success' => true,
  'user' => [
    'user_id' => $user_id,
    'pgp_public_key' => $users[$user_id]['pgp_public_key']
  ]
]);

?>