<?php

$website = $_POST['website'];

$assignmentId = $_POST['assignmentId'];

$trialNo = $_POST['trialCount'];
$queryLetter = $_POST['queryLetter'];
$submittedLetter = $_POST['submittedLetter'];
$startTimeMs = $_POST['startTimeMs'];
$endTimeMs = $_POST['endTimeMs'];

$path = $_SERVER['DOCUMENT_ROOT'] . "/" . $website . "/php/DatabaseConfiguration.php";
require_once $path;

$config = new DatabaseConfiguration();
$conn = $config->createConnection();

// Insert trial entry into trial table
// Protect against injection using prepared statements and parameterized queries
$stmt = mysqli_prepare($conn, "INSERT INTO trial (assignment_id, trial_no, query_letter, submitted_letter, start_time_ms, end_time_ms) VALUES (?, ?, ?, ?, ?, ?)");
mysqli_stmt_bind_param($stmt, 'iissss', $assignmentId, $trialNo, $queryLetter, $submittedLetter, $startTimeMs, $endTimeMs);
$result = mysqli_stmt_execute($stmt);

$new_trial_id = mysqli_insert_id($conn);
mysqli_stmt_close($stmt);

if ($result === TRUE) {
    echo "Recorded new trial entry (trial_id: " . $new_trial_id . ")\n";
} else {
    echo "Error: " . $sql . "\n" . $conn->error . "\n";
}

mysqli_close($conn);
?>
