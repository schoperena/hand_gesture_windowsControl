# main.spec
# Archivo generado para empaquetar main.py con mediapipe y opencv

import os
import mediapipe as mp
from PyInstaller.utils.hooks import collect_submodules

mp_models = os.path.join(os.path.dirname(mp.__file__), "modules")

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[(mp_models, "mediapipe/modules")],
    hiddenimports=collect_submodules('mediapipe'),
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='hand_ges_control',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GestosWindows',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=None  # aquí podrías incluir un icono .ico si deseas
)
