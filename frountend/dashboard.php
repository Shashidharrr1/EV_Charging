<?php
require_once '../config.php';
session_start();

if (!isset($_SESSION['user_id'])) {
    header("Location: login.php");
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Dashboard - EV Recharge Bunk</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <header>
        <nav>
            <div class="logo">EV Recharge Bunk</div>
            <ul class="nav-links">
                <li><a href="find-stations.php">Find Stations</a></li>
                <li><a href="my-bookings.php">My Bookings</a></li>
                <li><a href="profile.php">Profile</a></li>
                <li><a href="logout.php">Logout</a></li>
            </ul>
        </nav>
    </header>

    <main class="dashboard">
        <h2>Welcome, <?php echo htmlspecialchars($_SESSION['username']); ?>!</h2>
        <div class="dashboard-stats">
            <div class="stat-box">
                <h3>Active Bookings</h3>
                <p>0</p>
            </div>
            <div class="stat-box">
                <h3>Completed Charges</h3>
                <p>0</p>
            </div>
        </div>
    </main>
</body>
</html>