<?php
require_once '../config.php';
session_start();

if (!isset($_SESSION['bunk_id'])) {
    header("Location: login.php");
    exit();
}

$bunk_id = $_SESSION['bunk_id'];

// Handle status updates
if (isset($_POST['point_id']) && isset($_POST['status'])) {
    $point_id = mysqli_real_escape_string($conn, $_POST['point_id']);
    $status = mysqli_real_escape_string($conn, $_POST['status']);
    
    $update_query = "UPDATE charging_points SET status = '$status' 
                     WHERE id = $point_id AND bunk_id = $bunk_id";
    mysqli_query($conn, $update_query);
}

// Get all charging points
$query = "SELECT * FROM charging_points WHERE bunk_id = $bunk_id";
$charging_points = mysqli_query($conn, $query);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manage Charging Points - EV Recharge Bunk</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <header>
        <nav>
            <div class="logo">EV Recharge Bunk</div>
            <ul class="nav-links">
                <li><a href="dashboard.php">Dashboard</a></li>
                <li><a href="bookings.php">Bookings</a></li>
                <li><a href="profile.php">Profile</a></li>
                <li><a href="logout.php">Logout</a></li>
            </ul>
        </nav>
    </header>

    <main class="container">
        <h2>Manage Charging Points</h2>
        
        <div class="charging-points-grid">
            <?php while ($point = mysqli_fetch_assoc($charging_points)) { ?>
            <div class="charging-point-card">
                <h3><?php echo htmlspecialchars($point['type']); ?></h3>
                <p><strong>Power Output:</strong> <?php echo htmlspecialchars($point['power_output']); ?></p>
                <p><strong>Price:</strong> ₹<?php echo htmlspecialchars($point['price_per_kwh']); ?>/kWh</p>
                
                <form method="POST" action="" class="status-form">
                    <input type="hidden" name="point_id" value="<?php echo $point['id']; ?>">
                    <label>Status:</label>
                    <select name="status" onchange="this.form.submit()">
                        <option value="available" <?php echo $point['status'] == 'available' ? 'selected' : ''; ?>>Available</option>
                        <option value="occupied" <?php echo $point['status'] == 'occupied' ? 'selected' : ''; ?>>Occupied</option>
                        <option value="maintenance" <?php echo $point['status'] == 'maintenance' ? 'selected' : ''; ?>>Maintenance</option>
                    </select>
                </form>
            </div>
            <?php } ?>
        </div>
        
        <a href="add-charging-point.php" class="button">Add New Charging Point</a>
    </main>
</body>
</html>