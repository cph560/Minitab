# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['Boxplot','DataStatus','designer','Equation','GUI_Dialog_New','GUI_Plot_Window_General','GUI_Plot_Window_Histogram_Setting','GUI_Plot_Window_Scatter','GUI_Plot_Window_Scatter_Setting','GUI_Plot_Window_Time_Series_Setting','GUI_Window_Result','GUI_Window_Statistics','Individual','mytablewidget','Pareto','Plot_interface','Plot_Window_General','Plot_Window_Histogram','Plot_Window_Scatter','Plot_Window_Time_Series','Probaplot','Random'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=True,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [('v', None, 'OPTION')],
    exclude_binaries=True,
    name='main',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
