from ultralytics import YOLO
import cv2
import pyttsx3
import time
import serial

# === Initialize YOLOv8 Model ===
model = YOLO('yolov8m.pt')  # More accurate than yolov8n

# === Text-to-Speech Engine ===
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Slower speech
engine.setProperty('volume', 1.0)

# === Arduino Serial Communication ===
try:
    arduino = serial.Serial('COM3', 9600)  # Adjust port as needed
except:
    arduino = None
    print("Arduino not connected.")

# === Camera ===
cap = cv2.VideoCapture(0)

# === Speaking Control ===
last_spoken = time.time()
spoken_objects = set()

def speak(sentence):
    print("Speaking:", sentence)
    engine.say(sentence)
    engine.runAndWait()

def get_direction(center_x, width):
    if center_x < width / 3:
        return "left"
    elif center_x < 2 * width / 3:
        return "center"
    else:
        return "right"

def get_distance(box_area):
    if box_area > 50000:
        return "very close"
    elif box_area > 20000:
        return "close"
    else:
        return "far"

def detect_traffic_light_color(cropped):
    hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))
    green_mask = cv2.inRange(hsv, (40, 40, 40), (90, 255, 255))
    red_pixels = cv2.countNonZero(red_mask)
    green_pixels = cv2.countNonZero(green_mask)
    
    if red_pixels > 1000:
        return "red"
    elif green_pixels > 1000:
        return "green"
    else:
        return "unknown"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(frame, imgsz=640)
    annotated_frame = results[0].plot()
    height, width, _ = frame.shape

    clear_path = True  # Assume no obstacles until found

    for r in results:
        for box in r.boxes:
            if box.conf[0] < 0.5:
                continue  # Skip low confidence
            
            class_id = int(box.cls[0])
            label = model.names[class_id]
            x1, y1, x2, y2 = box.xyxy[0]
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            box_area = (x2 - x1) * (y2 - y1)

            direction = get_direction(center_x, width)
            distance = get_distance(box_area)

            # === Handle traffic light detection ===
            if label == "traffic light":
                cropped = frame[int(y1):int(y2), int(x1):int(x2)]
                color = detect_traffic_light_color(cropped)
                if color == "red" and time.time() - last_spoken > 3:
                    speak("Stop. Red light ahead.")
                    last_spoken = time.time()
                elif color == "green" and time.time() - last_spoken > 3:
                    speak("Green light. You may cross.")
                    last_spoken = time.time()
                continue

            clear_path = False  # Found something

            key = (label, direction, distance)
            if key not in spoken_objects and time.time() - last_spoken > 3:
                sentence = f"There is a {label} to your {direction}, it seems {distance}."
                speak(sentence)
                last_spoken = time.time()
                spoken_objects.add(key)

            # === Send vibration command to Arduino ===
            if arduino:
                if distance in ['very close', 'close']:
                    arduino.write(b'v')  # Vibrate
                else:
                    arduino.write(b'n')  # No vibration

    # === Clear path announcement (no objects) ===
    if clear_path and time.time() - last_spoken > 5:
        speak("Path is clear ahead.")
        last_spoken = time.time()
        spoken_objects.clear()
        if arduino:
            arduino.write(b'n')

    # === Show frame (for testing) ===
    cv2.imshow('Assistive Vision', annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()
