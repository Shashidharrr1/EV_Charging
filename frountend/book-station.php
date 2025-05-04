<?php
require_once '../config.php';
session_start();

if (!isset($_SESSION['user_id'])) {
    header("Location: login.php");
    exit();
}

if (!isset($_GET['station_id'])) {
    header("Location: find-stations.php");
    exit();
}

$station_id = mysqli_real_escape_string($conn, $_GET['station_id']);
$query = "SELECT b.*, cp.id as point_id, cp.type, cp.power_output, cp.price_per_kwh 
         FROM bunks b 
         JOIN charging_points cp ON b.id = cp.bunk_id 
         WHERE cp.id = $station_id AND cp.status = 'available'";
$result = mysqli_query($conn, $query);
$station = mysqli_fetch_assoc($result);

if (!$station) {
    header("Location: find-stations.php");
    exit();
}

$error = '';
$success = '';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $user_id = $_SESSION['user_id'];
    $charging_point_id = $station['point_id'];
    $booking_time = mysqli_real_escape_string($conn, $_POST['booking_time']);
    $duration = mysqli_real_escape_string($conn, $_POST['duration']);

    $query = "INSERT INTO bookings (user_id, charging_point_id, booking_time, duration) 
              VALUES ($user_id, $charging_point_id, '$booking_time', $duration)";
    
    if (mysqli_query($conn, $query)) {
        // Update charging point status
        mysqli_query($conn, "UPDATE charging_points SET status = 'occupied' WHERE id = $charging_point_id");
        $success = "Booking successful!";
    } else {
        $error = "Error: " . mysqli_error($conn);
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Book Station - EV Recharge Bunk</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <div class="auth-container booking-container">
        <h2>Book Charging Station</h2>
        <?php if($error) echo "<div class='error'>$error</div>"; ?>
        <?php if($success) echo "<div class='success'>$success</div>"; ?>
        
        <div class="station-details">
            <h3><?php echo htmlspecialchars($station['name']); ?></h3>
            <p><strong>Address:</strong> <?php echo htmlspecialchars($station['address']); ?></p>
            <p><strong>Charger Type:</strong> <?php echo htmlspecialchars($station['type']); ?></p>
            <p><strong>Power Output:</strong> <?php echo htmlspecialchars($station['power_output']); ?></p>
            <p><strong>Price:</strong> ₹<?php echo htmlspecialchars($station['price_per_kwh']); ?>/kWh</p>
        </div>
        
        <form method="POST" action="">
            <div class="form-group">
                <label for="booking_time">Booking Time:</label>
                <input type="datetime-local" id="booking_time" name="booking_time" required>
            </div>
            
            <div class="form-group">
                <label for="duration">Duration (minutes):</label>
                <input type="number" id="duration" name="duration" min="30" max="180" step="30" required>
            </div>
            
            <button type="submit">Confirm Booking</button>
        </form>
        
        <a href="find-stations.php" class="button secondary">Back to Stations</a>
    </div>

    <script>
    // Set minimum booking time to current time
    const bookingTimeInput = document.getElementById('booking_time');
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    bookingTimeInput.min = now.toISOString().slice(0, 16);
    </script>
</body>
</html>