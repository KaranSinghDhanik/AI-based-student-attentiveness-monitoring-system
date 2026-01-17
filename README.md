# AI‑based Student Attentiveness Monitoring System

An intelligent desktop application that uses computer vision and machine learning to monitor and evaluate student attentiveness in real time through webcam input.

This system detects **eye state (open/closed), head movement, and lip movement** to estimate whether a student is attentive or distracted. It also offers a simple GUI to display real‑time feedback and logs.

---

## 🧠 Features

✔ Real‑time attentiveness monitoring using webcam  
✔ Multiple behavioral cues:  
- **Eye State Detection**  
- **Head Movement Detection**  
- **Lip Movement Analysis**  
✔ Track attention patterns over time  
✔ Interactive graphical interface for visualization  
✔ Train your own models with provided training scripts  

---

## 🧰 Tech Stack

- **Python**  
- **OpenCV** – Camera and image processing  
- **TensorFlow / Keras** – Deep learning models  
- **tkinter** – Graphical user interface (GUI)  
- **SQLite** – Local logging of results  

---

## 📁 Repository Structure

```
AI‑based‑student‑attentiveness‑monitoring‑system/
├── eye_state_model.h5
├── head_movement.h5
├── lip_movement_model.h5
├── train.py
├── combined.py
├── Gui.py
├── alldataGui.py
├── attentiveness.db
└── README.md
```

---

## 🚀 Installation

### 1. Clone the repository
```
git clone https://github.com/KaranSinghDhanik/AI-based-student-attentiveness-monitoring-system.git
cd AI-based-student-attentiveness-monitoring-system
```

### 2. Install dependencies
```
pip install opencv-python tensorflow numpy pandas matplotlib
```

### 3. Run the project
```
python Gui.py
```

---

## 📊 How It Works

1. Captures real-time video using webcam  
2. Detects eye state, head movement, and lip movement  
3. Runs pretrained ML models for each feature  
4. Combines results to calculate attentiveness  
5. Displays and stores results in database  

---

## 🏋️ Train Your Own Models

```
python train.py
```

Replace generated `.h5` models in the main directory.

---

## 📌 Future Improvements

- Dashboard for attentiveness analytics  
- Multi-student detection  
- Online class integration  
- Exportable reports  

---

## 📄 License

MIT License

---

## 👨‍💻 Author

**Karan Singh Dhanik**  
BTech Student | AI & Web Development Enthusiast  

---

⭐ If you like this project, give it a star!
