from DrissionPage import Chromium
from DrissionPage._configs.chromium_options import ChromiumOptions
from util.system import  Env
class Config:
    type = 'interval'
    seconds = 5
    task_name='任务1'
url = "https://juejin.cn/user/center/signin?from=main_page"
def main():
    print('hello')
    # 启动或接管浏览器，并创建标签页对象
    # co = ChromiumOptions().headless()

    # tab = Chromium(9224,co).latest_tab
    # # 跳转到目标页面
    # tab.get(url)
    
