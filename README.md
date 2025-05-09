# 👁️ Smart Assistive Device for the Visually Impaired

This project is a smart real-time vision assistant for visually impaired individuals. It uses **YOLOv8** for object detection, gives **audio feedback** using text-to-speech, **detects traffic light color**, provides **vibration alerts via Arduino**, and supports **voice commands** like “Repeat that” or “What’s ahead?”.

---

## 🚀 Features

- 🎯 **Real-time Object Detection** using YOLOv8
- 🧠 **Intelligent Speech**: Only speaks when needed, not repeatedly
- 🟢 **Traffic Light Detection**: Identifies red/green lights
- 🤖 **Vibration Feedback**: Alerts user if objects are very close
- 🎙️ **Voice Commands**: Ask “What’s ahead?” or say “Repeat that”
- 🔊 Works even in noisy environments with ambient noise cancellation

---

## 🧰 Tech Stack

| Component         | Technology                     |
|------------------|--------------------------------|
| Object Detection | [YOLOv8](https://github.com/ultralytics/ultralytics) |
| Camera           | OpenCV                         |
| Audio Output     | pyttsx3 (Text-to-Speech)       |
| Voice Input      | SpeechRecognition + Google API |
| Microcontroller  | Arduino with Serial over USB   |
| Vibration        | Controlled via Arduino PWM     |

---

## 🛠️ Hardware Required

- 🔲 Camera (Laptop/USB/Webcam)
- 🔌 Arduino Uno/Nano
- 🔉 Buzzer/Vibrator motor module
- 🔧 Jumper wires, resistors
- 🔋 Power supply (USB or battery)

---

## 🖥️ Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/assistive-vision-device.git
   cd assistive-vision-device
