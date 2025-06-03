import airsim
import time

# Connect to AirSim
client = airsim.MultirotorClient()
client.confirmConnection()
print("✅ Connected to AirSim")

# Enable API control and arm the drone
client.enableApiControl(True)
print("🔧 API control enabled")

client.armDisarm(True)
print("🔫 Drone armed")

# Takeoff and wait
print("🛫 Taking off...")
client.takeoffAsync().join()

# Wait until drone is stabilized
time.sleep(2)

# Move to a safe altitude (negative Z means up in NED)
target_altitude = -30
print(f"📍 Moving to altitude {target_altitude}m")
client.moveToZAsync(target_altitude, 1).join()
time.sleep(1)

# Start recording
client.startRecording()
print("🎥 Recording started")

# Move forward in steps
velocity = 2  # m/s
duration = 1  # seconds per move
steps = 100

print("🚀 Starting forward motion loop")
for i in range(steps):
    # Move in +X direction
    client.moveByVelocityAsync(velocity, 0, 0, duration).join()
    print(f"Step {i + 1}/{steps} completed")
    time.sleep(0.1)

# Stop recording
client.stopRecording()
print("🛑 Recording stopped")

# Land and disarm
print("🛬 Landing...")
client.landAsync().join()

client.armDisarm(False)
print("🔒 Drone disarmed")

client.enableApiControl(False)
print("🔌 API control released")
