<?php
require_once '../config.php';
session_start();

if (!isset($_SESSION['bunk_id'])) {
    header("Location: login.php");
    exit();
}

// Get bunk details
$bunk_id = $_SESSION['bunk_id'];
$query = "SELECT * FROM bunks WHERE id = $bunk_id";
$result = mysqli_query($conn, $query);
$bunk = mysqli_fetch_assoc($result);

// Get charging points
$query = "SELECT * FROM charging_points WHERE bunk_id = $bunk_id";
$charging_points = mysqli_query($conn, $query);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bunk Dashboard - EV Recharge Bunk</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <header>
        <nav>
            <div class="logo">EV Recharge Bunk</div>
            <ul class="nav-links">
                <li><a href="charging-points.php">Charging Points</a></li>
                <li><a href="bookings.php">Bookings</a></li>
                <li><a href="profile.php">Profile</a></li>
                <li><a href="logout.php">Logout</a></li>
            </ul>
        </nav>
    </header>

    <main class="dashboard">
        <h2>Welcome, <?php echo htmlspecialchars($bunk['name']); ?>!</h2>
        
        <div class="bunk-info">
            <h3>Bunk Information</h3>
            <p><strong>Address:</strong> <?php echo htmlspecialchars($bunk['address']); ?></p>
            <p><strong>Owner:</strong> <?php echo htmlspecialchars($bunk['owner_name']); ?></p>
            <p><strong>Email:</strong> <?php echo htmlspecialchars($bunk['email']); ?></p>
        </div>

        <div class="charging-points">
            <h3>Charging Points</h3>
            <table>
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>Power Output</th>
                        <th>Status</th>
                        <th>Price per kWh</th>
                    </tr>
                </thead>
                <tbody>
                    <?php while ($point = mysqli_fetch_assoc($charging_points)) { ?>
                    <tr>
                        <td><?php echo htmlspecialchars($point['type']); ?></td>
                        <td><?php echo htmlspecialchars($point['power_output']); ?></td>
                        <td><?php echo htmlspecialchars($point['status']); ?></td>
                        <td>₹<?php echo htmlspecialchars($point['price_per_kwh']); ?></td>
                    </tr>
                    <?php } ?>
                </tbody>
            </table>
            <a href="add-charging-point.php" class="button">Add New Charging Point</a>
        </div>
    </main>
</body>
</html>