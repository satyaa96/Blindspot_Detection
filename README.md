# 🚗 Blind Spot Detection System for Cars

---

## 📝 Project Overview

This project is a **software simulation** of a **Blind Spot Detection System** aimed at enhancing driver safety by detecting vehicles or objects in the blind spots — areas around a car that are difficult for drivers to see with mirrors alone.

The system continuously monitors nearby vehicles in simulated lanes and alerts the driver visually when an object enters one of the **three critical blind spot zones**:

* **Left rear blind spot**
* **Right rear blind spot**
* **Directly behind the vehicle**

---

## ✨ Features

* **Real-time simulation** of multiple vehicles moving in lanes from both directions
* **Three clearly marked blind spot zones** around the player’s vehicle
* **Visual alerts** when a vehicle enters a blind spot
* **Simple and effective visualization** built using [Pygame](https://www.pygame.org/news)
* **Distance smoothing logic implemented in C** for realistic detection behavior

---

## 🛠️ Technologies Used

| Technology | Purpose                               |
| ---------- | ------------------------------------- |
| Python 3   | Main simulation and visualization     |
| Pygame     | Graphics and animation                |
| C          | Efficient smoothing & detection logic |

---

## 🚀 How It Works

1. The player’s car is placed at the center of the screen.
2. Vehicles spawn randomly in predefined lanes and move either from top to bottom or bottom to top.
3. The system checks if any vehicle collides with the three blind spot zones behind the player’s car.
4. If a vehicle is detected in any blind spot, a **warning message** is displayed indicating which zones are occupied.
5. The detection uses a **moving average filter** in C code to smooth out noisy data and reduce false warnings.

---

## 🚧 Future Enhancements

* Integrate with **real sensor data** for live detection on hardware
* Add **audible alerts** alongside visual warnings
* Implement more **realistic traffic behavior and vehicle models**
* Build an **embedded system version** with hardware interfaces
* Enhance UI with **better graphics and interactive controls**

---
