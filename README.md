# 🎯 Quantum Dart - Interactive Quantum Simulation

An interactive visualization tool and multiplayer game that gamifies Quantum Mechanics concepts (Pauli Gates) using Python and Pygame. This project simulates quantum state changes through a dart game mechanic, featuring dynamic visual effects and real-time score tracking.

## 🚀 Features

* **Quantum Logic Gates:** visualizes Pauli-X (Bit Flip), Pauli-Z (Phase Flip), and Identity operations.
* **Dynamic Multiplayer:** Supports customizable player counts (N-players) with name input interface.
* **Visual Physics Engine:** Custom particle system, shockwaves, and neon aesthetics built from scratch.
* **Responsive UI:** Auto-scaling text and HUD based on screen resolution and player count.
* **Miss Mechanic:** "Karavana" (Zero Point) system for missed shots.

## 🎮 Controls

The game is controlled via keyboard inputs to simulate quantum gate applications:

| Key | Function | Description |
| :--- | :--- | :--- |
| **`X`** | **Bit Flip (Pauli-X)** | Inverts the probability amplitude (High Risk/Reward). |
| **`Z`** | **Phase Flip (Pauli-Z)** | Changes the phase of the quantum state (Negative/Positive Score). |
| **`I`** or **`1`** | **Identity** | Leaves the state unchanged (Safe Score). |
| **`SPACE`** or **`0`** | **Miss (Karavana)** | Registers a missed shot (0 Points). |
| **`ESC`** | **Exit** | Quits the application. |
| **`R`** | **Restart** | Resets the game session (when game over). |

## 🛠️ Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/ZeroPyon/Quantum-Dart.git](https://github.com/ZeroPyon/Quantum-Dart.git)
    ```
2.  **Install dependencies:**
    You need Python installed. This project uses `pygame`.
    ```bash
    pip install pygame
    ```
3.  **Run the simulation:**
    ```bash
    python quandart.py
    ```


## 👨‍💻 Technologies Used

* **Python 3.x**
* **Pygame Library** (Rendering & Input Handling)
* **Math Module** (Physics & Particle Calculations)

---
*Developed by [ZeroPyon](https://github.com/ZeroPyon)*
