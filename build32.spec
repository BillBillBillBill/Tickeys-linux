# -*- mode: python -*-
# coding: utf-8
block_cipher = None

a = Analysis(
    ['./tickeys/run.py'],
    pathex=['./tickeys'],
    binaries=[
        ('lib/32/libmodplug.so.1',"."),
        ('lib/32/libSDL2_ttf-2.0.so.0',"."),
        ('lib/32/libSDL2_image-2.0.so.0',"."),
        ('lib/32/libSDL2_mixer-2.0.so.0',"."),
        ('lib/32/libSDL2-2.0.so.0',"."),
        ('lib/32/libsndio.so.6.0',"."),
        ], # 动态库
    datas=[("./tickeys/tickeys.png",".")], # 数据文件，可以是任意文件类型，例如ini配置文件、字体文件、图片等
    hiddenimports=['six','packaging', 'packaging.version', 'packaging.specifiers'],
    hookspath=None,
    runtime_hooks=None,
    excludes=None,
    win_no_prefer_redirects=None,
    win_private_assemblies=None,
    cipher=block_cipher)
a.datas += Tree("./tickeys/Resources", prefix = "Resources")
a.datas += Tree("./tickeys/kivy", prefix = "kivy")
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Tickeys',
          debug=False,
          strip=None,
          upx=True,
          console=True
          )
