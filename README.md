# Picturebook-to-Animation V0.1

当前交付为本地验证、面向云端迁移的 V0.1，不是已部署的 Work 云端服务。测试图由脚本原创绘制，30 秒、640×360、24fps、无声；第一镜头缓慢推近，第二镜头透明前景轻微横移。2.5D 是手工分层视差，不是自动分割或三维重建。

## 运行
Python 3.9+，新建虚拟环境后 `pip install -r requirements.txt`。
首次原创测试：`python scripts/pipeline.py demo`。
继续：`python scripts/pipeline.py render`。
重做：`python scripts/pipeline.py render --shot S01 --redo`，之后全量 render 再生成成片。
输出 renders/preview.mp4；state.json 按镜头及素材内容摘要跳过已完成镜头，单镜头临时文件完成后原子替换。中断后重复 render。不要同时启动两个渲染进程。

## 配置和审核
storyboard.json 为实际镜头 manifest：version、rights、shots。每镜头 id 仅用字母数字，duration 秒，mode=pan/layers，source 相对路径，layers 另需 foreground 透明 PNG，review=draft/approved/changes_requested。先审核故事、时长、裁切与分层，再设 approved。源图不可覆写。发布审批需另记审核人、时间与意见，rendered 不等于获准发布。
默认仅支持无声硬切；配音、字幕、音效、自动分层、精确镜头编辑 UI 不在 V0.1 内。原画像素不经生成模型改画，但运镜会裁切，需人工检查。

## 首本真实绘本导入入口
将授权文件与逐页 PNG/JPEG 放入 import/，填写 intake.json。必须明确改编、云端存储、公开传播的地域、平台、有效期及音频授权；只有购买凭证不足以确认改编权。当前没有真实绘本或授权，禁止开始真实书制作。由审核者检查凭据后，才可填写 storyboard 的 rights；不能通过把布尔值改为 true 代替授权审核。视频生成服务上传权限默认关闭。

## 公司/家中接力
代码仓库：https://github.com/zhaochendaxingxing/Picturebook-to-Animation （Private）。
素材库：https://drive.google.com/drive/folders/1j3u-EwRuQbBaWwxWpaU6gidLgbjc1xFg 。已验证读取和上传，跨设备下载未验证。
开工前拉取同一个 Git 提交，从 Drive 下载匹配的 assets/、renders/ 和 state.json。一次只运行一个制作进程。收工先上传素材及输出，再保存检查点：Git 提交号、素材 SHA256、state.json、审核人及审核意见。确认上传完成后才能换设备。新设备读取最后完成的检查点再运行 render。令牌仅存执行环境秘密配置，不进入 Git 或网盘包。
真实绘本及授权文件不提交代码库。大文件保存在私有 Drive，当前尚未实现自动同步，也尚未部署 Linux 云端节点。

## 即梦独立适配器与验证矩阵
运行 `python adapters/jimeng.py` 仅报告环境，不提交网络任务。
官方公开页面：https://jimeng.jianying.com/ai-tool/business ，列出 @jimeng/canvas-cli 安装入口。不同公开渠道命名不一致，未确认包身份前不安装。不得执行 curl | bash 或未经审查脚本。
当前主机 macOS ARM64；docker/node/npm/dreamina-canvas 均不存在，因此 Linux 安装、版本、无界面登录、任务提交、下载均未验证。生成被用户禁用付费调用约束阻止，不应通过“免费额度”猜测绕过。后续先获取官方包与校验信息、审查安装行为，在隔离 Linux 环境安装，读取实际 help/schema/version；按官方设备授权流程由用户登录，秘密不得写日志。仅做无费用状态查询。生成与下载端到端验证需另有明确允许免费测试的条件，当前不执行。适配器为禁用边界桩，尚非可用生成器。

补充实测：官方 install.sh 已成功只下载并初步检查，包含 Linux 平台分发逻辑；完整审查尚未完成，未执行。该文件的存在不能证明 Linux 安装及登录可用。测试记录见 TEST-RESULTS.txt。Skill 已打包在本目录，尚未安装到用户全局技能目录。


## 2026-11-10 云端连接进展
GitHub 私有空仓库及 push 权限已由连接器验证，正在初始化 V0.1。Drive 原创样片和完整备份包已上传。Linux 执行和即梦端到端仍未验证。
