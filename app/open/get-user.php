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

// Connect to database
$db = new PDO('sqlite:' . $_SERVER['APP_DIR_DATA'] . '/sqlite.db');

// Try to select user
$select_user = $db->prepare('SELECT user_id, pgp_public_key FROM users WHERE user_id = :user_id');
$select_user->bindParam(':user_id', $user_id);
$select_user->execute();
$select_user_result = $select_user->fetch(PDO::FETCH_ASSOC);
if (!$select_user_result) {
  respond_with_failure();
}

// Respond with user
echo json_encode([
  'success' => true,
  'user' => [
    'user_id' => $user_id,
    'pgp_public_key' => $select_user_result['pgp_public_key']
  ]
]);

?>