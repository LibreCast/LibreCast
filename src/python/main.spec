# -*- mode: python -*-
a = Analysis(['main.pyw'],
             pathex=['/Users/jrg/Desktop/LibreCast/src/python'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='LibreCast',
          debug=False,
          strip=None,
          upx=True,
          console=False)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='LibreCast')
