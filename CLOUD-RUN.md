# Linux 云端测试入口

仓库 Actions → Linux original-art demo → Run workflow。
只手动触发，不随提交自动运行；不调用即梦，不读取真实绘本，不需要 Drive 密钥。
GitHub Actions 私有仓库可能计入运行额度：先在 GitHub 账单设置检查剩余额度与预算，确认不产生费用后再运行。当前未检查账单，也未启动任务。
成功后在运行页 Artifacts 下载 original-demo-checkpoint，内含成片及 checkpoint.zip。Artifact 保留7天，应及时转存私有 Drive。

本地/云端保存：`python scripts/checkpoint.py save checkpoint.zip`。
新设备检出相同代码，安装 requirements.txt，在没有 state.json 的新工作目录执行 `python scripts/checkpoint.py restore /absolute/path/checkpoint.zip`，再运行 `python scripts/pipeline.py render`。
检查点包含素材、分镜、状态、镜头及成片和 SHA256；不包含授权书与凭据。真实绘本只有获得云端存储授权后才能上传检查点。只从可信项目接收检查点；不并行制作同一项目。

当前 checkpoint 上传 Drive 仍由会话工具执行；GitHub Actions 不自动连接用户 Drive。跨设备人工交接可用，后台自动同步未实现。GitHub Actions 是测试执行器，不代表 Work 云端环境已部署。
