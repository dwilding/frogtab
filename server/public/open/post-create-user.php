<?php

require $_SERVER['DIR_PACKAGES'] . '/vendor/autoload.php';
use Ramsey\Uuid\Uuid;
use Devium\Toml\Toml;

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

// Get PGP public key
if (!array_key_exists('pgp_public_key', $request_body)) {
  respond_with_failure();
}
$pgp_public_key = $request_body['pgp_public_key'];
if (!str_starts_with($pgp_public_key, '-----BEGIN PGP PUBLIC KEY BLOCK-----')) {
  respond_with_failure();
}

// Check whether registration is allowed
if (file_exists($_SERVER['FILE_SETTINGS'])) {
  $settings_toml = file_get_contents($_SERVER['FILE_SETTINGS']);
  $settings = Toml::decode($settings_toml, false);
  if (!$settings['allow_registration']) {
    respond_with_failure();
  }
}
else {
  $settings = [
    'allow_registration' => true,
  ];
  $settings_toml = Toml::encode($settings);
  file_put_contents($_SERVER['FILE_SETTINGS'], $settings_toml);
}

// Connect to database
if (file_exists($_SERVER['FILE_SQLITEDB'])) {
  $db = new PDO('sqlite:' . $_SERVER['FILE_SQLITEDB']);
}
else {
  $db = new PDO('sqlite:' . $_SERVER['FILE_SQLITEDB']);
  $db->exec('CREATE TABLE users (
          user_id TEXT PRIMARY KEY,
          api_key TEXT NOT NULL,
          pgp_public_key TEXT NOT NULL
      );'
  );
  $db->exec('CREATE TABLE messages (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          for TEXT NOT NULL,
          message TEXT NOT NULL
      );'
  );
}

// Send comment to me (optional)
if (
  array_key_exists('comment', $request_body)
  && str_starts_with($request_body['comment'], '-----BEGIN PGP MESSAGE-----')
) {
  $my_user_id = '03ae6b6f-1134-4e7b-83ed-deaae4b53af7';
  $select_user = $db->prepare('SELECT user_id FROM users WHERE user_id = :user_id');
  $select_user->bindParam(':user_id', $my_user_id);
  $select_user->execute();
  $select_user_result = $select_user->fetch(PDO::FETCH_ASSOC);
  if (!$select_user_result) {
    respond_with_failure();
  }
  $insert_message = $db->prepare('INSERT INTO messages (for, message) VALUES (:for, :message)');
  $insert_message->bindParam(':for', $my_user_id);
  $insert_message->bindParam(':message', $request_body['comment']);
  $insert_message->execute();
}

// Generate credentials
$user_id = Uuid::uuid4()->toString();
$api_key = Uuid::uuid4()->toString();

// Add new user
$insert_user = $db->prepare('INSERT INTO users (user_id, api_key, pgp_public_key) VALUES (:user_id, :api_key, :pgp_public_key)');
$insert_user->bindParam(':user_id', $user_id);
$insert_user->bindParam(':api_key', $api_key);
$insert_user->bindParam(':pgp_public_key', $pgp_public_key);
$insert_user->execute();

// Respond with credentials
echo json_encode([
  'success' => true,
  'user' => [
    'user_id' => $user_id,
    'api_key' => $api_key,
  ],
]);

?>
