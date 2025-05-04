<?php
require_once '../config.php';
session_start();

if (!isset($_SESSION['user_id'])) {
    header("Location: login.php");
    exit();
}

// Get all available charging stations
$query = "SELECT b.*, cp.type, cp.power_output, cp.price_per_kwh, cp.status 
         FROM bunks b 
         JOIN charging_points cp ON b.id = cp.bunk_id 
         WHERE cp.status = 'available'";
$stations = mysqli_query($conn, $query);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Find Charging Stations - EV Recharge Bunk</title>
    <link rel="stylesheet" href="../style.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
</head>
<body>
    <header>
        <nav>
            <div class="logo">EV Recharge Bunk</div>
            <ul class="nav-links">
                <li><a href="dashboard.php">Dashboard</a></li>
                <li><a href="my-bookings.php">My Bookings</a></li>
                <li><a href="profile.php">Profile</a></li>
                <li><a href="logout.php">Logout</a></li>
            </ul>
        </nav>
    </header>

    <main class="container">
        <h2>Find Charging Stations</h2>
        
        <div class="station-finder">
            <div id="map" class="map-container"></div>
            
            <div class="stations-list">
                <?php while ($station = mysqli_fetch_assoc($stations)) { ?>
                <div class="station-card" data-lat="<?php echo $station['latitude']; ?>" data-lng="<?php echo $station['longitude']; ?>">
                    <h3><?php echo htmlspecialchars($station['name']); ?></h3>
                    <p><strong>Address:</strong> <?php echo htmlspecialchars($station['address']); ?></p>
                    <p><strong>Charger Type:</strong> <?php echo htmlspecialchars($station['type']); ?></p>
                    <p><strong>Power Output:</strong> <?php echo htmlspecialchars($station['power_output']); ?></p>
                    <p><strong>Price:</strong> ₹<?php echo htmlspecialchars($station['price_per_kwh']); ?>/kWh</p>
                    <a href="book-station.php?station_id=<?php echo $station['id']; ?>" class="button">Book Now</a>
                </div>
                <?php } ?>
            </div>
        </div>
    </main>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        // Initialize map
        const map = L.map('map').setView([20.5937, 78.9629], 5);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Add markers for each station
        const stations = document.querySelectorAll('.station-card');
        stations.forEach(station => {
            const lat = station.dataset.lat;
            const lng = station.dataset.lng;
            const name = station.querySelector('h3').textContent;
            
            L.marker([lat, lng])
                .bindPopup(name)
                .addTo(map);
        });
    </script>
</body>
</html>