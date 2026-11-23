
import threading
import tkinter as tk
import customtkinter as ctk

try:
    import psutil
except ImportError:
    psutil = None

from src.system_info import (
    get_cpu_usage,
    get_memory_info,
    get_disk_info
)

from src.process_manager import get_processes


# ---------- THEME ----------
ctk.set_appearance_mode("dark")

BG = "#101010"
CARD = "#191919"
CARD_BORDER = "#303030"
TEXT = "#F5F5F5"
MUTED = "#A0A0A0"

BLUE = "#3B82F6"
GREEN = "#10B981"
ORANGE = "#F59E0B"
PURPLE = "#A78BFA"


class LinuxTaskManager(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Mini Linux Task Manager")
        self.geometry("1250x780")
        self.minsize(950, 650)
        self.configure(fg_color=BG)

        self.processes = []
        self.sort_mode = "CPU"
        self.refreshing = False
        self.closing = False

        self.histories = {
            "CPU": [],
            "Memory": [],
            "Disk": [],
            "Network": []
        }

        self.network_previous = None

        self.create_ui()
        self.refresh_data()

    # ---------- MAIN UI ----------

    def create_ui(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_metric_cards()
        self.create_process_section()

    # ---------- TOP CARDS ----------

    def create_metric_cards(self):

        self.cards_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.cards_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=15,
            pady=(15, 10)
        )

        for i in range(4):
            self.cards_frame.grid_columnconfigure(i, weight=1)

        self.cpu_card = self.create_card(
            0, "CPU Usage", BLUE, "System Load"
        )

        self.memory_card = self.create_card(
            1, "Memory", GREEN, "RAM Utilization"
        )

        self.disk_card = self.create_card(
            2, "Disk Usage", ORANGE, "Primary Drive"
        )

        self.network_card = self.create_card(
            3, "Network", PURPLE, "Network Activity"
        )

    def create_card(self, column, title, accent, subtitle):

        card = ctk.CTkFrame(
            self.cards_frame,
            fg_color=CARD,
            corner_radius=12,
            border_width=1,
            border_color=CARD_BORDER
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=6
        )

        card.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=14,
            pady=(12, 0)
        )

        ctk.CTkLabel(
            header,
            text=title,
            font=("Arial", 12, "bold"),
            text_color=MUTED
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="●",
            text_color=accent,
            font=("Arial", 12)
        ).pack(side="right")

        value = ctk.CTkLabel(
            card,
            text="0%",
            font=("Arial", 29, "bold"),
            text_color=TEXT
        )

        value.pack(
            anchor="w",
            padx=14,
            pady=(5, 0)
        )

        description = ctk.CTkLabel(
            card,
            text=subtitle,
            font=("Arial", 10),
            text_color=MUTED
        )

        description.pack(
            anchor="w",
            padx=14
        )

        graph = tk.Canvas(
            card,
            height=48,
            bg=CARD,
            highlightthickness=0
        )

        graph.pack(
            fill="x",
            padx=10,
            pady=(5, 10)
        )

        return {
            "value": value,
            "description": description,
            "graph": graph,
            "color": accent
        }

    # ---------- SPARKLINE ----------

    def draw_graph(self, card, values):

        canvas = card["graph"]
        canvas.delete("all")

        width = max(canvas.winfo_width(), 150)
        height = 48

        if len(values) < 2:
            return

        values = values[-35:]
        points = []

        for i, value in enumerate(values):

            x = 3 + i * (width - 6) / (len(values) - 1)

            y = height - 4 - (
                max(0, min(value, 100)) / 100
            ) * (height - 9)

            points.extend([x, y])

        canvas.create_line(
            0,
            height - 2,
            width,
            height - 2,
            fill="#333333"
        )

        canvas.create_line(
            *points,
            fill=card["color"],
            width=2,
            smooth=True
        )

    # ---------- PROCESS SECTION ----------

    def create_process_section(self):

        section = ctk.CTkFrame(
            self,
            fg_color=BG,
            corner_radius=0
        )

        section.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(5, 15)
        )

        section.grid_columnconfigure(0, weight=1)
        section.grid_rowconfigure(1, weight=1)

        # Toolbar
        toolbar = ctk.CTkFrame(
            section,
            fg_color="transparent"
        )

        toolbar.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        ctk.CTkLabel(
            toolbar,
            text="Active Processes",
            font=("Arial", 21, "bold"),
            text_color=TEXT
        ).pack(side="left")

        self.total_label = ctk.CTkLabel(
            toolbar,
            text="0 processes",
            font=("Arial", 11),
            text_color=MUTED
        )

        self.total_label.pack(
            side="left",
            padx=12
        )

        self.refresh_button = ctk.CTkButton(
            toolbar,
            text="↻  Refresh",
            width=100,
            height=34,
            fg_color="#252525",
            hover_color="#383838",
            text_color=TEXT,
            command=self.refresh_data
        )

        self.refresh_button.pack(side="right")

        self.sort_menu = ctk.CTkOptionMenu(
            toolbar,
            values=["CPU", "Memory", "Name"],
            command=self.change_sort,
            width=115,
            height=34,
            fg_color="#252525",
            button_color="#383838",
            button_hover_color="#505050"
        )

        self.sort_menu.pack(
            side="right",
            padx=8
        )

        self.search_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="Search process...",
            width=190,
            height=34,
            fg_color="#1C1C1C",
            border_color="#333333"
        )

        self.search_entry.pack(
            side="right",
            padx=8
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.render_processes()
        )

        # Table container
        table = ctk.CTkFrame(
            section,
            fg_color=CARD,
            corner_radius=12,
            border_width=1,
            border_color=CARD_BORDER
        )

        table.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        table.grid_columnconfigure(0, weight=1)
        table.grid_rowconfigure(1, weight=1)

        # Table headings
        headings = ctk.CTkFrame(
            table,
            fg_color="#252525",
            corner_radius=7,
            height=44
        )

        headings.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        headings.grid_propagate(False)

        self.columns = [
            ("PID", 0.09),
            ("Name", 0.30),
            ("CPU", 0.14),
            ("Memory", 0.16),
            ("Mem %", 0.14),
            ("State", 0.17)
        ]

        position = 0

        for name, width in self.columns:

            ctk.CTkLabel(
                headings,
                text=name,
                font=("Arial", 12, "bold"),
                text_color=MUTED,
                anchor="w"
            ).place(
                relx=position,
                rely=0,
                relwidth=width,
                relheight=1
            )

            position += width

        self.process_frame = ctk.CTkScrollableFrame(
            table,
            fg_color="transparent"
        )

        self.process_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 8)
        )

        # Footer
        footer = ctk.CTkFrame(
            table,
            fg_color="transparent"
        )

        footer.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=15,
            pady=(0, 10)
        )

        self.status_label = ctk.CTkLabel(
            footer,
            text="● CONNECTING",
            text_color=GREEN,
            font=("Arial", 10, "bold")
        )

        self.status_label.pack(side="left")

        self.network_label = ctk.CTkLabel(
            footer,
            text="Network: Waiting...",
            text_color=MUTED,
            font=("Arial", 10)
        )

        self.network_label.pack(side="right")

    # ---------- DATA COLLECTION ----------

    def refresh_data(self):

        if self.refreshing or self.closing:
            return

        self.refreshing = True

        self.status_label.configure(
            text="● UPDATING",
            text_color=ORANGE
        )

        self.refresh_button.configure(
            state="disabled"
        )

        def worker():

            try:

                cpu = get_cpu_usage()
                memory = get_memory_info()
                disk = get_disk_info()

                processes = get_processes(interval=1)

                network = None

                if psutil is not None:
                    network = psutil.net_io_counters()

                if not self.closing:

                    self.after(
                        0,
                        lambda: self.update_ui(
                            cpu,
                            memory,
                            disk,
                            processes,
                            network
                        )
                    )

            except Exception as error:

                if not self.closing:

                    self.after(
                        0,
                        lambda: self.show_error(str(error))
                    )

        threading.Thread(
            target=worker,
            daemon=True
        ).start()

    # ---------- UI UPDATE ----------

    def update_ui(self, cpu, memory, disk, processes, network):

        if self.closing:
            return

        cpu = float(cpu)
        ram = float(memory["usage_percent"])
        disk_usage = float(disk["usage_percent"])

        self.cpu_card["value"].configure(
            text=f"{cpu:.1f}%"
        )

        self.memory_card["value"].configure(
            text=f"{ram:.1f}%"
        )

        self.disk_card["value"].configure(
            text=f"{disk_usage:.1f}%"
        )

        if network is not None:

            if self.network_previous is not None:

                sent = max(
                    0,
                    network.bytes_sent -
                    self.network_previous.bytes_sent
                )

                received = max(
                    0,
                    network.bytes_recv -
                    self.network_previous.bytes_recv
                )

                self.network_card["value"].configure(
                    text=f"↑ {sent / 1024:.1f} KB/s"
                )

                self.network_card["description"].configure(
                    text=f"↓ {received / 1024:.1f} KB/s"
                )

                self.network_label.configure(
                    text=(
                        f"Network  ↑ {sent / 1024:.1f} KB/s"
                        f"     ↓ {received / 1024:.1f} KB/s"
                    )
                )

                network_activity = min(
                    100,
                    (sent + received) / 1024 / 10
                )

            else:
                network_activity = 0

            self.network_previous = network

        else:

            network_activity = 0

            self.network_card["value"].configure(
                text="N/A"
            )

            self.network_card["description"].configure(
                text="psutil unavailable"
            )

        self.histories["CPU"].append(cpu)
        self.histories["Memory"].append(ram)
        self.histories["Disk"].append(disk_usage)
        self.histories["Network"].append(network_activity)

        for key in self.histories:
            self.histories[key] = self.histories[key][-35:]

        self.draw_graph(
            self.cpu_card,
            self.histories["CPU"]
        )

        self.draw_graph(
            self.memory_card,
            self.histories["Memory"]
        )

        self.draw_graph(
            self.disk_card,
            self.histories["Disk"]
        )

        self.draw_graph(
            self.network_card,
            self.histories["Network"]
        )

        self.processes = processes
        self.render_processes()

        self.total_label.configure(
            text=f"{len(processes)} processes"
        )

        self.status_label.configure(
            text="● LIVE MONITORING",
            text_color=GREEN
        )

        self.refresh_button.configure(
            state="normal"
        )

        self.refreshing = False

        if not self.closing:
            self.after(2000, self.refresh_data)

    # ---------- PROCESS SEARCH AND SORT ----------

    def change_sort(self, choice):

        self.sort_mode = choice
        self.render_processes()

    def render_processes(self):

        if not hasattr(self, "process_frame"):
            return

        for widget in self.process_frame.winfo_children():
            widget.destroy()

        search = self.search_entry.get().lower()

        filtered = [
            p for p in self.processes
            if search in p["name"].lower()
            or search in str(p["pid"])
        ]

        if self.sort_mode == "CPU":

            filtered.sort(
                key=lambda p: p["cpu"],
                reverse=True
            )

        elif self.sort_mode == "Memory":

            filtered.sort(
                key=lambda p: p["memory"],
                reverse=True
            )

        else:

            filtered.sort(
                key=lambda p: p["name"].lower()
            )

        for index, process in enumerate(filtered):

            # Improved process row
            row = ctk.CTkFrame(
                self.process_frame,
                fg_color=(
                    "#202020"
                    if index % 2 == 0
                    else "#171717"
                ),
                corner_radius=6,
                height=46
            )

            row.pack(
                fill="x",
                pady=3
            )

            row.pack_propagate(False)

            values = [
                process["pid"],
                process["name"][:28],
                f"{process['cpu']}%",
                f"{process['memory']} MB",
                f"{process['memory_percent']}%",
                process["state"]
            ]

            position = 0

            for i, ((_, width), value) in enumerate(
                zip(self.columns, values)
            ):

                color = TEXT

                if i == 2:
                    color = BLUE

                elif i == 3 or i == 4:
                    color = GREEN

                elif i == 5:
                    color = MUTED

                ctk.CTkLabel(
                    row,
                    text=str(value),
                    anchor="w",
                    font=("Arial", 12),
                    text_color=color
                ).place(
                    relx=position,
                    rely=0,
                    relwidth=width,
                    relheight=1
                )

                position += width

    # ---------- ERROR HANDLING ----------

    def show_error(self, error):

        if self.closing:
            return

        self.status_label.configure(
            text="● UPDATE FAILED",
            text_color="#EF4444"
        )

        self.network_label.configure(
            text=f"Error: {error}"
        )

        self.refresh_button.configure(
            state="normal"
        )

        self.refreshing = False

        self.after(3000, self.refresh_data)

    # ---------- CLOSE ----------

    def on_close(self):

        self.closing = True
        self.destroy()


def launch_dashboard():

    app = LinuxTaskManager()

    app.protocol(
        "WM_DELETE_WINDOW",
        app.on_close
    )

    app.mainloop()


if __name__ == "__main__":
    launch_dashboard()
