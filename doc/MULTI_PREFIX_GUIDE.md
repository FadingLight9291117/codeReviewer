# 🔍 多前缀Git提交代码审查工具使用指南

## 📖 概述

多前缀Git提交代码审查工具是一个强大的AI驱动代码分析工具，能够：

- 🎯 **智能匹配**: 根据提交前缀自动识别相关代码文件
- 🤖 **AI审查**: 使用GPT-4o等先进AI模型进行代码质量分析
- 📊 **多维度分析**: 支持代码审查、错误检测、安全检查等
- 📄 **综合报告**: 生成详细的Markdown格式审查报告

## 🚀 快速开始

### 1. 基本使用

```bash
# 使用默认前缀审查最近2周的提交
python multi_prefix_review.py

# 指定特定前缀
python multi_prefix_review.py --prefixes "feat:,fix:,refactor:"

# 指定时间范围
python multi_prefix_review.py --time "1 month ago"

# 指定输出文件
python multi_prefix_review.py --output "my_review.md"
```

### 2. 在Python代码中使用

```python
from multi_prefix_review import multi_prefix_review

# 基本使用
report_file = multi_prefix_review()

# 自定义参数
report_file = multi_prefix_review(
    prefixes=["feat:", "fix:", "docs:"],
    time_range="1 week ago",
    output_file="custom_review.md"
)
```

## 📋 支持的前缀类型

| 前缀 | 描述 | 示例提交 |
|------|------|----------|
| `feat:` | 新功能开发 | `feat: 添加用户登录功能` |
| `fix:` | Bug修复 | `fix: 修复登录验证错误` |
| `refactor:` | 代码重构 | `refactor: 重构用户模块` |
| `docs:` | 文档更新 | `docs: 更新API文档` |
| `style:` | 代码格式化 | `style: 修复代码格式` |
| `test:` | 测试相关 | `test: 添加单元测试` |
| `chore:` | 杂项任务 | `chore: 更新依赖包` |

## 🔧 命令行参数

### 完整参数列表

```bash
python multi_prefix_review.py [选项]
```

| 参数 | 说明 | 示例 |
|------|------|------|
| `--help`, `-h` | 显示帮助信息 | `python multi_prefix_review.py --help` |
| `--prefixes` | 指定前缀列表（逗号分隔） | `--prefixes "feat:,fix:,docs:"` |
| `--time` | 指定时间范围 | `--time "2 weeks ago"` |
| `--output` | 指定输出文件名 | `--output "review_report.md"` |

### 时间范围格式

支持多种时间格式：
- `"1 week ago"` - 1周前
- `"2 weeks ago"` - 2周前
- `"1 month ago"` - 1月前
- `"3 days ago"` - 3天前
- `"2025-01-01"` - 具体日期

## 📊 审查类型

工具支持三种主要的AI审查类型：

### 1. 代码审查 (Code Review)
- 代码质量评分
- 最佳实践检查
- 可读性分析
- 架构建议

### 2. 错误检测 (Bug Detection)
- 潜在错误识别
- 逻辑漏洞检查
- 边界条件分析
- 异常处理审查

### 3. 安全检查 (Security Check)
- 安全漏洞扫描
- 输入验证检查
- 权限控制审查
- 敏感信息泄露检测

## 📄 报告格式

生成的Markdown报告包含以下部分：

### 1. 报告头部
- 生成时间
- 审查范围
- 匹配前缀列表

### 2. 审查概览
- 前缀统计表格
- 文件和提交计数
- 状态汇总

### 3. 详细审查结果
- 每个前缀的详细分析
- 文件列表和审查结果
- AI分析结果预览

### 4. 总结与建议
- 改进建议
- 后续行动计划

## 🎯 使用场景

### 1. 代码审查流程
```bash
# 审查最近的功能开发
python multi_prefix_review.py --prefixes "feat:" --time "1 week ago"

# 审查Bug修复质量
python multi_prefix_review.py --prefixes "fix:" --time "2 weeks ago"
```

### 2. 发布前检查
```bash
# 全面审查发布分支
python multi_prefix_review.py --prefixes "feat:,fix:,refactor:" --time "1 month ago"
```

### 3. 安全审计
```bash
# 重点关注安全相关提交
python multi_prefix_review.py --prefixes "security:,fix:" --time "3 months ago"
```

### 4. 文档质量检查
```bash
# 审查文档更新
python multi_prefix_review.py --prefixes "docs:,feat:" --time "2 weeks ago"
```

## ⚙️ 配置要求

### 1. 环境依赖
- Python 3.7+
- Git仓库环境
- 网络连接（AI服务）

### 2. 配置文件
确保存在 `config.yaml` 文件，包含AI服务配置：

```yaml
openai:
  api_key: "your-openai-api-key"
  base_url: "https://openrouter.ai/api/v1"
  model: "openai/gpt-4o"
```

### 3. 项目文件
- `ai_code_reviewer.py` - 核心审查类
- `ai_router.py` - AI路由管理
- `git_commit_analyzer.py` - Git分析工具
- `multi_prefix_review.py` - 多前缀审查工具

## 🐛 常见问题

### 1. 无匹配提交
**问题**: 提示"未找到任何匹配的提交记录"
**解决**: 
- 检查Git提交消息格式
- 调整时间范围
- 确认前缀拼写正确

### 2. AI连接失败
**问题**: AI服务连接超时
**解决**:
- 检查网络连接
- 验证API密钥
- 确认服务状态

### 3. 文件编码错误
**问题**: 文件读取编码错误
**解决**:
- 确保文件使用UTF-8编码
- 检查二进制文件过滤

## 📈 输出示例

### 终端输出
```
🔍 多前缀Git提交代码审查工具
==================================================
📝 匹配前缀: feat:, fix:
⏰ 时间范围: 1 week ago
==================================================

[1/2] 🏷️ 处理前缀: feat:
     ✅ 找到 4 个文件，3 个提交

[2/2] 🏷️ 处理前缀: fix:
     ✅ 找到 2 个文件，1 个提交

📊 审查汇总:
   📂 总计文件: 6
   📝 总计提交: 4
   🏷️ 匹配前缀: 2/2

✅ 多前缀审查报告已生成: multi_prefix_review_20250819_182904.md
```

### 报告文件预览
```markdown
# 🔍 多前缀Git提交代码审查报告

| 前缀类型 | 审查文件数 | 分析提交数 | 状态 |
|---------|-----------|-----------|------|
| `feat:` | 4 | 3 | ✅ 完成 |
| `fix:` | 2 | 1 | ✅ 完成 |

**总计**: 6 个文件，4 个提交
```

## 🔄 集成建议

### 1. CI/CD集成
```yaml
# GitHub Actions 示例
- name: Code Review
  run: |
    python multi_prefix_review.py --prefixes "feat:,fix:" --output "review.md"
    # 将报告添加到PR评论
```

### 2. 定期审查
```bash
# 每周运行的脚本
#!/bin/bash
python multi_prefix_review.py --time "1 week ago" --output "weekly_review.md"
```

### 3. 团队规范
- 统一提交前缀格式
- 定期运行审查工具
- 将报告纳入代码审查流程

---

*多前缀Git提交代码审查工具 - 让代码审查更智能、更高效！* 🚀
