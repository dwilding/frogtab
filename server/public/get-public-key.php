<?php

function respond_with_failure() {
  header("HTTP/1.1 500 Internal Server Error");
  header('Content-Type: text/plain');
  echo 'Error';
  exit();
}

// Get user ID from request
if (empty($_GET['user_id'])) {
  respond_with_failure();
}
$user_id = $_GET['user_id'];

// Connect to database
if (file_exists($_SERVER['FILE_SQLITEDB'])) {
  $db = new PDO('sqlite:' . $_SERVER['FILE_SQLITEDB']);
}
else {
  respond_with_failure();
}

// Try to select user
$select_user = $db->prepare('SELECT user_id, pgp_public_key FROM users WHERE user_id = :user_id');
$select_user->bindParam(':user_id', $user_id);
$select_user->execute();
$select_user_result = $select_user->fetch(PDO::FETCH_ASSOC);
if (!$select_user_result) {
  respond_with_failure();
}

// Respond with PGP public key
header('Content-Type: application/pgp-keys');
echo $select_user_result['pgp_public_key'];

?>