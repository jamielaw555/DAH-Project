import time
import RPi.GPIO as GPIO

def reading():
    # Define the GPIO pins for TRIG and ECHO
    TRIG = 17
    ECHO = 27
    
    # Send a 10-microsecond pulse to TRIG
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(TRIG, False)
    
    # Record the last low and high times for ECHO
    while GPIO.input(ECHO) == 0:
        signaloff = time.time()
    
    while GPIO.input(ECHO) == 1:
        signalon = time.time()
    
    # Calculate time elapsed and convert to distance
    timepassed = signalon - signaloff
    distance = (timepassed * 34300) / 2  # distance in cm
    
    return distance

# Disable warnings and set the GPIO mode
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setup TRIG as output and ECHO as input
TRIG = 17
ECHO = 27
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
# Set up LED and buzzer output
LED_PIN = 22
BUZZER_PIN = 23
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

try:
    while True:
        # Take a distance reading
        dist = reading()
        print(f"Distance: {dist:.2f} cm")
        # Check if an object is within a certain distance
        if dist < 20:
            #Turn on the LED and Buzzer
            GPIO.output(LED_PIN, True)
            GPIO.output(BUZZER_PIN, True)
            time.sleep(0.1)
            
            GPIO.output(LED_PIN, False)
            GPIO.ouyput(BUZZER_PIN, False)
        else:
            
            GPIO.output(LED_PIN, False)
            GPIO.output(BUZZER_PIN, False)
        time.sleep(1)  # Wait 1 second before taking the next reading
except KeyboardInterrupt:
    print("Measurement stopped by User")
finally:
    # Clean up GPIO when finished
    GPIO.cleanup()
