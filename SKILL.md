---
name: picturebook-to-animation
description: 将已授权绘本制作成30–60秒原画运镜或手工分层2.5D动画，管理分镜审核、断点续作和独立镜头重做。
---
先读 README.md。真实绘本必须检查 import/intake.json 的授权凭据与素材清单；购买图书不等于取得改编授权。缺资料时停在导入阶段。禁止将绘本上传生成服务，禁止付费调用。
用 storyboard.json 管理镜头；只渲染 approved 镜头。保留原图，分层必须由获授权素材提供透明前景与完整背景；不自动补画。改变构图与遮挡需用户审核。
运行 scripts/pipeline.py render；指定 --shot S01 --redo 独立重做，最终全量 render 检查后合成。state.json 是缓存，不代替审批记录。发布前人工检查原画一致性、裁切、透明边缘、节奏及授权。
适配器见 adapters/jimeng.py；未核实官方命令和无界面认证前不启用生成。跨设备持久化按 README.md 执行，不把聊天记录当项目数据库。
