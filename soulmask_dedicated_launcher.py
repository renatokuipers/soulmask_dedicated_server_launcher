import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from translations import TRANSLATIONS as translations
import subprocess
import urllib.request
import zipfile
import shutil
import logging
from pathlib import Path
from urllib.error import URLError, HTTPError
import threading

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for server setup
STEAMCMD_URL = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
DEFAULT_STEAMCMD_DIR = Path("C:/steamcmd")
DEFAULT_SERVER_DIR = Path("C:/steamcmd/steamapps/common/Soulmask Dedicated Server For Windows")
DEFAULT_SAVED_DIR = DEFAULT_SERVER_DIR / "WS" / "Saved"
DEFAULT_CONFIG_DIR = DEFAULT_SAVED_DIR / "Config" / "WindowsServer"
DEFAULT_GAMEPLAYSETTINGS_DIR = DEFAULT_SAVED_DIR / "GamePlaySettings"
ENGINE_INI_CONTENT = """[Core.System]
Paths=../../../Engine/Content
Paths=%GAMEDIR%Content
Paths=../../../Engine/Plugins/Experimental/CommonUI/Content
Paths=../../../WS/Plugins/DungeonArchitect/Content
Paths=../../../Engine/Plugins/Runtime/AMD/FSR/Content
Paths=../../../Engine/Plugins/Experimental/PythonScriptPlugin/Content
Paths=../../../Engine/Plugins/FX/Niagara/Content
Paths=../../../Engine/Plugins/Experimental/Water/Content
Paths=../../../Engine/Plugins/Experimental/Landmass/Content
Paths=../../../Engine/Plugins/Experimental/GeometryProcessing/Content
Paths=../../../Engine/Plugins/Runtime/Nvidia/DLSS/Content
Paths=../../../WS/Plugins/AntiGS/Content
Paths=../../../WS/Plugins/DBChuli/Content
Paths=../../../WS/Plugins/GBufferModifyPlugin/Content
Paths=../../../WS/Plugins/LoadingScreen/Content
Paths=../../../WS/Plugins/PacketCheckHandlerComponent/Content
Paths=../../../WS/Plugins/Wwise/Content
Paths=../../../Engine/Plugins/Editor/GeometryMode/Content
Paths=../../../Engine/Plugins/Developer/AnimationSharing/Content
Paths=../../../Engine/Plugins/Editor/SpeedTreeImporter/Content
Paths=../../../Engine/Plugins/Enterprise/DatasmithContent/Content
Paths=../../../Engine/Plugins/Media/MediaCompositing/Content
Paths=../../../Engine/Plugins/Runtime/Synthesis/Content
Paths=../../../Engine/Plugins/Runtime/AudioSynesthesia/Content

[URL]
Port=7777

[Dedicated.Settings]
SteamServerName="My Soulmask Server"
MaxPlayers=4
pvp=False
backup=900
saving=600
"""
GAME_XISHU_JSON_CONTENT = {
    "0": {
        "ExpRatio": 1,
        "CaiJiDiaoLuoRatio": 1,
        "FaMuDiaoLuoRatio": 1,
        "CaiKuangDiaoLuoRatio": 1,
        "DongWuShiTiDiaoLuoRatio": 1,
        "DongWuShiTiZhongYaoDiaoLuoRatio": 1,
        "CaiJiShengChanJianZhuDiaoLuoRatio": 1,
        "PuTongRenDiaoLuoRatio": 1,
        "JingYingRenDiaoLuoRatio": 1,
        "BossRenDiaoLuoRatio": 1,
        "ZuoWuDropRatio": 1,
        "AddRenKeDuRatio": 1,
        "ZuoWuShengZhangRatio": 1,
        "BinSiKaiGuan": 1,
        "JianZhuFuLanMul": 1,
        "JianZhuXiuLiMul": 1,
        "JianZhuFuLanKaiGuan": 1,
        "ZhiZuoTimeRatio": 1,
        "DamageYeShengRatio": 1,
        "BeDamageByYeShengRatio": 1,
        "GameWorldDayTimePortion": 0.699999988079071,
        "GameWorldTimePower": 24,
        "BaoXiangDropRatio": 1,
        "HuXIangShangHaiKaiGuan": 1,
        "ZhiBeiChongShengRatio": 1,
        "ChengZhangExpRatio": 1,
        "MJExpRatio": 1,
        "ShuLianDuExpRatio": 1,
        "NaiJiuXiShu": 1,
        "ReDuXiShu": 1,
        "CaiJiExpRatio": 1,
        "ZhiZuoExpRatio": 1,
        "ShaGuaiExpRatio": 1,
        "QiTaExpRatio": 1,
        "BeiDongYiJiShuXingRatio": 1,
        "ZhuDongYiJiShuXingRatio": 1,
        "ErJiShuXingRatio": 1,
        "MaRenBeiDongYiJiShuXingRatio": 1,
        "MaRenZhuDongYiJiShuXingRatio": 1,
        "MaRenErJiShuXingRatio": 1,
        "DongWuBeiDongYiJiShuXingRatio": 1,
        "DongWuZhuDongYiJiShuXingRatio": 1,
        "DongWuErJiShuXingRatio": 1,
        "ShiWuXiaoHaoRatio": 1,
        "ShuiXiaoHaoRatio": 1,
        "QiXiXiaoHaoRatio": 1,
        "ShengMingHuiFuRatio": 1,
        "TiLiHuiFuRatio": 1,
        "QiXiHuiFuRatio": 1,
        "DongWuDamageRatio": 1,
        "DongWuJianShangRatio": 1,
        "MaRenDamageRatio": 1,
        "ManRenJianShangRatio": 1,
        "JiaSiHuiFuRatio": 1,
        "CaiJiDamageRatio": 1,
        "ZiYuanShengMingRatio": 1,
        "RanLiaoXiaoHaoRatio": 1,
        "DongWuShengZhangRatio": 1,
        "FanZhiJianGeRatio": 1,
        "DongWuShengChanJianGeRatio": 1,
        "DongWuChanChuRatio": 1,
        "DongWuXiaoHaoShiWuRatio": 1,
        "DongWuXiaoHaoShuiRatio": 1,
        "ZuoWuFeiLiaoXiaoHaoRatio": 1,
        "ZuoWuShuiXiaoHaoRatio": 1,
        "ZuoWuXiaoHuiRatio": 1,
        "GongJiJianZhuDamageRatio": 1,
        "DongWuPinZhiRatio": 1,
        "ManRenPinZhiRatio": 1,
        "WanJiaZiYuanJinShuaBanJing": 1,
        "JianZhuZiYuanJinShuaBanJing": 1,
        "WuPinFuHuaiRatio": 1,
        "WuPinXiaoHuiTime": 1,
        "XiuLiXuYaoCaiLiaoRatio": 1,
        "XiuLiJiangNaiJiuShangXianRatio": 1,
        "RuQinKaiGuan": 1,
        "RuQinGuiMoXiShu": 1,
        "RuQinQiangDuXiShu": 1,
        "RuQinGuaiCountMin": 8,
        "RuQinGuaiCountMax": 128,
        "RuQinPerBoGuaiMin": 3,
        "RuQinPerBoGuaiMax": 16,
        "RuQinGuaiLevelXiShu": 1,
        "TanChaMinuteLimit": 20,
        "JinGongMinuteLimit": 90,
        "LengQueMinuteLimit": 1440,
        "ChongsuRatio": 1,
        "RuQinMaxChangCiCount": 2,
        "RuQinBeginHour": 0,
        "RuQinEndHour": 24,
        "RuQinShaoChengXiShu": 0.6000000238418579,
        "RuQinTuShaXiShu": 0.30000001192092896,
        "XiuMianDistance": 10000,
        "HuanXingDistance": 9000,
        "GongHuiMaxZhaoMuCount": 50,
        "GeRenMaxZhaoMuCount": 6,
        "GeRenMaxZhaoMuCount_Two": 10,
        "GeRenMaxZhaoMuCount_Three": 15,
        "XinQingZengZhang": 1,
        "XinQingJianShao": 1,
        "XiShuWeiLing": 0,
        "HuiFuChuShiBodyData": 1,
        "YouFangShangHaiKaiGuan": 0,
        "YeShengHitJianZhuShangHaiRatio": 4,
        "PVP_ShangHaiRatio_WithoutP2P_YouFang": 0,
        "WanJiaHitJianZhuShangHaiRatio": 1,
        "ShaGuaiExpShareRatio": 0.20000000298023224,
        "YunXuOtherDaKaiGongZuoTai": 0,
        "YunXuOtherDaKaiXiangZi": 0,
        "PVP_ShangHaiRatio_JinZhan": 0.4000000059604645,
        "PVP_ShangHaiRatio_YuanCheng": 0.4000000059604645,
        "GongHuiMaxDongWuCount": 50,
        "GeRenMaxDongWuCount": 10,
        "SuiJiRuQinKaiGuan": 1,
        "PanpaKaiGuan": 1,
        "WanJiaBeiXiaoRenRatio": 0.800000011920929,
        "WanJiaBeiXiaoTiRatio": 0.800000011920929,
        "KaiQiJianZhuHuiXueBuilding": 1,
        "PVP_ShangHaiRatio_PlayerToPlayer_DiFang": 1,
        "PVP_GAPVPDamageRatio": 1,
        "PlayerYouFangShangHaiKaiGuan": 1,
        "MeiTiShiWanKaiGuan": 0,
        "PVP_ShangHaiRatio_PlayerToPlayer_YouFang": 0.05999999865889549,
        "BaoXiangDiaoLuoDengJi": 0,
        "KaiQiKuaFu": 0,
        "FuHuaSpeed": 1,
        "YingHuoRanShaoSuDuRatio": 1,
        "HuDongExcludeBetweenCameraCharacter": 1,
        "PVPTimeAsiaWorkStartTime": 0,
        "PVPTimeAsiaWorkEndTime": 24,
        "PVPTimeAsiaNoWorkStartTime": 0,
        "PVPTimeAsiaNoWorkEndTime": 24,
        "PVPTimeAmericaWorkStartTime": 0,
        "PVPTimeAmericaWorkEndTime": 24,
        "PVPTimeAmericaNoWorkStartTime": 0,
        "PVPTimeAmericaNoWorkEndTime": 24,
        "PVPTimeEuropeWorkStartTime": 0,
        "PVPTimeEuropeWorkEndTime": 24,
        "PVPTimeEuropeNoWorkStartTime": 0,
        "PVPTimeEuropeNoWorkEndTime": 24,
        "WuLiYouHuaDist": 6666,
        "MovementYouHua": 1,
        "XiuMianOfflineDays": 7,
        "WanJiaShiWanKaiGuan": 0,
        "WuLiYouHuaKaiGuan": 1,
        "TiaoWuLengQueTime": 4,
        "MaxLevel": 60,
        "PVEOnlyTongGuiShuCanOpenKaiGuan": 1,
        "TeShuDaoJuDropXiShuJiaChengKaiGuan": 0,
        "JianZhuChuanSongMenPlusKaiGuan": 0,
        "FuHuoMoveSiWangBaoKaiGuan": 0
    },
    "1": {
        "ExpRatio": 1,
        "CaiJiDiaoLuoRatio": 1,
        "FaMuDiaoLuoRatio": 1,
        "CaiKuangDiaoLuoRatio": 1,
        "DongWuShiTiDiaoLuoRatio": 1,
        "DongWuShiTiZhongYaoDiaoLuoRatio": 1,
        "CaiJiShengChanJianZhuDiaoLuoRatio": 1,
        "PuTongRenDiaoLuoRatio": 1,
        "JingYingRenDiaoLuoRatio": 1,
        "BossRenDiaoLuoRatio": 1,
        "ZuoWuDropRatio": 1,
        "AddRenKeDuRatio": 1,
        "ZuoWuShengZhangRatio": 1,
        "BinSiKaiGuan": 1,
        "JianZhuFuLanMul": 1,
        "JianZhuXiuLiMul": 1,
        "JianZhuFuLanKaiGuan": 1,
        "ZhiZuoTimeRatio": 1,
        "DamageYeShengRatio": 1,
        "BeDamageByYeShengRatio": 1,
        "GameWorldDayTimePortion": 0.800000011920929,
        "GameWorldTimePower": 24,
        "BaoXiangDropRatio": 1,
        "HuXIangShangHaiKaiGuan": 0,
        "ZhiBeiChongShengRatio": 1,
        "ChengZhangExpRatio": 1,
        "MJExpRatio": 1,
        "ShuLianDuExpRatio": 1,
        "NaiJiuXiShu": 1,
        "ReDuXiShu": 1,
        "CaiJiExpRatio": 1,
        "ZhiZuoExpRatio": 1,
        "ShaGuaiExpRatio": 1,
        "QiTaExpRatio": 1,
        "BeiDongYiJiShuXingRatio": 1,
        "ZhuDongYiJiShuXingRatio": 1,
        "ErJiShuXingRatio": 1,
        "MaRenBeiDongYiJiShuXingRatio": 1,
        "MaRenZhuDongYiJiShuXingRatio": 1,
        "MaRenErJiShuXingRatio": 1,
        "DongWuBeiDongYiJiShuXingRatio": 1,
        "DongWuZhuDongYiJiShuXingRatio": 1,
        "DongWuErJiShuXingRatio": 1,
        "ShiWuXiaoHaoRatio": 1,
        "ShuiXiaoHaoRatio": 1,
        "QiXiXiaoHaoRatio": 1,
        "ShengMingHuiFuRatio": 1,
        "TiLiHuiFuRatio": 1,
        "QiXiHuiFuRatio": 1,
        "DongWuDamageRatio": 1,
        "DongWuJianShangRatio": 1,
        "MaRenDamageRatio": 1,
        "ManRenJianShangRatio": 1,
        "JiaSiHuiFuRatio": 1,
        "CaiJiDamageRatio": 1,
        "ZiYuanShengMingRatio": 1,
        "RanLiaoXiaoHaoRatio": 1,
        "DongWuShengZhangRatio": 1,
        "FanZhiJianGeRatio": 1,
        "DongWuShengChanJianGeRatio": 1,
        "DongWuChanChuRatio": 1,
        "DongWuXiaoHaoShiWuRatio": 1,
        "DongWuXiaoHaoShuiRatio": 1,
        "ZuoWuFeiLiaoXiaoHaoRatio": 1,
        "ZuoWuShuiXiaoHaoRatio": 1,
        "ZuoWuXiaoHuiRatio": 1,
        "GongJiJianZhuDamageRatio": 1,
        "DongWuPinZhiRatio": 1,
        "ManRenPinZhiRatio": 1,
        "WanJiaZiYuanJinShuaBanJing": 1,
        "JianZhuZiYuanJinShuaBanJing": 1,
        "WuPinFuHuaiRatio": 1,
        "WuPinXiaoHuiTime": 1,
        "XiuLiXuYaoCaiLiaoRatio": 1,
        "XiuLiJiangNaiJiuShangXianRatio": 1,
        "RuQinKaiGuan": 1,
        "RuQinGuiMoXiShu": 1,
        "RuQinQiangDuXiShu": 1,
        "RuQinGuaiCountMin": 8,
        "RuQinGuaiCountMax": 128,
        "RuQinPerBoGuaiMin": 3,
        "RuQinPerBoGuaiMax": 16,
        "RuQinGuaiLevelXiShu": 1,
        "TanChaMinuteLimit": 20,
        "JinGongMinuteLimit": 90,
        "LengQueMinuteLimit": 1440,
        "ChongsuRatio": 1,
        "RuQinMaxChangCiCount": 2,
        "RuQinBeginHour": 0,
        "RuQinEndHour": 24,
        "RuQinShaoChengXiShu": 0.6000000238418579,
        "RuQinTuShaXiShu": 0.30000001192092896,
        "XiuMianDistance": 10000,
        "HuanXingDistance": 9000,
        "GongHuiMaxZhaoMuCount": 50,
        "GeRenMaxZhaoMuCount": 6,
        "GeRenMaxZhaoMuCount_Two": 10,
        "GeRenMaxZhaoMuCount_Three": 15,
        "XinQingZengZhang": 1,
        "XinQingJianShao": 1,
        "XiShuWeiLing": 0,
        "HuiFuChuShiBodyData": 1,
        "YouFangShangHaiKaiGuan": 0,
        "YeShengHitJianZhuShangHaiRatio": 4,
        "PVP_ShangHaiRatio_WithoutP2P_YouFang": 0,
        "WanJiaHitJianZhuShangHaiRatio": 1,
        "ShaGuaiExpShareRatio": 0.20000000298023224,
        "YunXuOtherDaKaiGongZuoTai": 0,
        "YunXuOtherDaKaiXiangZi": 0,
        "PVP_ShangHaiRatio_JinZhan": 0.4000000059604645,
        "PVP_ShangHaiRatio_YuanCheng": 0.4000000059604645,
        "GongHuiMaxDongWuCount": 50,
        "GeRenMaxDongWuCount": 10,
        "SuiJiRuQinKaiGuan": 1,
        "PanpaKaiGuan": 1,
        "WanJiaBeiXiaoRenRatio": 0.800000011920929,
        "WanJiaBeiXiaoTiRatio": 0.800000011920929,
        "KaiQiJianZhuHuiXueBuilding": 1,
        "PVP_ShangHaiRatio_PlayerToPlayer_DiFang": 1,
        "PVP_GAPVPDamageRatio": 1,
        "PlayerYouFangShangHaiKaiGuan": 1,
        "MeiTiShiWanKaiGuan": 0,
        "PVP_ShangHaiRatio_PlayerToPlayer_YouFang": 0.05999999865889549,
        "BaoXiangDiaoLuoDengJi": 0,
        "KaiQiKuaFu": 0,
        "FuHuaSpeed": 1,
        "YingHuoRanShaoSuDuRatio": 1,
        "HuDongExcludeBetweenCameraCharacter": 1,
        "PVPTimeAsiaWorkStartTime": 0,
        "PVPTimeAsiaWorkEndTime": 24,
        "PVPTimeAsiaNoWorkStartTime": 0,
        "PVPTimeAsiaNoWorkEndTime": 24,
        "PVPTimeAmericaWorkStartTime": 0,
        "PVPTimeAmericaWorkEndTime": 24,
        "PVPTimeAmericaNoWorkStartTime": 0,
        "PVPTimeAmericaNoWorkEndTime": 24,
        "PVPTimeEuropeWorkStartTime": 0,
        "PVPTimeEuropeWorkEndTime": 24,
        "PVPTimeEuropeNoWorkStartTime": 0,
        "PVPTimeEuropeNoWorkEndTime": 24,
        "WuLiYouHuaDist": 6666,
        "MovementYouHua": 1,
        "XiuMianOfflineDays": 7,
        "WanJiaShiWanKaiGuan": 0,
        "WuLiYouHuaKaiGuan": 1,
        "TiaoWuLengQueTime": 4,
        "MaxLevel": 60,
        "PVEOnlyTongGuiShuCanOpenKaiGuan": 1,
        "TeShuDaoJuDropXiShuJiaChengKaiGuan": 0,
        "JianZhuChuanSongMenPlusKaiGuan": 0,
        "FuHuoMoveSiWangBaoKaiGuan": 0
    },
    "2": {
        "ExpRatio": 1,
        "CaiJiDiaoLuoRatio": 1,
        "FaMuDiaoLuoRatio": 1,
        "CaiKuangDiaoLuoRatio": 1,
        "DongWuShiTiDiaoLuoRatio": 1,
        "DongWuShiTiZhongYaoDiaoLuoRatio": 1,
        "CaiJiShengChanJianZhuDiaoLuoRatio": 1,
        "PuTongRenDiaoLuoRatio": 1,
        "JingYingRenDiaoLuoRatio": 1,
        "BossRenDiaoLuoRatio": 1,
        "ZuoWuDropRatio": 1,
        "AddRenKeDuRatio": 1,
        "ZuoWuShengZhangRatio": 1,
        "BinSiKaiGuan": 1,
        "JianZhuFuLanMul": 1,
        "JianZhuXiuLiMul": 1,
        "JianZhuFuLanKaiGuan": 1,
        "ZhiZuoTimeRatio": 1,
        "DamageYeShengRatio": 1,
        "BeDamageByYeShengRatio": 1,
        "GameWorldDayTimePortion": 0.699999988079071,
        "GameWorldTimePower": 24,
        "BaoXiangDropRatio": 1,
        "HuXIangShangHaiKaiGuan": 0,
        "ZhiBeiChongShengRatio": 1,
        "ChengZhangExpRatio": 1,
        "MJExpRatio": 1,
        "ShuLianDuExpRatio": 1,
        "NaiJiuXiShu": 1,
        "ReDuXiShu": 1,
        "CaiJiExpRatio": 1,
        "ZhiZuoExpRatio": 1,
        "ShaGuaiExpRatio": 1,
        "QiTaExpRatio": 1,
        "BeiDongYiJiShuXingRatio": 1,
        "ZhuDongYiJiShuXingRatio": 1,
        "ErJiShuXingRatio": 1,
        "MaRenBeiDongYiJiShuXingRatio": 1,
        "MaRenZhuDongYiJiShuXingRatio": 1,
        "MaRenErJiShuXingRatio": 1,
        "DongWuBeiDongYiJiShuXingRatio": 1,
        "DongWuZhuDongYiJiShuXingRatio": 1,
        "DongWuErJiShuXingRatio": 1,
        "ShiWuXiaoHaoRatio": 1,
        "ShuiXiaoHaoRatio": 1,
        "QiXiXiaoHaoRatio": 1,
        "ShengMingHuiFuRatio": 1,
        "TiLiHuiFuRatio": 1,
        "QiXiHuiFuRatio": 1,
        "DongWuDamageRatio": 1,
        "DongWuJianShangRatio": 1,
        "MaRenDamageRatio": 1,
        "ManRenJianShangRatio": 1,
        "JiaSiHuiFuRatio": 1,
        "CaiJiDamageRatio": 1,
        "ZiYuanShengMingRatio": 1,
        "RanLiaoXiaoHaoRatio": 1,
        "DongWuShengZhangRatio": 1,
        "FanZhiJianGeRatio": 1,
        "DongWuShengChanJianGeRatio": 1,
        "DongWuChanChuRatio": 1,
        "DongWuXiaoHaoShiWuRatio": 1,
        "DongWuXiaoHaoShuiRatio": 1,
        "ZuoWuFeiLiaoXiaoHaoRatio": 1,
        "ZuoWuShuiXiaoHaoRatio": 1,
        "ZuoWuXiaoHuiRatio": 1,
        "GongJiJianZhuDamageRatio": 1,
        "DongWuPinZhiRatio": 1,
        "ManRenPinZhiRatio": 1,
        "WanJiaZiYuanJinShuaBanJing": 1,
        "JianZhuZiYuanJinShuaBanJing": 1,
        "WuPinFuHuaiRatio": 1,
        "WuPinXiaoHuiTime": 1,
        "XiuLiXuYaoCaiLiaoRatio": 1,
        "XiuLiJiangNaiJiuShangXianRatio": 1,
        "RuQinKaiGuan": 1,
        "RuQinGuiMoXiShu": 1,
        "RuQinQiangDuXiShu": 1,
        "RuQinGuaiCountMin": 8,
        "RuQinGuaiCountMax": 128,
        "RuQinPerBoGuaiMin": 3,
        "RuQinPerBoGuaiMax": 16,
        "RuQinGuaiLevelXiShu": 1,
        "TanChaMinuteLimit": 20,
        "JinGongMinuteLimit": 90,
        "LengQueMinuteLimit": 1440,
        "ChongsuRatio": 1,
        "RuQinMaxChangCiCount": 2,
        "RuQinBeginHour": 0,
        "RuQinEndHour": 24,
        "RuQinShaoChengXiShu": 0.6000000238418579,
        "RuQinTuShaXiShu": 0.30000001192092896,
        "XiuMianDistance": 10000,
        "HuanXingDistance": 9000,
        "GongHuiMaxZhaoMuCount": 50,
        "GeRenMaxZhaoMuCount": 6,
        "GeRenMaxZhaoMuCount_Two": 10,
        "GeRenMaxZhaoMuCount_Three": 15,
        "XinQingZengZhang": 1,
        "XinQingJianShao": 1,
        "XiShuWeiLing": 0,
        "HuiFuChuShiBodyData": 1,
        "YouFangShangHaiKaiGuan": 0,
        "YeShengHitJianZhuShangHaiRatio": 4,
        "PVP_ShangHaiRatio_WithoutP2P_YouFang": 0,
        "WanJiaHitJianZhuShangHaiRatio": 1,
        "ShaGuaiExpShareRatio": 0.20000000298023224,
        "YunXuOtherDaKaiGongZuoTai": 0,
        "YunXuOtherDaKaiXiangZi": 0,
        "PVP_ShangHaiRatio_JinZhan": 0.4000000059604645,
        "PVP_ShangHaiRatio_YuanCheng": 0.4000000059604645,
        "GongHuiMaxDongWuCount": 50,
        "GeRenMaxDongWuCount": 10,
        "SuiJiRuQinKaiGuan": 1,
        "PanpaKaiGuan": 1,
        "WanJiaBeiXiaoRenRatio": 0.800000011920929,
        "WanJiaBeiXiaoTiRatio": 0.800000011920929,
        "KaiQiJianZhuHuiXueBuilding": 1,
        "PVP_ShangHaiRatio_PlayerToPlayer_DiFang": 1,
        "PVP_GAPVPDamageRatio": 1,
        "PlayerYouFangShangHaiKaiGuan": 1,
        "MeiTiShiWanKaiGuan": 0,
        "PVP_ShangHaiRatio_PlayerToPlayer_YouFang": 0.05999999865889549,
        "BaoXiangDiaoLuoDengJi": 0,
        "KaiQiKuaFu": 0,
        "FuHuaSpeed": 1,
        "YingHuoRanShaoSuDuRatio": 1,
        "HuDongExcludeBetweenCameraCharacter": 1,
        "PVPTimeAsiaWorkStartTime": 0,
        "PVPTimeAsiaWorkEndTime": 24,
        "PVPTimeAsiaNoWorkStartTime": 0,
        "PVPTimeAsiaNoWorkEndTime": 24,
        "PVPTimeAmericaWorkStartTime": 0,
        "PVPTimeAmericaWorkEndTime": 24,
        "PVPTimeAmericaNoWorkStartTime": 0,
        "PVPTimeAmericaNoWorkEndTime": 24,
        "PVPTimeEuropeWorkStartTime": 0,
        "PVPTimeEuropeWorkEndTime": 24,
        "PVPTimeEuropeNoWorkStartTime": 0,
        "PVPTimeEuropeNoWorkEndTime": 24,
        "WuLiYouHuaDist": 6666,
        "MovementYouHua": 1,
        "XiuMianOfflineDays": 7,
        "WanJiaShiWanKaiGuan": 0,
        "WuLiYouHuaKaiGuan": 1,
        "TiaoWuLengQueTime": 4,
        "MaxLevel": 60,
        "PVEOnlyTongGuiShuCanOpenKaiGuan": 1,
        "TeShuDaoJuDropXiShuJiaChengKaiGuan": 0,
        "JianZhuChuanSongMenPlusKaiGuan": 0,
        "FuHuoMoveSiWangBaoKaiGuan": 0
    }
}

# Helper functions for server setup
def create_directory_structure(server_dir=DEFAULT_SERVER_DIR):
    """Create the necessary directory structure for the server."""
    try:
        saved_dir = server_dir / "WS" / "Saved"
        config_dir = saved_dir / "Config" / "WindowsServer"
        gameplay_settings_dir = saved_dir / "GamePlaySettings"

        # Create directories
        logging.info("Creating directory structure...")
        config_dir.mkdir(parents=True, exist_ok=True)
        gameplay_settings_dir.mkdir(parents=True, exist_ok=True)

        logging.info("Directory structure created.")
    except OSError as e:
        logging.error("Failed to create directory structure: %s", e)
        raise

def create_config_files(server_dir=DEFAULT_SERVER_DIR, steam_server_name="My Soulmask Server", max_players=10, pvp=False):
    """Create the necessary configuration files for the server."""
    try:
        config_dir = server_dir / "WS" / "Saved" / "Config" / "WindowsServer"
        gameplay_settings_dir = server_dir / "WS" / "Saved" / "GamePlaySettings"

        # Create Engine.ini
        engine_ini_path = config_dir / "Engine.ini"
        with open(engine_ini_path, 'w', encoding="utf8") as f:
            f.write(ENGINE_INI_CONTENT.format(SteamServerName=steam_server_name, MaxPlayers=max_players, pvp=pvp))
        logging.info("Engine.ini created at %s", engine_ini_path)

        # Create GameXishu.json
        game_xishu_json_path = gameplay_settings_dir / "GameXishu.json"
        with open(game_xishu_json_path, 'w', encoding='utf-8') as f:
            json.dump(GAME_XISHU_JSON_CONTENT, f, ensure_ascii=False, indent=4)
        logging.info("GameXishu.json created at %s", game_xishu_json_path)
    except OSError as e:
        logging.error("Failed to create config files: %s", e)
        raise

def download_steamcmd(steamcmd_dir=DEFAULT_STEAMCMD_DIR, steamcmd_url=STEAMCMD_URL):
    """Download and set up SteamCMD in the specified directory."""
    steamcmd_dir = Path(steamcmd_dir)
    steamcmd_zip_path = steamcmd_dir / "steamcmd.zip"
    
    try:
        if not steamcmd_dir.exists():
            logging.info("Creating directory: %s", steamcmd_dir)
            steamcmd_dir.mkdir(parents=True)

        # Download steamcmd.zip
        logging.info("Downloading SteamCMD from %s to %s", steamcmd_url, steamcmd_zip_path)
        with urllib.request.urlopen(steamcmd_url) as response, open(steamcmd_zip_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

        # Extract steamcmd.zip
        logging.info("Extracting SteamCMD to %s", steamcmd_dir)
        with zipfile.ZipFile(steamcmd_zip_path, 'r') as zip_ref:
            zip_ref.extractall(steamcmd_dir)

        # Clean up the zip file
        logging.info("Removing zip file: %s", steamcmd_zip_path)
        steamcmd_zip_path.unlink()
    except (URLError, HTTPError) as e:
        logging.error("Failed to download SteamCMD: %s", e)
    except zipfile.BadZipFile as e:
        logging.error("Failed to extract SteamCMD: %s", e)

def download_game_server(steamcmd_dir=DEFAULT_STEAMCMD_DIR):
    """Download and install the game server using SteamCMD."""
    steamcmd_exe = steamcmd_dir / "steamcmd.exe"
    command = f'{steamcmd_exe} +login anonymous +app_update 3017310 validate +quit'
    
    for attempt in range(3):
        try:
            logging.info("Starting game server download (attempt %d)...", attempt + 1)
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logging.info("Game server download complete.")
            logging.info("Command output:\n%s", result.stdout.decode())
            return
        except subprocess.CalledProcessError as e:
            logging.error("Attempt %d: Failed to download the game server: %s", attempt + 1, e)
            logging.error("Command output:\n%s", e.stderr.decode())
            if attempt == 2:
                raise
            logging.info("Retrying...")

# Helper function to clean up before re-running
def clean_up(server_dir=DEFAULT_SERVER_DIR):
    """Clean up previous server installations."""
    server_dir = Path(server_dir)
    if server_dir.exists():
        logging.info("Removing previous installation at: %s", server_dir)
        shutil.rmtree(server_dir)
        logging.info("Clean up complete.")

# Main function for setting up the game server
def setup_game_server(steam_server_name="My Soulmask Server", max_players=10, pvp=False):
    """Set up the game server."""
    download_steamcmd()
    download_game_server()
    create_directory_structure()
    create_config_files(steam_server_name=steam_server_name, max_players=max_players, pvp=pvp)

# GUI Code

# Load the config file
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
config_file = BASE_DIR / 'config.json'
ini_file = BASE_DIR / 'Engine.ini'
ini_file_path = DEFAULT_CONFIG_DIR / 'Engine.ini'
json_file_path = DEFAULT_GAMEPLAYSETTINGS_DIR / 'GameXishu.json'


# Function to load the configuration from the .ini file
def load_ini_config(file_path):
    if not ini_file_path.exists():
        config = {}
        with open(ini_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("Port="):
                    config['Port'] = line.split('=')[1].strip()
                elif line.startswith("SteamServerName="):
                    config['SteamServerName'] = line.split('=')[1].strip()
                elif line.startswith("MaxPlayers="):
                    config['MaxPlayers'] = line.split('=')[1].strip()
                elif line.startswith("pvp="):
                    config['pvp'] = line.split('=')[1].strip().lower() == 'true'
                elif line.startswith("backup="):
                    config['backup'] = line.split('=')[1].strip()
                elif line.startswith("saving="):
                    config['saving'] = line.split('=')[1].strip()
        return config
    else:
        config = {}
        with open(ini_file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("Port="):
                    config['Port'] = line.split('=')[1].strip()
                elif line.startswith("SteamServerName="):
                    config['SteamServerName'] = line.split('=')[1].strip()
                elif line.startswith("MaxPlayers="):
                    config['MaxPlayers'] = line.split('=')[1].strip()
                elif line.startswith("pvp="):
                    config['pvp'] = line.split('=')[1].strip().lower() == 'true'
                elif line.startswith("backup="):
                    config['backup'] = line.split('=')[1].strip()
                elif line.startswith("saving="):
                    config['saving'] = line.split('=')[1].strip()
        return config

# Function to save the updated configuration to the .ini file
def save_ini_config():
    ini_config['Port'] = port_var.get()
    ini_config['SteamServerName'] = steam_server_name_var.get()
    ini_config['MaxPlayers'] = max_players_var.get()
    ini_config['pvp'] = pvp_var.get()
    ini_config['backup'] = backup_var.get()
    ini_config['saving'] = saving_var.get()
    
    with open(ini_file_path, 'r') as file:
        lines = file.readlines()
    
    with open(ini_file_path, 'w') as file:
        for line in lines:
            if line.startswith("Port="):
                file.write(f"Port={ini_config['Port']}\n")
            elif line.startswith("SteamServerName="):
                file.write(f"SteamServerName='{ini_config['SteamServerName']}'\n")
            elif line.startswith("MaxPlayers="):
                file.write(f"MaxPlayers={ini_config['MaxPlayers']}\n")
            elif line.startswith("pvp="):
                file.write(f"pvp={'True' if ini_config['pvp'] else 'False'}\n")
            elif line.startswith("backup="):
                file.write(f"backup={ini_config['backup']}\n")
            elif line.startswith("saving="):
                file.write(f"saving={ini_config['saving']}\n")
            else:
                file.write(line)
    
    messagebox.showinfo("Success", "Configuration saved successfully")

# Load the config file
def load_config():
    if not json_file_path.exists():
        with open(config_file, 'r') as f:
            return json.load(f)
    with open(json_file_path, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(json_file_path, 'w') as f:
        json.dump(config, f, indent=4)

def update_region():
    region = region_var.get()
    if region:
        settings = config[region]
        for key in settings:
            if key in entry_vars:
                entry_vars[key].set(settings[key])
            if key in switch_vars:
                switch_vars[key].set(int(settings[key]))

def save_region_config():
    region = region_var.get()
    if region:
        for key in config[region]:
            if key in entry_vars:
                try:
                    if '.' in entry_vars[key].get():
                        config[region][key] = float(entry_vars[key].get())
                    else:
                        config[region][key] = int(entry_vars[key].get())
                except ValueError:
                    config[region][key] = entry_vars[key].get()
            if key in switch_vars:
                config[region][key] = int(switch_vars[key].get())
        save_config(config)
        messagebox.showinfo("Success", f"Region {region} configuration saved successfully.")

def start_server():
    steam_server_name = steam_server_name_var.get()
    port = port_var.get()
    password = password_var.get()
    admin_password = admin_password_var.get()
    pvp_mode = "pvp" if pvp_var.get() else "pve"

    executable_path = DEFAULT_SERVER_DIR / "WS" / "Binaries" / "Win64" / "WSServer-Win64-Shipping.exe"
    
    command = [
        str(executable_path),
        "Level01_Main",
        "-server",
        "-log",
        "-UTF8Output",
        f"-MULTIHOME=0.0.0.0",
        f"-EchoPort={port}",
        f"-forcepassthrough",
        f"-SteamServerName={steam_server_name}",
        f"-PSW={password}",
        f"-adminpsw={admin_password}",
        f"-{pvp_mode}"
    ]
    
    try:
        # Execute the command and capture output without opening a new window
        logging.info("Starting server with command: %s", " ".join(command))
        process = subprocess.Popen(
            command,
            cwd=DEFAULT_SERVER_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        def read_output(pipe):
            for line in iter(pipe.readline, ''):
                if line:
                    output_text.insert(tk.END, line)
                    output_text.see(tk.END)
            pipe.close()

        threading.Thread(target=read_output, args=(process.stdout,), daemon=True).start()
        threading.Thread(target=read_output, args=(process.stderr,), daemon=True).start()

        server_status_var.set("Running")
        server_status_label.config(foreground="green")
    except Exception as e:
        logging.error("Failed to start server: %s", e)
        messagebox.showerror("Error", f"Failed to start server: {e}")

def stop_server():
    try:
        command = ['telnet', '127.0.0.1', '18888']
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, universal_newlines=True)

        process.stdin.write('quit 15\n')
        process.stdin.flush()

        output, error = process.communicate(timeout=10)

        if process.returncode == 0:
            server_status_var.set("Stopped")
            server_status_label.config(foreground="red")
            messagebox.showinfo("Success", "Server stopped successfully.")
        else:
            logging.error("Failed to stop server: %s", error)
            messagebox.showerror("Error", f"Failed to stop server: {error}")
    except Exception as e:
        logging.error("Failed to stop server: %s", e)
        messagebox.showerror("Error", f"Failed to stop server: {e}")


def install_server():
    try:
        setup_game_server(steam_server_name_var.get(), max_players_var.get(), pvp_var.get())
        enable_gui_elements()
        messagebox.showinfo("Success", "Server installed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to install server: {e}")

def check_server_installed():
    return DEFAULT_SERVER_DIR.exists()

def disable_gui_elements():
    for widget in root.winfo_children():
        if isinstance(widget, ttk.Widget):
            if widget != install_server_button:
                widget.state(['disabled'])
    for tab in notebook.winfo_children():
        for widget in tab.winfo_children():
            if isinstance(widget, ttk.Widget):
                widget.state(['disabled'])

def enable_gui_elements():
    for widget in root.winfo_children():
        if isinstance(widget, ttk.Widget):
            widget.state(['!disabled'])
    for tab in notebook.winfo_children():
        for widget in tab.winfo_children():
            if isinstance(widget, ttk.Widget):
                widget.state(['!disabled'])

# Load initial config
config = load_config()

# Load initial ini config
ini_config = load_ini_config(ini_file)

# Define language
language = 'en'  # Change this to the desired language code

# Define switch options
switch_options = ["BinSiKaiGuan", "JianZhuFuLanKaiGuan", "HuXIangShangHaiKaiGuan", "RuQinKaiGuan", 
                  "YouFangShangHaiKaiGuan", "YunXuOtherDaKaiGongZuoTai", "YunXuOtherDaKaiXiangZi", 
                  "SuiJiRuQinKaiGuan", "PanpaKaiGuan", "KaiQiJianZhuHuiXueBuilding", 
                  "PlayerYouFangShangHaiKaiGuan", "MeiTiShiWanKaiGuan", "KaiQiKuaFu", 
                  "PVEOnlyTongGuiShuCanOpenKaiGuan", "TeShuDaoJuDropXiShuJiaChengKaiGuan", 
                  "JianZhuChuanSongMenPlusKaiGuan", "FuHuoMoveSiWangBaoKaiGuan"]

# Create main window
root = tk.Tk()
root.title("Server Management Tool")
root.geometry("1280x720")

# Create a notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Create frames for each tab
server_management_frame = ttk.Frame(notebook)
server_config_frame = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(server_management_frame, text="Server Management")
notebook.add(server_config_frame, text="Server Config")

# Create frames for server management and console output
server_management_left_frame = ttk.Frame(server_management_frame)
server_management_left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

console_output_frame = ttk.Frame(server_management_frame)
console_output_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

# Server Management Tab
# Variables for server management settings
executable_name_var = tk.StringVar(value="WSServer.exe")
map_name_var = tk.StringVar(value="Level01_Main")
steam_server_name_var = tk.StringVar(value="")
max_players_var = tk.IntVar(value=4)
password_var = tk.StringVar(value="")
admin_password_var = tk.StringVar(value="")
port_var = tk.StringVar(value=ini_config['Port'])
steam_server_name_var = tk.StringVar(value=ini_config['SteamServerName'])
max_players_var = tk.IntVar(value=ini_config['MaxPlayers'])
pvp_var = tk.BooleanVar(value=ini_config['pvp'])
backup_var = tk.StringVar(value=ini_config['backup'])
saving_var = tk.StringVar(value=ini_config['saving'])

# Place settings widgets in the left frame
ttk.Label(server_management_left_frame, text="Executable Name:").grid(row=0, column=0, padx=10, pady=10)
ttk.Entry(server_management_left_frame, textvariable=executable_name_var).grid(row=0, column=1, padx=10, pady=10)

ttk.Label(server_management_left_frame, text="Map Name:").grid(row=1, column=0, padx=10, pady=10)
ttk.Entry(server_management_left_frame, textvariable=map_name_var).grid(row=1, column=1, padx=10, pady=10)

ttk.Label(server_management_left_frame, text="Steam Server Name:").grid(row=2, column=0, padx=10, pady=10)
ttk.Entry(server_management_left_frame, textvariable=steam_server_name_var).grid(row=2, column=1, padx=10, pady=10)

ttk.Label(server_management_left_frame, text="Max Players:").grid(row=3, column=0, padx=10, pady=10)
ttk.Entry(server_management_left_frame, textvariable=max_players_var).grid(row=3, column=1, padx=10, pady=10)

ttk.Label(server_management_left_frame, text="Password:").grid(row=4, column=0, padx=10, pady=10)
ttk.Entry(server_management_left_frame, textvariable=password_var, show='*').grid(row=4, column=1, padx=10, pady=10)

ttk.Label(server_management_left_frame, text="Admin Password:").grid(row=5, column=0, padx=10, pady=10)
ttk.Entry(server_management_left_frame, textvariable=admin_password_var, show='*').grid(row=5, column=1, padx=10, pady=10)

# Create additional fields for server management settings from ini file
ttk.Label(server_management_left_frame, text="Port:").grid(row=6, column=0, padx=10, pady=10)
ttk.Entry(server_management_left_frame, textvariable=port_var).grid(row=6, column=1, padx=10, pady=10)

ttk.Label(server_management_left_frame, text="PVP:").grid(row=7, column=0, padx=10, pady=10)
ttk.Checkbutton(server_management_left_frame, variable=pvp_var, onvalue=True, offvalue=False).grid(row=7, column=1, padx=10, pady=10)

ttk.Label(server_management_left_frame, text="Backup (seconds):").grid(row=8, column=0, padx=10, pady=10)
ttk.Entry(server_management_left_frame, textvariable=backup_var).grid(row=8, column=1, padx=10, pady=10)

ttk.Label(server_management_left_frame, text="Saving (seconds):").grid(row=9, column=0, padx=10, pady=10)
ttk.Entry(server_management_left_frame, textvariable=saving_var).grid(row=9, column=1, padx=10, pady=10)

# Buttons to start and stop server
ttk.Button(server_management_left_frame, text="Start Server", command=start_server).grid(row=10, column=0, padx=10, pady=10)
ttk.Button(server_management_left_frame, text="Stop Server", command=stop_server).grid(row=10, column=1, padx=10, pady=10)

# Server status display
server_status_var = tk.StringVar(value="Stopped")
ttk.Label(server_management_left_frame, text="Server Status:").grid(row=11, column=0, padx=10, pady=10)
server_status_label = ttk.Label(server_management_left_frame, textvariable=server_status_var, foreground="red")
server_status_label.grid(row=11, column=1, padx=10, pady=10)

# Placeholder button for saving server management settings
ttk.Button(server_management_left_frame, text="Save Server Settings", command=save_ini_config).grid(row=12, column=0, columnspan=2, pady=20)

# Console Output
# Text widget for displaying output
output_text = tk.Text(console_output_frame, wrap='word', height=40, width=115)
output_text.pack(side="left", fill="both", expand=True)

# Add a scrollbar to the text widget
output_scrollbar = ttk.Scrollbar(console_output_frame, orient='vertical', command=output_text.yview)
output_scrollbar.pack(side="right", fill="y")
output_text['yscrollcommand'] = output_scrollbar.set

# Install server button
install_server_button = ttk.Button(root, text="Install Server", command=install_server)
install_server_button.pack(pady=10)

# Server Config Tab
# Create a canvas for the scrollbar in the "Server Config" tab
canvas = tk.Canvas(server_config_frame)
scrollbar = tk.Scrollbar(server_config_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Variables for region selection and settings
region_var = tk.StringVar()
entry_vars = {key: tk.StringVar() for key in translations[language].keys() if key not in switch_options}
switch_vars = {key: tk.IntVar() for key in switch_options}

# Create dropdown for region selection
ttk.Label(scrollable_frame, text="Select Region:").grid(row=0, column=0, padx=10, pady=10)
region_menu = ttk.Combobox(scrollable_frame, textvariable=region_var, values=list(config.keys()))
region_menu.grid(row=0, column=1, padx=10, pady=10)
region_menu.bind("<<ComboboxSelected>>", lambda e: update_region())

# Create frames for settings and switches side by side
settings_frame = ttk.Frame(scrollable_frame)
settings_frame.grid(row=1, column=0, padx=10, pady=10, sticky="n")

switches_frame = ttk.Frame(scrollable_frame)
switches_frame.grid(row=1, column=1, padx=10, pady=10, sticky="n")

# Create entry fields for settings using translations
row = 0
for key, label in translations[language].items():
    if key not in switch_options:
        ttk.Label(settings_frame, text=label).grid(row=row, column=0, padx=10, pady=5)
        ttk.Entry(settings_frame, textvariable=entry_vars[key]).grid(row=row, column=1, padx=10, pady=5)
        row += 1

# Create checkboxes for switch options using translations
row = 0
for key, label in translations[language].items():
    if key in switch_options:
        ttk.Label(switches_frame, text=label).grid(row=row, column=0, padx=10, pady=5)
        ttk.Checkbutton(switches_frame, variable=switch_vars[key]).grid(row=row, column=1, padx=10, pady=5)
        row += 1

# Create a frame for the fixed save button
button_frame = tk.Frame(server_config_frame)
button_frame.pack(side="bottom", fill="x")

# Save button
ttk.Button(button_frame, text="Save Region Config", command=save_region_config).pack(pady=10)

# Pack the canvas and scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Check if server is installed and enable/disable GUI accordingly
if not check_server_installed():
    disable_gui_elements()
else:
    install_server_button.pack_forget()

# Start the GUI
root.mainloop() 