<?php

$website = $_POST['website'];

$assignmentId = $_POST['assignmentId'];
$endHit = $_POST['endHit'];
$status = $_POST['status'];

$path = $_SERVER['DOCUMENT_ROOT'] . "/" . $website . "/php/DatabaseConfiguration.php"; // e.g. /var/www/bdroads.com
require_once $path;

$config = new DatabaseConfiguration();
$conn = $config->createConnection();

// Update assignment entry in assignment table
// Protect against injection using prepared statements and parameterized queries
$stmt = mysqli_prepare($conn, "UPDATE assignment SET end_hit=?, status=? WHERE assignment_id=?");
mysqli_stmt_bind_param($stmt, 'ssi', $endHit, $status, $assignmentId);
$result = mysqli_stmt_execute($stmt);

if ($result === TRUE) {
    echo "Assignment entry successfully updated.";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

mysqli_stmt_close($stmt);
mysqli_close($conn);
?>
