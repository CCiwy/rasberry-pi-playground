import adafruit_dht
import time
import board

# Set up the sensor type (DHT11 or DHT22) and GPIO pin
sensor_dev = adafruit_dht.DHT11(board.D4)

try:
    while True:
        # Attempt to get sensor reading
        temperature = sensor_dev.temperature
        humidity = sensor_dev.humidity

        # Print results to the terminal
        if humidity is not None and temperature is not None:
            print(f'Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%')
        else:
            print('Failed to retrieve data from the sensor.')

        # Wait for a short interval before the next reading
        time.sleep(2)

except KeyboardInterrupt:
    print('Script terminated by user.')

