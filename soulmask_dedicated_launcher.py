import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import json

class DedicatedServerLauncher(tk.Tk):
    def __init__(self):
        super().__init__()

        self.region_entries = {}  # Initialize region_entries here

        self.title("SoulMask Dedicated Server Launcher")
        self.geometry("1000x800")
        
        # Load config
        self.config = self.load_config()

        # Tabs
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=1, fill="both")

        self.main_tab = ttk.Frame(self.tab_control)
        self.config_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.main_tab, text="Main")
        self.tab_control.add(self.config_tab, text="Config")

        # Main tab (General settings and server controls)
        self.create_label_entry(self.main_tab, "Executable Name:", "WSServer.exe")
        self.create_label_entry(self.main_tab, "Map Name:", "Level01_Main")
        self.create_label_entry(self.main_tab, "Steam Server Name:", "")
        self.create_label_entry(self.main_tab, "Max Players:", "4")
        self.create_label_entry(self.main_tab, "Password:", "", show="*")
        self.create_label_entry(self.main_tab, "Admin Password:", "", show="*")

        self.start_button = tk.Button(self.main_tab, text="Start Server", command=self.start_server)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.main_tab, text="Stop Server", command=self.stop_server)
        self.stop_button.pack(pady=5)

        self.save_button = tk.Button(self.main_tab, text="Save Config", command=self.save_config)
        self.save_button.pack(pady=5)

        # Logs
        self.log_text = scrolledtext.ScrolledText(self.main_tab, wrap=tk.WORD, state='disabled')
        self.log_text.pack(expand=1, fill='both')

        self.status_label = tk.Label(self.main_tab, text="Server Status: Stopped", font=("Helvetica", 16))
        self.status_label.pack(pady=10)

        # Config tab
        self.selected_region = tk.StringVar()
        self.region_selector = ttk.Combobox(self.config_tab, textvariable=self.selected_region)
        self.region_selector['values'] = [f"Region {region}" for region in self.config.keys()]
        self.region_selector.bind("<<ComboboxSelected>>", self.load_region_settings)
        self.region_selector.pack(pady=10)

        self.region_frame = ttk.Frame(self.config_tab)
        self.region_frame.pack(expand=1, fill="both")

        self.save_config_button = tk.Button(self.config_tab, text="Save Region Config", command=self.save_region_config)
        self.save_config_button.pack(pady=5)

        self.current_region = None

        self.server_process = None

    def load_config(self):
        with open("config.json", "r", encoding='utf-8') as f:
            return json.load(f)

    def create_label_entry(self, parent, label_text, default_value, show=None):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=5)

        label = tk.Label(frame, text=label_text)
        label.pack(side="left", padx=5)
        entry = tk.Entry(frame, show=show)
        entry.insert(0, default_value)
        entry.pack(side="left", fill="x", expand=True, padx=5)
        setattr(self, label_text.replace(" ", "_").replace(":", "").lower(), entry)
        self.region_entries[label_text.replace(" ", "_").replace(":", "").lower()] = entry

    def create_region_settings(self, parent, config):
        for widget in parent.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        translations = {
            "ExpRatio": "Experience Ratio",
            "CaiJiDiaoLuoRatio": "Gathering Drop Ratio",
            "FaMuDiaoLuoRatio": "Lumber Drop Ratio",
            "CaiKuangDiaoLuoRatio": "Mining Drop Ratio",
            "DongWuShiTiDiaoLuoRatio": "Animal Corpse Drop Ratio",
            "DongWuShiTiZhongYaoDiaoLuoRatio": "Important Animal Corpse Drop Ratio",
            "CaiJiShengChanJianZhuDiaoLuoRatio": "Gathering Production Building Drop Ratio",
            "PuTongRenDiaoLuoRatio": "Common Human Drop Ratio",
            "JingYingRenDiaoLuoRatio": "Elite Human Drop Ratio",
            "BossRenDiaoLuoRatio": "Boss Human Drop Ratio",
            "ZuoWuDropRatio": "Plant Drop Ratio",
            "AddRenKeDuRatio": "Add Human Affinity Ratio",
            "ZuoWuShengZhangRatio": "Plant Growth Ratio",
            "BinSiKaiGuan": "BinSi Switch",
            "JianZhuFuLanMul": "Building Coverage Multiplier",
            "JianZhuXiuLiMul": "Building Repair Multiplier",
            "JianZhuFuLanKaiGuan": "Building Coverage Switch",
            "ZhiZuoTimeRatio": "Crafting Time Ratio",
            "DamageYeShengRatio": "Wild Damage Ratio",
            "BeDamageByYeShengRatio": "Be Damaged by Wild Ratio",
            "GameWorldDayTimePortion": "Game World Day Time Portion",
            "GameWorldTimePower": "Game World Time Power",
            "BaoXiangDropRatio": "Treasure Chest Drop Ratio",
            "HuXIangShangHaiKaiGuan": "Mutual Damage Switch",
            "ZhiBeiChongShengRatio": "Rebirth Ratio",
            "ChengZhangExpRatio": "Growth Experience Ratio",
            "MJExpRatio": "MJ Experience Ratio",
            "ShuLianDuExpRatio": "Proficiency Experience Ratio",
            "NaiJiuXiShu": "Durability Coefficient",
            "ReDuXiShu": "Heat Coefficient",
            "CaiJiExpRatio": "Gathering Experience Ratio",
            "ZhiZuoExpRatio": "Crafting Experience Ratio",
            "ShaGuaiExpRatio": "Monster Killing Experience Ratio",
            "QiTaExpRatio": "Other Experience Ratio",
            "BeiDongYiJiShuXingRatio": "Passive Attribute Ratio",
            "ZhuDongYiJiShuXingRatio": "Active Attribute Ratio",
            "ErJiShuXingRatio": "Secondary Attribute Ratio",
            "MaRenBeiDongYiJiShuXingRatio": "Horseman Passive Attribute Ratio",
            "MaRenZhuDongYiJiShuXingRatio": "Horseman Active Attribute Ratio",
            "MaRenErJiShuXingRatio": "Horseman Secondary Attribute Ratio",
            "DongWuBeiDongYiJiShuXingRatio": "Animal Passive Attribute Ratio",
            "DongWuZhuDongYiJiShuXingRatio": "Animal Active Attribute Ratio",
            "DongWuErJiShuXingRatio": "Animal Secondary Attribute Ratio",
            "ShiWuXiaoHaoRatio": "Food Consumption Ratio",
            "ShuiXiaoHaoRatio": "Water Consumption Ratio",
            "QiXiXiaoHaoRatio": "Energy Consumption Ratio",
            "ShengMingHuiFuRatio": "Health Recovery Ratio",
            "TiLiHuiFuRatio": "Stamina Recovery Ratio",
            "QiXiHuiFuRatio": "Energy Recovery Ratio",
            "DongWuDamageRatio": "Animal Damage Ratio",
            "DongWuJianShangRatio": "Animal Damage Reduction Ratio",
            "MaRenDamageRatio": "Horseman Damage Ratio",
            "ManRenJianShangRatio": "Horseman Damage Reduction Ratio",
            "JiaSiHuiFuRatio": "Armor Recovery Ratio",
            "CaiJiDamageRatio": "Gathering Damage Ratio",
            "ZiYuanShengMingRatio": "Resource Health Ratio",
            "RanLiaoXiaoHaoRatio": "Fuel Consumption Ratio",
            "DongWuShengZhangRatio": "Animal Growth Ratio",
            "FanZhiJianGeRatio": "Reproduction Interval Ratio",
            "DongWuShengChanJianGeRatio": "Animal Production Interval Ratio",
            "DongWuChanChuRatio": "Animal Production Ratio",
            "DongWuXiaoHaoShiWuRatio": "Animal Food Consumption Ratio",
            "DongWuXiaoHaoShuiRatio": "Animal Water Consumption Ratio",
            "ZuoWuFeiLiaoXiaoHaoRatio": "Plant Fertilizer Consumption Ratio",
            "ZuoWuShuiXiaoHaoRatio": "Plant Water Consumption Ratio",
            "ZuoWuXiaoHuiRatio": "Plant Decay Ratio",
            "GongJiJianZhuDamageRatio": "Building Attack Damage Ratio",
            "DongWuPinZhiRatio": "Animal Quality Ratio",
            "ManRenPinZhiRatio": "Horseman Quality Ratio",
            "WanJiaZiYuanJinShuaBanJing": "Player Resource Loading Radius",
            "JianZhuZiYuanJinShuaBanJing": "Building Resource Loading Radius",
            "WuPinFuHuaiRatio": "Item Corruption Ratio",
            "WuPinXiaoHuiTime": "Item Decay Time",
            "XiuLiXuYaoCaiLiaoRatio": "Repair Material Ratio",
            "XiuLiJiangNaiJiuShangXianRatio": "Repair Durability Cap Ratio",
            "RuQinKaiGuan": "Invasion Switch",
            "RuQinGuiMoXiShu": "Invasion Scale Coefficient",
            "RuQinQiangDuXiShu": "Invasion Intensity Coefficient",
            "RuQinGuaiCountMin": "Minimum Invasion Monster Count",
            "RuQinGuaiCountMax": "Maximum Invasion Monster Count",
            "RuQinPerBoGuaiMin": "Minimum Monsters Per Wave",
            "RuQinPerBoGuaiMax": "Maximum Monsters Per Wave",
            "RuQinGuaiLevelXiShu": "Invasion Monster Level Coefficient",
            "TanChaMinuteLimit": "Scouting Time Limit",
            "JinGongMinuteLimit": "Attack Time Limit",
            "LengQueMinuteLimit": "Cooldown Time Limit",
            "ChongsuRatio": "Respawn Ratio",
            "RuQinMaxChangCiCount": "Maximum Invasion Events",
            "RuQinBeginHour": "Invasion Start Hour",
            "RuQinEndHour": "Invasion End Hour",
            "RuQinShaoChengXiShu": "Invasion City Damage Coefficient",
            "RuQinTuShaXiShu": "Invasion Massacre Coefficient",
            "XiuMianDistance": "Sleep Distance",
            "HuanXingDistance": "Wake Distance",
            "GongHuiMaxZhaoMuCount": "Guild Maximum Recruitment Count",
            "GeRenMaxZhaoMuCount": "Personal Maximum Recruitment Count",
            "GeRenMaxZhaoMuCount_Two": "Personal Maximum Recruitment Count - Level 2",
            "GeRenMaxZhaoMuCount_Three": "Personal Maximum Recruitment Count - Level 3",
            "XinQingZengZhang": "Mood Increase",
            "XinQingJianShao": "Mood Decrease",
            "XiShuWeiLing": "Coefficient of Negative Effects",
            "HuiFuChuShiBodyData": "Restore Initial Body Data",
            "YouFangShangHaiKaiGuan": "Defensive Damage Switch",
            "YeShengHitJianZhuShangHaiRatio": "Wild Attack Building Damage Ratio",
            "PVP_ShangHaiRatio_WithoutP2P_YouFang": "PVP Damage Ratio Without P2P Defense",
            "WanJiaHitJianZhuShangHaiRatio": "Player Attack Building Damage Ratio",
            "ShaGuaiExpShareRatio": "Monster Killing Experience Share Ratio",
            "YunXuOtherDaKaiGongZuoTai": "Allow Others to Open Workbench",
            "YunXuOtherDaKaiXiangZi": "Allow Others to Open Chest",
            "PVP_ShangHaiRatio_JinZhan": "PVP Damage Ratio Melee",
            "PVP_ShangHaiRatio_YuanCheng": "PVP Damage Ratio Ranged",
            "GongHuiMaxDongWuCount": "Guild Maximum Animal Count",
            "GeRenMaxDongWuCount": "Personal Maximum Animal Count",
            "SuiJiRuQinKaiGuan": "Random Invasion Switch",
            "PanpaKaiGuan": "Pampa Switch",
            "WanJiaBeiXiaoRenRatio": "Player Hunger Ratio",
            "WanJiaBeiXiaoTiRatio": "Player Thirst Ratio",
            "KaiQiJianZhuHuiXueBuilding": "Enable Building Health Restoration",
            "PVP_ShangHaiRatio_PlayerToPlayer_DiFang": "PVP Damage Ratio Player to Player (Defender)",
            "PVP_GAPVPDamageRatio": "PVP GAP Damage Ratio",
            "PlayerYouFangShangHaiKaiGuan": "Player Defensive Damage Switch",
            "MeiTiShiWanKaiGuan": "Media Test Switch",
            "PVP_ShangHaiRatio_PlayerToPlayer_YouFang": "PVP Damage Ratio Player to Player (Offense)",
            "BaoXiangDiaoLuoDengJi": "Treasure Chest Drop Level",
            "KaiQiKuaFu": "Enable Cross-server",
            "FuHuaSpeed": "Incubation Speed",
            "YingHuoRanShaoSuDuRatio": "Firefly Burning Speed Ratio",
            "HuDongExcludeBetweenCameraCharacter": "Exclude Interaction Between Camera and Character",
            "PVPTimeAsiaWorkStartTime": "PVP Time Asia Work Start Time",
            "PVPTimeAsiaWorkEndTime": "PVP Time Asia Work End Time",
            "PVPTimeAsiaNoWorkStartTime": "PVP Time Asia No Work Start Time",
            "PVPTimeAsiaNoWorkEndTime": "PVP Time Asia No Work End Time",
            "PVPTimeAmericaWorkStartTime": "PVP Time America Work Start Time",
            "PVPTimeAmericaWorkEndTime": "PVP Time America Work End Time",
            "PVPTimeAmericaNoWorkStartTime": "PVP Time America No Work Start Time",
            "PVPTimeAmericaNoWorkEndTime": "PVP Time America No Work End Time",
            "PVPTimeEuropeWorkStartTime": "PVP Time Europe Work Start Time",
            "PVPTimeEuropeWorkEndTime": "PVP Time Europe Work End Time",
            "PVPTimeEuropeNoWorkStartTime": "PVP Time Europe No Work Start Time",
            "PVPTimeEuropeNoWorkEndTime": "PVP Time Europe No Work End Time",
            "WuLiYouHuaDist": "Physical Optimization Distance",
            "MovementYouHua": "Movement Optimization",
            "XiuMianOfflineDays": "Offline Days for Sleep Mode",
            "WanJiaShiWanKaiGuan": "Player Test Switch",
            "WuLiYouHuaKaiGuan": "Physical Optimization Switch",
            "TiaoWuLengQueTime": "Dance Cooldown Time",
            "MaxLevel": "Maximum Level",
            "PVEOnlyTongGuiShuCanOpenKaiGuan": "PVE Only Same Guild Can Open Switch",
            "TeShuDaoJuDropXiShuJiaChengKaiGuan": "Special Item Drop Coefficient Bonus Switch",
            "JianZhuChuanSongMenPlusKaiGuan": "Building Teleport Door Plus Switch",
            "FuHuoMoveSiWangBaoKaiGuan": "Revival Movement Death Package Switch"
        }

        self.region_entries = {}
        
        for key, value in config.items():
            translated_key = translations.get(key, key)
            if isinstance(value, bool):
                self.create_checkbox(scrollable_frame, translated_key, value)
            else:
                self.create_label_entry(scrollable_frame, translated_key, str(value))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_checkbox(self, parent, label_text, value):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=5)

        var = tk.BooleanVar(value=value)
        checkbox = ttk.Checkbutton(frame, text=label_text, variable=var)
        checkbox.pack(side="left", padx=5)
        self.region_entries[label_text.replace(" ", "_").replace(":", "").lower()] = var

    def load_region_settings(self, event):
        region = self.selected_region.get().split()[-1]
        if region in self.config:
            self.current_region = region
            self.create_region_settings(self.region_frame, self.config[region])

    def start_server(self):
        if self.server_process and self.server_process.poll() is None:
            messagebox.showwarning("Server Running", "The server is already running.")
            return

        exe_name = self.executable_name.get()
        map_name = self.map_name.get()
        steam_server_name = self.steam_server_name.get()
        max_players = self.max_players.get()
        password = self.password.get()
        admin_password = self.admin_password.get()

        server_args = "-server -log -UTF8Output -MULTIHOME=0.0.0.0 -EchoPort=18888 -forcepassthrough -pve"

        command = [
            exe_name, map_name,
            server_args,
            f"-SteamServerName=\"{steam_server_name}\"",
            f"-MaxPlayers={max_players}",
            f"-PSW=\"{password}\"",
            f"-adminpsw=\"{admin_password}\""
        ]

        def run_server():
            self.server_process = subprocess.Popen(" ".join(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            self.status_label.config(text="Server Status: Running")

            for stdout_line in iter(self.server_process.stdout.readline, ""):
                self.log_text.config(state='normal')
                self.log_text.insert(tk.END, stdout_line)
                self.log_text.config(state='disabled')
                self.log_text.see(tk.END)
            self.server_process.stdout.close()

            self.status_label.config(text="Server Status: Stopped")

        threading.Thread(target=run_server, daemon=True).start()

    def stop_server(self):
        if self.server_process and self.server_process.poll() is None:
            self.server_process.terminate()
            self.server_process = None
            self.status_label.config(text="Server Status: Stopped")
            messagebox.showinfo("Server Stopped", "The server has been stopped.")
        else:
            messagebox.showwarning("Server Not Running", "No server is currently running.")

    def save_config(self):
        for region, settings in self.config.items():
            if str(region) == str(self.current_region):
                for key, value in settings.items():
                    widget_key = key.replace(" ", "_").replace(":", "").lower()
                    widget = self.region_entries.get(widget_key)
                    if widget:
                        if isinstance(widget, tk.BooleanVar):
                            self.config[region][key] = widget.get()
                        else:
                            self.config[region][key] = widget.get()
        with open("config.json", "w", encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

        messagebox.showinfo("Save Config", "Configuration saved successfully.")

    def save_region_config(self):
        if self.current_region:
            self.save_config()

if __name__ == "__main__":
    app = DedicatedServerLauncher()
    app.mainloop()