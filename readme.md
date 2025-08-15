# 智能代码审查工具 (AI Code Reviewer)

一个基于人工智能的代码审查工具，能够自动分析代码质量、发现潜在问题并提供改进建议。

> **项目状态**: 🚧 开发中
> - ✅ 配置管理模块 (`main.py`, `config.yaml`)
> - ✅ AI提示词管理模块 (`ai_prompt.py`)
> - 🔄 代码读取模块 (`code_reader.py`) - 待实现
> - 🔄 文件搜索模块 (`code_file_search.py`) - 待实现  
> - 🔄 AI路由模块 (`ai_router.py`) - 待实现

## 📋 目录

- [功能特性](#功能特性)
- [技术栈](#技术栈)
- [安装方法](#安装方法)
- [使用指南](#使用指南)
- [配置说明](#配置说明)
- [API文档](#API文档)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## ✨ 功能特性

- 🤖 **AI驱动的代码分析**: 使用先进的AI模型进行智能代码审查
- 🔍 **多种审查类型**: 支持代码质量、Bug检测、性能分析、安全检查等7种审查模式
- 📋 **智能提示词**: 预定义专业的提示词模板，确保审查质量
- ⚙️ **YAML配置管理**: 通过配置文件轻松管理API密钥和模型设置
- 🔧 **模块化设计**: 清晰的模块划分，易于扩展和维护
- �️ **类型安全**: 完整的类型注解，提高代码可靠性
- 🌐 **多模型支持**: 通过OpenRouter支持多种AI模型

## 🛠 技术栈

- **Python 3.8+**: 主要开发语言
- **OpenAI API**: AI模型接口
- **OpenRouter**: AI模型路由服务
- **PyYAML**: 配置文件管理
- **typing**: 类型注解支持

## 📦 安装方法

### 环境要求

- Python 3.8 或更高版本
- pip 包管理器

### 克隆项目

```bash
git clone https://github.com/your-username/codeReviewer.git
cd codeReviewer
```

### 安装依赖

```bash
pip install -r requirements.txt
```

如果没有 `requirements.txt` 文件，请安装以下依赖：

```bash
pip install openai pyyaml
```

## 🚀 使用指南

### 基本使用

1. **配置API密钥**
   
   创建 `config.yaml` 文件：
   ```yaml
   config:
     openai:
       base_url: https://openrouter.ai/api/v1
       api_key: your-api-key-here
       model: "openai/gpt-4o"
       organization: your-org
   ```

2. **运行主程序**
   ```bash
   python main.py
   ```

3. **代码审查流程**
   - 确保配置文件正确设置
   - 运行程序开始分析
   - 查看AI生成的审查结果

### 高级用法

#### 使用不同的审查模板
```python
from ai_prompt import AIPromptManager, create_bug_detection_prompt

# 使用预定义的Bug检测模板
code = "your_code_here"
bug_prompt = create_bug_detection_prompt(code, "python")

# 或使用管理器进行更复杂的操作
manager = AIPromptManager()
available_templates = manager.get_available_templates()
print(f"可用模板: {available_templates}")
```

#### 自定义审查配置
```python
from main import ConfigManager, AIClient

# 加载配置
config_manager = ConfigManager("config.yaml")
ai_client = AIClient(config_manager)

# 创建自定义审查请求
messages = [{"role": "user", "content": "审查这段代码..."}]
response = ai_client.create_chat_completion(messages)
```

## ⚙️ 配置说明

### YAML配置文件

在项目根目录创建 `config.yaml` 文件：

```yaml
config:
  openai:
    base_url: https://openrouter.ai/api/v1
    api_key: your-api-key-here
    model: "openai/gpt-4o"
    organization: your-organization
```

### 配置参数说明

- `base_url`: OpenRouter API 端点
- `api_key`: 你的 OpenRouter API 密钥
- `model`: 要使用的AI模型（如 openai/gpt-4o）
- `organization`: 组织名称（可选）

### 环境变量

你也可以使用环境变量来管理敏感信息：

```bash
export OPENAI_API_KEY="your-api-key"
export OPENROUTER_API_KEY="your-openrouter-key"
```

## 📚 API文档

### 核心模块

#### `main.py`
- **ConfigManager**: 配置管理器
  - `load_config()`: 加载YAML配置文件
  - `get_openai_config()`: 获取OpenAI相关配置
  - `get_api_key()`: 获取API密钥
  - `get_model()`: 获取模型名称
- **AIClient**: AI客户端封装
  - `create_chat_completion(messages, **kwargs)`: 创建聊天补全

#### `ai_prompt.py`
- **AIPromptManager**: 提示词管理器
  - `get_prompt(template_name, **kwargs)`: 获取格式化提示词
  - `get_available_templates()`: 获取可用模板列表
  - `add_custom_template()`: 添加自定义模板
- **CodeReviewPromptBuilder**: 代码审查提示构建器
  - `build_review_prompt()`: 构建代码审查提示
  - `build_multi_file_review_prompt()`: 构建多文件审查提示

#### 预定义提示模板
- `code_review`: 通用代码审查
- `bug_detection`: Bug检测
- `performance_analysis`: 性能分析
- `security_check`: 安全检查
- `code_improvement`: 代码改进
- `documentation_review`: 文档审查
- `architecture_analysis`: 架构分析

#### `code_reader.py` (待实现)
- **功能**: 读取和解析代码文件
- **主要方法**: 
  - `read_file(filepath)`: 读取单个文件
  - `parse_code(content)`: 解析代码内容

#### `code_file_search.py` (待实现)
- **功能**: 搜索和发现代码文件
- **主要方法**:
  - `find_files(directory, extensions)`: 查找指定类型的文件
  - `scan_project(path)`: 扫描整个项目

#### `ai_router.py` (待实现)
- **功能**: AI模型路由和调用
- **主要方法**:
  - `route_request(model, prompt)`: 路由AI请求
  - `get_available_models()`: 获取可用模型列表

## 📝 使用示例

### 简单的代码审查

```python
from main import ConfigManager, AIClient
from ai_prompt import create_code_review_prompt

# 初始化配置和AI客户端
config_manager = ConfigManager()
ai_client = AIClient(config_manager)

# 要审查的代码
code = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
"""

# 创建代码审查提示
prompt = create_code_review_prompt(code, "python")

# 发送给AI进行审查
messages = [{"role": "user", "content": prompt}]
review_result = ai_client.create_chat_completion(messages)

print(review_result)
```

### 使用不同类型的审查

```python
from ai_prompt import (
    create_bug_detection_prompt,
    create_security_check_prompt,
    create_performance_analysis_prompt
)

code = "your_code_here"

# Bug检测
bug_prompt = create_bug_detection_prompt(code, "python")

# 安全检查
security_prompt = create_security_check_prompt(code, "python")

# 性能分析
performance_prompt = create_performance_analysis_prompt(code, "python")

# 使用AI客户端进行分析
for prompt_type, prompt in [
    ("Bug检测", bug_prompt),
    ("安全检查", security_prompt),
    ("性能分析", performance_prompt)
]:
    messages = [{"role": "user", "content": prompt}]
    result = ai_client.create_chat_completion(messages)
    print(f"=== {prompt_type} ===")
    print(result)
    print()
```

### 自定义审查配置

```python
from ai_prompt import AIPromptManager

# 创建提示管理器
manager = AIPromptManager()

# 添加自定义模板
custom_template = """
请对以下{language}代码进行{focus}方面的分析：

代码：
```{language}
{code}
```

请重点关注{focus}相关的问题和改进建议。
"""

manager.add_custom_template(
    "custom_review", 
    custom_template, 
    ["code", "language", "focus"]
)

# 使用自定义模板
prompt = manager.get_prompt(
    "custom_review",
    code="print('hello')",
    language="python",
    focus="可读性"
)
```

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 此仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

### 开发规范

- 遵循 PEP 8 代码风格
- 添加适当的注释和文档字符串
- 编写单元测试
- 确保代码通过所有测试

## 🐛 问题报告

如果您发现任何问题，请通过 [Issues](https://github.com/your-username/codeReviewer/issues) 页面报告。

请包含以下信息：
- 操作系统版本
- Python版本
- 错误信息
- 重现步骤

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 感谢 OpenAI 提供的强大AI模型
- 感谢 OpenRouter 提供的模型路由服务
- 感谢所有贡献者的宝贵建议和代码贡献

## 📞 联系方式

- 项目主页: [https://github.com/your-username/codeReviewer](https://github.com/your-username/codeReviewer)
- 问题反馈: [Issues](https://github.com/your-username/codeReviewer/issues)
- 邮箱: your-email@example.com

---

⭐ 如果这个项目对您有帮助，请给我们一个星标！