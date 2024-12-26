from PyInstaller import __main__ as pyi

# 打包快捷设置,避免手动输入命令
params = [
    "-F",  #  是否单文件
    # "-w",  # 是否隐藏控制台-w代表无,默认有
    "--hidden-import=nanoid",
    "--hidden-import=fastapi.templating",
    # 额外目录纳入打包
    "--add-data=router;router",
    "--add-data=util;util",
    "--add-data=tasks;tasks",
    # 指定输出目录
    "--distpath=build",
    # 无需用户确认
    "--noconfirm",
    # 输出的名字
    "-n=lga",
    # 启动文件
    "main.py",
]
pyi.run(params)
