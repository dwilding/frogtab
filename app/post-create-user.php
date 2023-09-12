<?php

require $_SERVER['APP_DIR_PACKAGES'] . '/vendor/autoload.php';
use Ramsey\Uuid\Uuid;

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

// Get PGP public key
if (!array_key_exists('pgp_public_key', $request_body)) {
  respond_with_failure();
}
$pgp_public_key = $request_body['pgp_public_key'];
if (!str_starts_with($pgp_public_key, '-----BEGIN PGP PUBLIC KEY BLOCK-----')) {
  respond_with_failure();
}

// Get comment
if (!array_key_exists('comment', $request_body)) {
  respond_with_failure();
}
$comment = $request_body['comment'];
if (!str_starts_with($comment, '-----BEGIN PGP MESSAGE-----')) {
  respond_with_failure();
}

// Generate credentials
$user_id = Uuid::uuid4()->toString();
$api_key = Uuid::uuid4()->toString();

// Connect to database
$db = new PDO('sqlite:' . $_SERVER['APP_DIR_DATA'] . '/sqlite.db');

// Add new user
$insert_user = $db->prepare('INSERT INTO users (user_id, api_key, pgp_public_key, comment) VALUES (:user_id, :api_key, :pgp_public_key, :comment)');
$insert_user->bindParam(':user_id', $user_id);
$insert_user->bindParam(':api_key', $api_key);
$insert_user->bindParam(':pgp_public_key', $pgp_public_key);
$insert_user->bindParam(':comment', $comment);
$insert_user->execute();

// Send comment to me
$my_user_id = '03ae6b6f-1134-4e7b-83ed-deaae4b53af7';
$insert_message = $db->prepare('INSERT INTO messages (for, message) VALUES (:for, :message)');
$insert_message->bindParam(':for', $my_user_id);
$insert_message->bindParam(':message', $comment);
$insert_message->execute();

// Respond with credentials
echo json_encode([
  'success' => true,
  'user' => [
    'user_id' => $user_id,
    'api_key' => $api_key
  ]
]);

?>