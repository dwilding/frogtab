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

// Update config
$users = json_decode(file_get_contents($_SERVER['APP_DIR_CONFIG'] . '/users.json'), true);
$users[$user_id] = [
  'comment' => $comment,
  'api_key' => $api_key,
  'pgp_public_key' => $pgp_public_key
];
file_put_contents($_SERVER['APP_DIR_CONFIG'] . '/users.json', json_encode($users));

// Send comment to me
$my_user_id = '03ae6b6f-1134-4e7b-83ed-deaae4b53af7';
$db = new PDO('sqlite:' . $_SERVER['APP_DIR_DATA'] . '/sqlite.db');
$sql_insert = $db->prepare('INSERT INTO messages (for, message) VALUES (:for, :message)');
$sql_insert->bindParam(':for', $my_user_id);
$sql_insert->bindParam(':message', $comment);
$sql_insert->execute();

// Respond with credentials
echo json_encode([
  'success' => true,
  'user' => [
    'user_id' => $user_id,
    'api_key' => $api_key
  ]
]);

?>