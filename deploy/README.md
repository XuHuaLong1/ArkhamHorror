# Arkham Horror — 中文本地化补丁层

把 Arkham Horror 网页版里**未中文化的英文 UI 按钮/菜单**补成中文，做成一层可复现的 Docker 镜像补丁，**不改动上游任何源码**。

## 为什么会有英文按钮
前端有两处英文来源：
1. **主翻译 chunk**：官方中文 `zh-P5ZxcOoo.js` 比英文少约 2,815 个 key，缺失的 key 会回退显示英文。
2. **组件内联默认翻译**：`create-Cemunwmn.js`（新建游戏/战役页面）把 `create` 命名空间的英文默认值直接内联在组件里；当 i18next 没加载到对应中文键时，页面就显示这些英文。

本补丁覆盖这两处里**界面控件类（约 318 条）**最显眼的英文文本；战役剧情、场景/卡牌专有名词按约定暂保留英文。

## 本目录内容
| 文件 | 作用 |
|------|------|
| `zh_patch.mjs` | **主翻译源**：扁平 `key: 中文` 共 253 条，用于修补 `zh-P5ZxcOoo.js`。保留 i18next 占位符 `{name}`、`@:{slot}`、`{'{'}curse{'}'}` 及 `<br>`/`|` 结构。 |
| `apply_patch.mjs` | 注入脚本：把 `zh_patch.mjs` 深合并进官方 zh chunk，并可选修正 `index.html` 的 `lang`。 |
| `patch_create_component.py` | 组件补丁脚本：把 `create-Cemunwmn.js` 内联的 62 条英文 UI 默认值改为中文。 |
| `Dockerfile` | 多阶段构建：依次注入 zh chunk、修补 create 组件、覆盖进官方镜像并改 `lang="zh"`。 |

> 仓库**不提交**任何 `.js` bundle 编译产物，镜像构建时才生成修补后的 chunk。

## 本地构建镜像
```bash
docker build -t arkham-horror-zh:latest ./deploy
docker run -p 3000:3000 arkham-horror-zh:latest
```

## 接入现有 docker compose
把 compose 里 web 服务的 `image:` 改为 `arkham-horror-zh:latest`（已改好），然后：
```bash
docker compose up -d
```

## 只想要修补后的 chunk（不重建镜像）
```bash
# 1. 取出官方 chunk
docker run --rm --entrypoint cat halogenandtoast/arkham-horror:latest \
  /opt/arkham/src/frontend/dist/assets/zh-P5ZxcOoo.js > out/zh-P5ZxcOoo.js
docker run --rm --entrypoint cat halogenandtoast/arkham-horror:latest \
  /opt/arkham/src/frontend/dist/assets/create-Cemunwmn.js > out/create-Cemunwmn.js

# 2. 本地注入
AH_SRC=out/zh-P5ZxcOoo.js AH_OUT=out/zh-P5ZxcOoo.patched.js \
  node deploy/apply_patch.mjs
python3 deploy/patch_create_component.py out/create-Cemunwmn.js out/create-Cemunwmn.patched.js
```

## 如何增删翻译
- 改 `zh_patch.mjs` → 影响全局 UI（主页、牌组、战役日志等）。
- 改 `patch_create_component.py` 里的 `zh` 字典 → 影响新建游戏/战役页面。

重新 `docker build` 即可生效，无需触碰源码。

## 当前状态
- 镜像 `arkham-horror-zh:latest` 已构建并运行。
- `docker-compose.yml` 已改为使用 `arkham-horror-zh:latest`。
- 本地服务已验证 HTTP 200，`create` 页面“高级规则配置/预设/第一章规则”等已显示中文。
