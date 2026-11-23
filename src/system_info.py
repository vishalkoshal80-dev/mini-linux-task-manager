
import time
import shutil


def read_cpu_stats():
    """Read CPU statistics from Linux /proc/stat."""
    with open("/proc/stat", "r") as file:
        values = file.readline().split()

    values = list(map(int, values[1:]))

    idle = values[3] + values[4]
    total = sum(values)

    return idle, total


def get_cpu_usage():
    """Calculate CPU usage percentage."""

    idle1, total1 = read_cpu_stats()

    time.sleep(1)

    idle2, total2 = read_cpu_stats()

    total_difference = total2 - total1
    idle_difference = idle2 - idle1

    if total_difference == 0:
        return 0.0

    usage = (
        (total_difference - idle_difference)
        / total_difference
    ) * 100

    return round(usage, 2)


def get_memory_info():
    """Read RAM information from /proc/meminfo."""

    memory = {}

    with open("/proc/meminfo", "r") as file:
        for line in file:
            key, value = line.split(":")
            memory[key] = int(value.strip().split()[0])

    total = memory["MemTotal"]
    available = memory["MemAvailable"]
    used = total - available

    return {
        "total": round(total / 1024, 2),
        "used": round(used / 1024, 2),
        "available": round(available / 1024, 2),
        "usage_percent": round((used / total) * 100, 2)
    }


def get_disk_info():
    """Get disk usage information."""

    total, used, free = shutil.disk_usage("/")

    return {
        "total": round(total / (1024 ** 3), 2),
        "used": round(used / (1024 ** 3), 2),
        "free": round(free / (1024 ** 3), 2),
        "usage_percent": round((used / total) * 100, 2)
    }
