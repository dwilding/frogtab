<?php

$page_state = '';
$icon_16 = '/favicons/icon-16.png';
$icon_32 = '/favicons/icon-32.png';
$query = $_SERVER['QUERY_STRING'];
if ($query == "t0" || $query == "t1" || $query == "i0" || $query == "i1") {
  $page_state = $query;
  if ($query == "t1" || $query == "i1") {
    $icon_16 = '/favicons/icon-16-notify.png';
    $icon_32 = '/favicons/icon-32-notify.png';
  }
}

echo $icon_32;

?>