"""独立、默认关闭的即梦适配器；不猜测登录或生成命令。"""
import json,platform,shutil
print(json.dumps({'platform':platform.platform(),'binary':shutil.which('dreamina-canvas'),'install':'not_verified','version':'not_verified','headless_login':'not_verified','generate':'disabled_no_paid_calls','download':'not_verified'},indent=2))
