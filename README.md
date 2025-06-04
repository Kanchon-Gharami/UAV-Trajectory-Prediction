# 🛸 UAV‑Trajectory‑Prediction

This repo shows you how to fly a virtual drone in AirSim, save its flight path, turn the raw log into clean CSV features, and train a tiny PyTorch Transformer to predict where the drone will be 20 seconds from now—all in a few simple notebooks.

---

## 📂 Project Layout

```text
UAV‑Trajectory‑Prediction/
├─ AirSim_Block/                # put the downloaded Blocks.exe here (not tracked)
│   └─ Blocks.exe
│   Documents/         
│   ├─ AirSim
│   │   ├─ settings.json
├─ raw_data/                    # will be generated at runtime
│   ├─ images/         
│   ├─ airsim_rec.txt     
│   └─ airsim_trajectory.csv
├─ data_collector.py            # script to record a flight and save airsim_rec.txt
├─ data_preprocessor.ipynb      # cleans log → CSV, adds features, builds windows
├─ trajectory_prediction.ipynb  # trains Transformer & visualises results
├─ README.md                    # project guide (this file)

```
**Note:**  
    * The following are **not present in a this repo**:  
    * `AirSim_Block/`, `raw_data/`.  
    * They are created automatically when you run **`data_collector.py`** and the preprocessing notebook.



## 🛸 Quick Start

```bash
git clone https://github.com/Kanchon-Gharami/UAV-Trajectory-Prediction.git
cd UAV-Trajectory-Prediction

# 1️⃣  create a Python env (optional, but highly recommended)
python -m venv AirEnv
AirEnv\Scripts\activate.bat        # Linux: source AirEnv/bin/activate

# 3️⃣  download simulator (one‑time)
#     https://github.com/microsoft/AirSim/releases → Blocks.zip
unzip Blocks.zip -d AirSim_Block
```

### 1️⃣ Data Collection via AirSim

* **Install Dependencies** Make sure your virtual environment is already active, if not active it with: `AirEnv\Scripts\activate.bat`.
     ```bash
     pip install --upgrade pip
     pip install numpy
     pip install msgpack-rpc-python
     pip install opencv-python
     pip install airsim
     ```
     Note: if `pip install --upgrade pip` create problem use `python -m ensurepip --upgrade`
* **Launch** `Blocks.exe`. 
    Downloaded from: https://github.com/microsoft/AirSim/releases
    * **Note:** Open this Blocks.exe, and press `No` for question "Would you like to use car simulation? Choose no to use quadrotor simulation". This software may require DirectX to install on your computer. Once you run this simulator, press `windows` key(between your `ctrl` and `alt` key) to navigate into the command prompt. You need to run the `data_collector.py` when the simulator is already running behind.
    * Play with Blocks.exe: Press `F1` For help/tools, press `/` for FPV view, press `0` for all types of view. `Alt+F4` for quite this simulator.
* Run **`data_collector.py`** to record a scripted flight.
   ```bash
   python data_collector.py          # converts .txt → airsim_trajectory.csv
   ```
  * `data_collector.py` uses the AirSim API to:
    * arm, take off, and fly a simple pattern,
    * start recording,
    * save **`airsim_rec.txt`** containing  
      `TimeStamp, POS_X, POS_Y, POS_Z, Q_W, Q_X, Q_Y, Q_Z, ImageFile`.  

* AirSim writes: Inside the `Documents` direcotry.
  * **`[time_of_data_collection]/airsim_rec.txt`** – raw log (tab‑delimited)
  * **`[time_of_data_collection]/images/`** – PNG frames captured by the forward camera
  * Copy this `airsim_rec.txt` file and `images/` directory and paste it newly created `raw_data/` directory inside your project's root folder.


### 2️⃣ Data Preprocessing
* **Install Dependencies** Make sure your virtual environment is already active, if not active it with: `AirEnv\Scripts\activate.bat`.
     ```bash
      pip install ipykernel
      pip install pandas
      pip install scipy
     ```
* Open and run **`data_preprocessor.ipynb`** to convert **`airsim_rec.txt`** into **`airsim_trajectory.csv`**.  
  The notebook:
  1. **Parses** the log and removes the `VehicleName` column.  
  2. **Converts** quaternion (`Q_W, Q_X, Q_Y, Q_Z`) ➜ **roll, pitch, yaw** (radians).  
  3. **Adds** continuous heading features **`YAW_SIN`** and **`YAW_COS`**.  
  4. **Computes** linear velocities **`VEL_X, VEL_Y, VEL_Z`** from position derivatives.  
  5. Saves the cleaned CSV to **`raw_data/airsim_trajectory.csv`**.



### 3️⃣ Trajectory Prediction
* **Install Dependencies** Make sure your virtual environment is already active, if not active it with: `AirEnv\Scripts\activate.bat`.
     ```bash
      pip install matplotlib
      pip install scikit-learn
      pip install tqdm
      pip install torch torchvision torchaudio
     ```
Open and run **`trajectory_prediction.ipynb`** – it walks through the full ML pipeline:
1. **Data‑window creation**  
   * Builds sliding windows *(e.g., past 10 s → future 20 s at 10 Hz)*.
2. **3‑D sanity plot**  
   * Displays one sample (history + future) to verify continuity.
3. **Model**  
   * Trains a lightweight **Transformer** on the windowed dataset.
4. **Visual evaluation**  
   * Plots history (blue), ground‑truth future (green), and **predicted future** (red dashed) in 3‑D.
5. **Metrics**  
   * Computes and prints **RMSE** on the held‑out test set.


### 📊 Sample Results

| Metric                | Typical value on one flight log |
|-----------------------|---------------------------------|
| RMSE (metres)         | about 0.7                       |
| Training time         | under 30-60 mins                |
| Inference latency     | roughly 1 ms per window         |

Numbers vary with flight length, hyper‑parameters, and hardware.



### 🛠️ FAQ

* **No data appears in raw_data**  
  Ensure the simulator is running before beginning to record.

* **Dependency errors appear (for example, tornado or msgpack‑rpc‑python)**  
  Install the missing packages in your environment, then reinstall the AirSim Python client.




### 🗺️ Future Direction

* Multi‑UAV social‑attention modelling  
* Vision‑enabled prediction to avoid obstracles  
* Diffusion‑based multi‑modal futures  

Contributions are welcome!

---

## 📜 License

MIT
