<?php

$website = $_POST['website'];
    
$mTurkAssignmentId = $_POST['mTurkAssignmentId'];
$mTurkWorkerId = $_POST['mTurkWorkerId'];
$mTurkHitId = $_POST['mTurkHitId'];
    
$ipaddress = $_SERVER['REMOTE_ADDR'];
$browserName = $_POST['browser'];
$userPlatform = $_POST['platform'];
$browserLanguage = $_POST['language'];

$codeVersion = $_POST['codeVersion'];
$beginHit = $_POST['beginHit'];
$status = $_POST['status'];

$path = $_SERVER['DOCUMENT_ROOT'] . "/" . $website . "/php/DatabaseConfiguration.php"; // e.g. /var/www/bdroads.com
require_once $path;

$config = new DatabaseConfiguration();
$conn = $config->createConnection();

// Insert assignment entry into assignment table
// Protect against injection using prepared statements and parameterized queries
$stmt = mysqli_prepare($conn, "INSERT INTO assignment (mturk_assignment_id, mturk_worker_id, mturk_hit_id, ipaddress, browser, platform, language, code_version, begin_hit, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
mysqli_stmt_bind_param($stmt, 'ssssssssss', $mTurkAssignmentId, $mTurkWorkerId, $mTurkHitId, $ipaddress, $browserName, $userPlatform, $browserLanguage, $codeVersion, $beginHit, $status);
$result = mysqli_stmt_execute($stmt);

$new_assignment_id = mysqli_insert_id($conn);

//if ($result === TRUE) {
//    echo "New assignment entry successfully created.";
//} else {
//    echo "Error: " . $sql . "<br>" . $conn->error;
//}

echo $new_assignment_id;

mysqli_stmt_close($stmt);
mysqli_close($conn);
?>