from DrissionPage import Chromium
from DrissionPage._configs.chromium_options import ChromiumOptions

type = 'delay'
task_name='hello2'
    
url = "https://juejin.cn/user/center/signin?from=main_page"
def main():
    print('hello2')
    # 启动或接管浏览器，并创建标签页对象
    # co = ChromiumOptions()
    # Chromium = Chromium(9223,co)
    # tab = Chromium.latest_tab
    # # 跳转到目标页面
    # tab.get(url)
    # Chromium.quit()
    
