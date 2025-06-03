import airsim
import time

client = airsim.MultirotorClient()
client.confirmConnection()
print("Connected to AirSim.")

client.enableApiControl(True)
print("API control enabled.")

client.armDisarm(True)
print("Drone armed.")

client.takeoffAsync().join()
print("Takeoff complete.")

client.moveToZAsync(-5, 2).join()
print("Moved to altitude -5.")

client.startRecording()
print("Recording started.")

for i in range(100):
    client.moveByVelocityAsync(2, 0, 0, 1).join()
    print(f"Moved forward step {i+1}")
    time.sleep(0.1)

client.stopRecording()
print("Recording stopped.")

client.landAsync().join()
print("Landing complete.")

client.armDisarm(False)
print("Drone disarmed.")

client.enableApiControl(False)
print("API control disabled.")
