### Phase 1 — Setup 

Open a terminal in Ubuntu and run these commands one at a time, reading what each does. Don't blind-copy. 
#### Step 1.1 — Update your system:
```bash
sudo apt update && sudo apt upgrade -y
```

#### Step 1.2 — Install Git, Python pip, build tools:
```bash
sudo apt install git python3-pip python3-venv build-essential cmake -y
```

#### Step 1.3 — Clone PX4-Autopilot
Pick a folder you'll keep — I suggest `~/drone-dev/`:
```bash
mkdir -p ~/drone-dev
cd ~/drone-dev
git clone [https://github.com/PX4/PX4-Autopilot.git](https://github.com/PX4/PX4-Autopilot.git) --recursive
```
This downloads ~2 GB. Wait it out. The `--recursive` matters — it pulls in submodules.

#### Step 1.4 — Run the official PX4 setup script
This installs the toolchain, Gazebo, and dependencies — much cleaner than installing things one by one:
```bash
cd ~/drone-dev/PX4-Autopilot
bash ./Tools/setup/ubuntu.sh
```
This takes 15-30 minutes. The script is intended to be run on clean Ubuntu LTS installations, and yours is fresh-ish, so you should be fine. It will ask for sudo password at some point. Reboot after it finishes.

#### Step 1.5 — Install MAVSDK-Python in a virtual environment
Don't install Python packages globally — use a `venv` per project. This is professional practice:
```bash
cd ~/drone-dev
python3 -m venv venv
source venv/bin/activate
pip install mavsdk
pip install matplotlib
```
When you see `(venv)` in your terminal prompt, you're inside the venv. To leave: type `deactivate`. Every time you work on this project, run `source ~/drone-dev/venv/bin/activate` first.

#### Step 1.6 — First simulator launch
Open one terminal, navigate to PX4-Autopilot, and run:
```bash
cd ~/drone-dev/PX4-Autopilot
make px4_sitl gz_x500
```
The first build takes 10-20 minutes. Be patient. Eventually a Gazebo window opens with a quadcopter (the X500 model) sitting on the ground. PX4 console shows "INFO [tone_alarm] home set" and similar messages.

If you only have one monitor and Gazebo's GUI is heavy, try headless mode:
```bash
HEADLESS=1 make px4_sitl gz_x500
```
When you see the drone in Gazebo (or PX4 ready in headless mode), Phase 1 is done.

----------------------------