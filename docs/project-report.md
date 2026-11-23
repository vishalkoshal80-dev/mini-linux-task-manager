# MINI LINUX TASK MANAGER
## Project Report

### 1. Introduction
The Mini Linux Task Manager is a Python-based application developed on Ubuntu Linux. It provides a graphical dashboard to monitor system resources and running processes.

### 2. Problem Statement
Monitoring system performance through terminal commands can be difficult for beginners. This project provides a graphical interface to make system monitoring easier and more convenient.

### 3. Project Objectives
- Monitor CPU utilization.
- Monitor RAM usage.
- Monitor disk usage.
- Display running processes.
- Search for processes.
- Sort processes by CPU and memory usage.
- Automatically refresh system information.

### 4. Technologies Used
| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Ubuntu Linux | Operating environment |
| CustomTkinter | Graphical user interface |
| psutil | System and process information |
| Matplotlib | Graph-related functionality |
| Linux /proc | System information source |

### 5. System Architecture
The project consists of three main modules:

- **system_info.py:** Collects CPU, RAM and disk information.
- **process_manager.py:** Retrieves and organizes running process information.
- **dashboard.py:** Displays system information through a graphical interface.

The `main.py` file launches the dashboard.

### 6. Working of the Project
1. The application starts through `main.py`.
2. The dashboard requests system information.
3. CPU, RAM and disk usage are collected.
4. Running processes are retrieved.
5. Information is displayed in the dashboard.
6. The dashboard refreshes information periodically.

### 7. Testing
The following checks were performed manually:

- Linux system monitoring commands.
- Dashboard launching.
- Live data refresh.
- Process search.
- CPU sorting.
- Memory sorting.

### 8. Results
The application successfully launches its graphical dashboard and displays system resource information and running processes in the Ubuntu environment.

### 9. Limitations
- The application currently focuses on monitoring.
- Advanced process management features are not included.
- Historical performance analysis can be improved.

### 10. Future Scope
- Add process termination with appropriate safeguards.
- Add historical performance graphs.
- Add report export functionality.
- Improve dashboard customization.

### 11. Conclusion
The Mini Linux Task Manager demonstrates how Python and Linux system interfaces can be used to build a graphical system monitoring application. It provides a convenient way to observe CPU, memory, disk and process information.
## 12. Project Screenshots
![Main Dashboard](../assets/screenshots/01_dashboard.png)


### 12.1 Main Dashboard
The following screenshot shows the main dashboard displaying CPU, memory, disk and network information.

![Main Dashboard](../assets/screenshots/01_dashboard.png)

### 12.2 Active Processes
This screenshot displays running processes with their PID, CPU usage, memory usage and state.

![Active Processes](../assets/screenshots/02_processes.png)

### 12.3 Process Search
This screenshot demonstrates the process search functionality.

![Process Search](../assets/screenshots/03_search.png)

### 12.4 Process Sorting
This screenshot demonstrates sorting processes by CPU usage.

![Process Sorting](../assets/screenshots/04_sorting.png)

### 12.5 Automated Testing
This screenshot shows the successful execution of automated system information tests.

![Automated Testing](../assets/screenshots/05_terminal_testing.png)