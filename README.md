# Mini Linux Task Manager

## 1. Project Overview
Mini Linux Task Manager is a Python-based system monitoring application developed on Ubuntu Linux. It provides a graphical dashboard to monitor CPU usage,AM usage, disk usage, and running processes.
<img width="1248" height="776" alt="image" src="https://github.com/user-attachments/assets/f39503f4-4129-4436-9462-63d952b2de80" />
<img width="1241" height="582" alt="image" src="https://github.com/user-attachments/assets/7e175cad-1698-4b30-96b3-2419043fc27b" />
<img width="1237" height="572" alt="image" src="https://github.com/user-attachments/assets/d253616e-7501-4c9a-9c2e-05b1f692d292" />

## 2. Objectives
- Monitor CPU utilization.
- Monitor RAM and disk usage.
- Display running Linux processes.
- Search processes by name.
- Sort processes by CPU and memory usage.
- Refresh system information automatically.

## 3. Technologies Used
- Python
- Ubuntu Linux
- CustomTkinter
- psutil
- Matplotlib
- Linux `/proc` filesystem

## 4. Features
1. CPU Usage Monitoring
2. RAM Usage Monitoring
3. Disk Usage Monitoring
4. Running Process Information
5. Process Search
6. CPU and Memory Sorting
7. Automatic Dashboard Refresh

## 5. Project Structure

```text
mini-linux-task-manager/
├── main.py
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── system_info.py
│   └── process_manager.py
├── tests/
│   └── test_system_info.py
├── assets/
└── docs/
```

## 6. Installation

Clone or open the project directory and create a virtual environment:

```bash
python3 -m venv .venv-linux
source .venv-linux/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Install Tkinter on Ubuntu:

```bash
sudo apt install python3-tk
```

## 7. Run the Project

```bash
python main.py
```

## 8. Linux System Monitoring

The application uses Linux system information, including the `/proc` filesystem, to retrieve CPU and process information. RAM information is collected from `/proc/meminfo`.

## 9. Future Enhancements
- Process termination functionality.
- Process detail view.
- Historical performance graphs.
- Export monitoring reports.
- Improved dashboard customization.

## 10. Conclusion


The Mini Linux Task Manager demonstrates Linux system monitoring using Python. It provides a graphical interface for observing system resource usage and managing process information.


