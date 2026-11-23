
import os
import time


# Get Linux clock ticks safely
_sysconf = getattr(os, "sysconf", None)
_sysconf_names = getattr(os, "sysconf_names", {})

if callable(_sysconf) and "SC_CLK_TCK" in _sysconf_names:
    CLK_TCK = _sysconf("SC_CLK_TCK")
else:
    CLK_TCK = 100


def read_process_snapshot():
    """Read process information from Linux /proc."""

    processes = {}

    for pid in os.listdir("/proc"):

        if not pid.isdigit():
            continue

        try:
            with open(f"/proc/{pid}/stat", "r") as file:
                stat_data = file.read()

            closing_bracket = stat_data.rfind(")")
            stat_fields = stat_data[closing_bracket + 2:].split()

            name = stat_data[
                stat_data.find("(") + 1:closing_bracket
            ]

            state = stat_fields[0]

            cpu_ticks = (
                int(stat_fields[11]) +
                int(stat_fields[12])
            )

            memory_kb = 0

            with open(f"/proc/{pid}/status", "r") as file:
                for line in file:

                    if line.startswith("VmRSS:"):
                        memory_kb = int(line.split()[1])
                        break

            processes[pid] = {
                "pid": pid,
                "name": name,
                "state": state,
                "cpu_ticks": cpu_ticks,
                "memory": memory_kb
            }

        except (
            FileNotFoundError,
            PermissionError,
            ProcessLookupError,
            ValueError,
            IndexError
        ):
            continue

    return processes


def get_processes(interval=1):
    """Calculate CPU and memory usage of processes."""

    first_snapshot = read_process_snapshot()
    start_time = time.monotonic()

    time.sleep(interval)

    second_snapshot = read_process_snapshot()
    elapsed = time.monotonic() - start_time

    total_memory = 0

    with open("/proc/meminfo", "r") as file:

        for line in file:

            if line.startswith("MemTotal:"):
                total_memory = int(line.split()[1])
                break

    processes = []

    for pid, current in second_snapshot.items():

        previous = first_snapshot.get(pid)

        cpu_percent = 0.0

        if previous and elapsed > 0:

            tick_difference = (
                current["cpu_ticks"] -
                previous["cpu_ticks"]
            )

            cpu_percent = max(
                0.0,
                (tick_difference / CLK_TCK / elapsed) * 100
            )

        memory_kb = current["memory"]

        memory_percent = (
            (memory_kb / total_memory) * 100
            if total_memory > 0 else 0
        )

        processes.append({
            "pid": pid,
            "name": current["name"],
            "cpu": round(cpu_percent, 2),
            "memory": round(memory_kb / 1024, 2),
            "memory_percent": round(memory_percent, 2),
            "state": current["state"]
        })

    processes.sort(
        key=lambda process: process["cpu"],
        reverse=True
    )

    return processes
