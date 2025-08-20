# 🔍 智能代码审查工具 (AI Code Reviewer)

一个基于人工智能的智能代码审查工具，能够自动分析Git提交记录、进行多维度代码质量检查并生成详细的审查报告。

## 🎯 解决的实际问题

### 开发团队常见痛点
- 🔍 代码审查耗时：人工代码审查占用大量开发时间，影响项目进度
- 📊 审查质量不一：不同审查者的经验和关注点差异导致审查质量参差不齐
- ⏰ 提交记录混乱：多种提交前缀格式难以统一管理和追踪
- 🚫 遗漏关键问题：人工审查容易遗漏安全漏洞、性能问题和代码规范问题
- 📈 项目规模增长：大型项目中手动审查所有变更变得不现实
- 🔄 重复性工作：检查常见问题（如代码风格、最佳实践）的重复性工作

### 本工具的解决方案
- ⚡ 自动化审查：自动分析Git提交，大幅减少人工审查时间
- 🤖 AI智能分析：利用GPT-4o等先进AI模型，提供专业级代码审查建议
- 🏷️ 智能前缀匹配：支持多种提交前缀同时审查，统一项目管理规范
- 📋 标准化报告：生成结构化的Markdown审查报告，确保审查质量一致性
- 🔍 多维度检查：涵盖代码质量、安全性、性能、可维护性等多个维度
- 🎨 灵活配置：适应不同项目需求和团队工作流程

> **项目状态**: ✅ **功能完整，可投入使用**
> - ✅ 配置管理模块 (`config.py`)
> - ✅ AI路由模块 (`ai_router.py`) 
> - ✅ AI提示词管理模块 (`ai_prompt.py`)
> - ✅ Git提交分析模块 (`git_commit_analyzer.py`)
> - ✅ 智能代码审查器 (`ai_code_reviewer.py`)
> - ✅ 多前缀匹配审查工具 (`multi_prefix_review.py`)
> - ✅ 完整的使用示例和文档

## 📋 目录

- [最新功能](#最新功能)
- [功能特性](#功能特性)
- [技术栈](#技术栈)
- [快速开始](#快速开始)
- [多前缀审查工具](#多前缀审查工具)
- [使用指南](#使用指南)
- [配置说明](#配置说明)
- [API文档](#API文档)
- [示例演示](#示例演示)
- [项目结构](#项目结构)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## ✨ 功能特性

### 🎯 核心功能
- 🤖 **AI驱动的智能分析**: 使用GPT-4o等先进AI模型进行代码审查
- � **Git集成**: 深度集成Git提交历史，智能识别需要审查的文件
- 🏷️ **多前缀匹配**: 同时支持多种提交前缀（feat:, fix:, refactor:, docs:等）
- 📁 **项目路径指定**: 支持指定不同项目路径进行审查
- 🔍 **多维度分析**: 代码质量、错误检测、安全检查、性能分析
- � **智能报告**: 自动生成结构化Markdown格式审查报告

### 🛠️ 技术特性
- ⚙️ **灵活配置**: YAML配置文件管理API密钥和模型设置
- 🔧 **模块化设计**: 清晰的模块划分，易于扩展和维护
- 🌐 **多模型支持**: 通过OpenRouter支持多种AI模型
- 📝 **命令行工具**: 支持命令行参数和交互式使用
- 🎨 **用户友好**: 详细的进度显示和错误处理
- 🚀 **高性能**: 并行处理和智能缓存机制

## 🛠 技术栈

- **Python 3.8+**: 主要开发语言
- **OpenAI API**: AI模型接口
- **OpenRouter**: AI模型路由服务  
- **Git**: 版本控制和提交历史分析
- **PyYAML**: 配置文件管理
- **typing**: 完整的类型注解支持

## � 快速开始

### 环境要求

- Python 3.8 或更高版本
- Git 仓库环境
- 网络连接（用于AI服务）

### 1. 克隆项目

```bash
git clone https://github.com/FadingLight9291117/codeReviewer.git
cd codeReviewer
```

### 2. 安装依赖

```bash
pip install openai pyyaml
```

### 3. 配置API密钥

创建 `config.yaml` 文件：
```yaml
openai:
  api_key: "your-openrouter-api-key"
  base_url: "https://openrouter.ai/api/v1"
  model: "openai/gpt-4o"
```

### 4. 立即开始使用

```bash
# 快速审查当前项目
python multi_prefix_review.py

# 指定前缀和时间范围
python multi_prefix_review.py --prefixes "feat:,fix:" --time "1 week ago"

# 指定项目路径
python multi_prefix_review.py --project "/path/to/your/project"

# 查看帮助
python multi_prefix_review.py --help
```

## 🏷️ 多前缀审查工具

### 基本使用

```bash
# 使用默认设置审查（常用前缀，最近2周）
python multi_prefix_review.py

# 自定义前缀
python multi_prefix_review.py --prefixes "feat:,fix:,refactor:,docs:"

# 指定时间范围
python multi_prefix_review.py --time "1 month ago"

# 指定输出文件
python multi_prefix_review.py --output "my_review_report.md"

# 指定项目路径
python multi_prefix_review.py --project "C:\Projects\MyApp"

# 组合使用
python multi_prefix_review.py --project "/path/to/project" --prefixes "feat:,fix:" --time "2 weeks ago" --output "custom_report.md"
```

### 支持的前缀类型

| 前缀 | 描述 | 示例提交消息 |
|------|------|-------------|
| `feat:` | 新功能开发 | `feat: 添加用户登录功能` |
| `fix:` | Bug修复 | `fix: 修复登录验证错误` |
| `refactor:` | 代码重构 | `refactor: 重构用户模块结构` |
| `docs:` | 文档更新 | `docs: 更新API使用文档` |
| `style:` | 代码格式化 | `style: 修复代码格式问题` |
| `test:` | 测试相关 | `test: 添加用户模块单元测试` |
| `chore:` | 杂项任务 | `chore: 更新项目依赖包` |
| `perf:` | 性能优化 | `perf: 优化数据库查询性能` |

### 审查类型

工具提供三种核心审查类型：

1. **代码审查 (Code Review)**: 代码质量评分、最佳实践、可读性分析
2. **错误检测 (Bug Detection)**: 潜在错误、逻辑漏洞、边界条件检查  
3. **安全检查 (Security Check)**: 安全漏洞、输入验证、权限控制审查

### Python API 使用

```python
from multi_prefix_review import multi_prefix_review

# 基本使用
report_file = multi_prefix_review()

# 自定义参数
report_file = multi_prefix_review(
    prefixes=["feat:", "fix:", "security:"],
    time_range="2 weeks ago", 
    output_file="security_review.md",
    project_path="/path/to/project"
)

print(f"审查报告已生成: {report_file}")
```

## 🚀 使用指南

### 智能代码审查器 (ai_code_reviewer.py)

```bash
# 演示模式
python ai_code_reviewer.py demo

# 交互式模式  
python ai_code_reviewer.py

# 指定配置文件
python ai_code_reviewer.py --config custom_config.yaml
```

### 示例脚本

```bash
# 运行核心功能教程
python examples/core_review_tutorial.py

# 运行多前缀功能展示
python examples/multi_prefix_showcase.py

# 运行系统验证
python examples/system_validator.py
```

### 在Python代码中使用

```python
from ai_code_reviewer import SmartCodeReviewer

# 初始化审查器
reviewer = SmartCodeReviewer(repo_path=".", config_path="config.yaml")

# 按提交前缀审查
result = reviewer.review_by_commit_prefix(
    prefix="feat:", 
    since="1 week ago",
    review_types=['code_review', 'bug_detection', 'security_check']
)

# 审查最近变更
result = reviewer.review_recent_changes(days=3)

# 审查指定文件
result = reviewer.review_files(["ai_code_reviewer.py", "config.py"], "自定义审查")

# 生成Markdown报告
markdown_report = reviewer.generate_markdown_report(result)
with open('review_report.md', 'w', encoding='utf-8') as f:
    f.write(markdown_report)
```
code = "your_code_here"
bug_prompt = create_bug_detection_prompt(code, "python")

# 或使用管理器进行更复杂的操作
manager = AIPromptManager()
available_templates = manager.get_available_templates()
print(f"可用模板: {available_templates}")
```

#### 自定义审查配置
```python
from config import ConfigManager, AIClient

# 加载配置
config_manager = ConfigManager("config.yaml")
ai_client = AIClient(config_manager)

# 创建自定义审查请求
messages = [{"role": "user", "content": "审查这段代码..."}]
response = ai_client.create_chat_completion(messages)
```

## ⚙️ 配置说明

### 基本配置文件 (config.yaml)

```yaml
openai:
  api_key: "your-openrouter-api-key"
  base_url: "https://openrouter.ai/api/v1"  
  model: "openai/gpt-4o"
```

### 配置参数说明

| 参数 | 描述 | 必需 | 默认值 |
|------|------|------|--------|
| `api_key` | OpenRouter API密钥 | ✅ | - |
| `base_url` | API端点地址 | ❌ | `https://openrouter.ai/api/v1` |
| `model` | AI模型名称 | ❌ | `openai/gpt-4o` |

### 支持的AI模型

- `openai/gpt-4o` - OpenAI GPT-4 Omni
- `openai/gpt-4-turbo` - OpenAI GPT-4 Turbo
- `anthropic/claude-3-sonnet` - Anthropic Claude 3 Sonnet
- `meta-llama/llama-3-70b-instruct` - Meta Llama 3 70B
- 更多模型请查看 [OpenRouter 文档](https://openrouter.ai/docs)

### 环境变量 (可选)

```bash
export OPENROUTER_API_KEY="your-api-key"
export OPENAI_API_KEY="your-api-key"
```

## 📚 API文档

### 核心模块

#### SmartCodeReviewer (ai_code_reviewer.py)
```python
class SmartCodeReviewer:
    def __init__(self, repo_path=".", config_path="config.yaml")
    
    def review_by_commit_prefix(self, prefix, since="1 week ago", review_types=None)
    def review_recent_changes(self, days=7, review_types=None)  
    def review_files(self, files, description="文件审查")
    def generate_markdown_report(self, review_result)
    def export_review_report(self, review_result, output_file=None)
```

#### AIRouter (ai_router.py)
```python
class AIRouter:
    def __init__(self, config_path="config.yaml")
    
    def chat(self, message, use_history=True)
    def create_completion(self, messages, model=None)
    def test_connection(self)
    def switch_model(self, model_name)
    def get_available_models(self)
```

#### GitAnalyzer (git_commit_analyzer.py)
```python
class GitAnalyzer:
    def __init__(self, repo_path=".")
    
    def get_commits_by_prefix(self, prefix, since="1 week ago")
    def get_recent_changed_files(self, days=7)
    def analyze_files_by_commits(self, commits)
    def get_file_changes(self, file_path, since="1 week ago")
```

#### AIPromptManager (ai_prompt.py)
```python
class AIPromptManager:
    def get_prompt(self, template_name, **kwargs)
    def get_available_templates(self)
    def add_custom_template(self, name, template, required_params)
    def get_review_prompt(self, code, language, review_type)
```

### 多前缀审查工具

#### multi_prefix_review()
```python
def multi_prefix_review(
    prefixes=None,           # 前缀列表，默认常用前缀
    time_range="2 weeks ago", # 时间范围
    output_file=None,        # 输出文件名
    project_path=None        # 项目路径，默认当前目录
) -> str                     # 返回生成的报告文件路径
```

### 预定义审查类型

- `code_review`: 代码质量和最佳实践审查
- `bug_detection`: 潜在错误和问题检测
- `security_check`: 安全漏洞和风险评估
- `performance_analysis`: 性能优化分析
- `documentation_review`: 文档质量审查
- `architecture_analysis`: 架构设计分析
  - `get_available_models()`: 获取可用模型列表

## 🎭 示例演示

### 命令行演示

```bash
# 基本多前缀审查
python multi_prefix_review.py
# 输出: 
# 🔍 多前缀Git提交代码审查工具
# 📝 匹配前缀: feat:, fix:, refactor:, docs:, style:, test:, chore:
# ⏰ 时间范围: 2 weeks ago
# ✅ 多前缀审查报告已生成: multi_prefix_review_20250820_143022.md

# 指定项目路径审查
python multi_prefix_review.py --project "C:\Projects\MyApp" --prefixes "feat:,fix:"
# 输出:
# 📁 项目路径: C:\Projects\MyApp
# 📝 匹配前缀: feat:, fix:
# [1/2] 🏷️ 处理前缀: feat:
#      ✅ 找到 8 个文件，5 个提交
# [2/2] 🏷️ 处理前缀: fix:  
#      ✅ 找到 3 个文件，2 个提交
```

### 生成的报告示例

```markdown
# 🔍 多前缀Git提交代码审查报告

**生成时间**: 2025-08-20 14:30:22
**项目路径**: /path/to/project
**审查范围**: 最近2周的提交记录
**匹配前缀**: feat:, fix:

## 📊 审查概览

| 前缀类型 | 审查文件数 | 分析提交数 | 状态 |
|---------|-----------|-----------|------|
| `feat:` | 8 | 5 | ✅ 完成 |
| `fix:` | 3 | 2 | ✅ 完成 |

**总计**: 11 个文件，7 个提交

## 🏷️ feat: 相关提交审查

### 📋 基本信息
- **审查文件数**: 8
- **分析提交数**: 5

### 🔍 审查结果详情

#### 📄 ai_code_reviewer.py
**Code Review**: 代码质量评分 8/10，建议优化异常处理...
**Bug Detection**: 发现1个潜在的空指针异常...
**Security Check**: 未发现安全漏洞...
```

### 完整功能演示

```bash
# 运行完整功能展示脚本
python examples/multi_prefix_showcase.py

# 展示包含：
# 🎯 展示1: 基本多前缀审查
# 🎯 展示2: 自定义前缀审查  
# 🎯 展示3: 指定项目路径审查
# 🎯 展示4: 不同时间范围审查
# 🎯 展示5: 综合代码审查
# 🎯 展示6: 错误处理展示
```

## 📁 项目结构

```
codeReviewer/
├── 📄 ai_code_reviewer.py        # 智能代码审查器核心类 (原main.py)
├── 🤖 ai_router.py              # AI模型路由管理
├── 💬 ai_prompt.py              # AI提示词模板管理  
├── 📊 git_commit_analyzer.py    # Git提交分析工具
├── ⚙️ config.py                # 配置管理
├── 🎯 multi_prefix_review.py    # 多前缀审查工具
├── � examples/                 # 示例和演示文件夹
│   ├── �📚 examples.py           # 使用示例集合
│   ├── 🎭 demo_multi_prefix.py  # 多前缀功能演示
│   └── 🧪 quick_test.py         # 快速功能测试
├── 🔄 rename_main.py            # 文件重命名工具
├── 📖 readme.md                 # 项目文档
├── 📋 MULTI_PREFIX_GUIDE.md     # 多前缀工具使用指南
├── 📊 INTEGRATION_REPORT.md     # 集成完成报告
├── ⚙️ config.yaml              # 配置文件
├── 📝 config_template.yaml      # 配置模板
└── 📄 生成的报告文件/
    ├── multi_prefix_review_*.md  # 多前缀审查报告
    ├── code_review_report.md     # 单次审查报告  
    └── comprehensive_review.md   # 综合审查报告
```

### 核心文件说明

| 文件 | 功能 | 状态 |
|------|------|------|
| `ai_code_reviewer.py` | 智能代码审查器，集成所有功能模块 | ✅ 完成 |
| `multi_prefix_review.py` | 多前缀匹配Git提交审查工具 | ✅ 完成 |
| `ai_router.py` | AI模型路由、切换、测试管理 | ✅ 完成 |
| `ai_prompt.py` | AI提示词模板和构建器 | ✅ 完成 |
| `git_commit_analyzer.py` | Git提交历史分析和文件发现 | ✅ 完成 |
| `config.py` | 配置文件管理和AI客户端封装 | ✅ 完成 |

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 此仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

### 开发规范

- 遵循 PEP 8 代码风格
- 添加适当的类型注解和文档字符串
- 编写单元测试覆盖新功能
- 确保代码通过所有现有测试
- 更新相关文档

### 贡献领域

- 🐛 Bug修复和问题报告
- ✨ 新功能开发
- 📚 文档改进
- 🧪 测试用例补充
- 🎨 用户体验优化
- 🌐 多语言支持

## 🔧 常见问题

### Q: 如何获取OpenRouter API密钥？
A: 访问 [OpenRouter](https://openrouter.ai/) 注册账户并获取API密钥。

### Q: 支持哪些编程语言的代码审查？
A: 支持大多数主流编程语言，包括Python、JavaScript、Java、C++、Go等。

### Q: 可以在没有网络的环境中使用吗？
A: 不可以，工具需要连接AI服务进行代码分析。

### Q: 如何审查私有仓库？
A: 工具在本地运行，只需要本地Git仓库访问权限，不会上传代码到外部服务。

### Q: 生成的报告可以自定义格式吗？
A: 目前支持Markdown格式，可以通过修改模板自定义报告样式。

## 🐛 问题报告

如果您发现任何问题，请通过 [Issues](https://github.com/FadingLight9291117/codeReviewer/issues) 页面报告。

请包含以下信息：
- 操作系统和Python版本
- 错误信息和堆栈跟踪
- 重现步骤和预期行为
- 项目环境信息

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🌟 特别感谢

- 🤖 **OpenAI** - 提供强大的GPT模型
- 🌐 **OpenRouter** - 提供便捷的AI模型路由服务  
- 📊 **Git** - 强大的版本控制系统
- 🐍 **Python社区** - 丰富的生态系统支持
- 👥 **所有贡献者** - 宝贵的建议和代码贡献

## 📞 联系方式

- 🏠 **项目主页**: [https://github.com/FadingLight9291117/codeReviewer](https://github.com/FadingLight9291117/codeReviewer)
- 🐛 **问题反馈**: [Issues](https://github.com/FadingLight9291117/codeReviewer/issues)
- 💬 **讨论交流**: [Discussions](https://github.com/FadingLight9291117/codeReviewer/discussions)

---

<div align="center">

### 🎯 让AI为你的代码质量保驾护航！

**⭐ 如果这个项目对您有帮助，请给我们一个星标！**

[![Stars](https://img.shields.io/github/stars/FadingLight9291117/codeReviewer?style=social)](https://github.com/FadingLight9291117/codeReviewer)
[![Forks](https://img.shields.io/github/forks/FadingLight9291117/codeReviewer?style=social)](https://github.com/FadingLight9291117/codeReviewer)
[![Issues](https://img.shields.io/github/issues/FadingLight9291117/codeReviewer)](https://github.com/FadingLight9291117/codeReviewer/issues)

</div>