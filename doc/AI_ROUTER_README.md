# AI路由器 - 多模型对话平台

## 项目简介

AI路由器是一个基于Python的多模型对话平台，支持通过OpenRouter服务访问多种AI模型，包括OpenAI、Anthropic、Google、Meta、Mistral等多家提供商的模型。

## 文件说明

### 1. `ai_router.py` - 完整功能版本
- **功能**: 完整的AI路由器实现，支持真实的API调用
- **依赖**: 需要有效的OpenRouter API密钥
- **配置**: 需要配置 `config.yaml` 文件

### 2. `ai_router_demo.py` - 演示版本
- **功能**: 功能演示版本，使用模拟响应
- **优点**: 无需API密钥即可运行，适合学习和测试
- **限制**: 生成模拟响应，不是真实的AI对话

### 3. `config.yaml` - 配置文件
- **用途**: 存储API密钥和模型配置
- **注意**: 包含敏感信息，不应提交到版本控制

### 4. `config_template.yaml` - 配置模板
- **用途**: 配置文件模板，帮助用户设置自己的配置
- **使用**: 复制并重命名为 `config.yaml`，然后填入你的API密钥

## 快速开始

### 方法一：使用演示版本（推荐新用户）

```bash
# 直接运行演示版本
python ai_router_demo.py
```

### 方法二：使用完整版本

1. **获取API密钥**
   - 访问 [OpenRouter](https://openrouter.ai/)
   - 注册账户并获取API密钥

2. **配置环境**
   ```bash
   # 复制配置模板
   copy config_template.yaml config.yaml
   
   # 编辑config.yaml，填入你的API密钥
   notepad config.yaml
   ```

3. **安装依赖**
   ```bash
   pip install openai pyyaml
   ```

4. **运行程序**
   ```bash
   python ai_router.py
   ```

## 功能特性

### 🤖 多模型支持
- **OpenAI**: GPT-4o, GPT-4-turbo, GPT-3.5-turbo
- **Anthropic**: Claude-3 系列
- **Google**: Gemini Pro 系列
- **Meta**: Llama-3 系列
- **Mistral**: Mistral 和 Mixtral 系列

### 💬 交互式聊天
- 支持连续对话，保留上下文
- 动态切换AI模型
- 清空历史记录
- 查看对话历史

### 🔧 灵活配置
- YAML配置文件
- 自定义系统提示词
- 模型参数调整

### 🛡️ 错误处理
- API限流处理
- 网络错误重试
- 详细错误信息

## 使用示例

### 基本对话
```python
from ai_router import AIRouter

# 创建路由器实例
router = AIRouter()

# 简单对话
response = router.chat("你好，你能帮我写一段Python代码吗？")
print(response)
```

### 代码审查
```python
code = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''

response = router.chat(f"请审查这段代码：{code}")
print(response)
```

### 切换模型
```python
# 切换到Claude模型
router.switch_model("anthropic/claude-3-sonnet")

# 使用新模型对话
response = router.chat("请解释一下机器学习的基本概念")
print(response)
```

## 命令行界面

运行程序后，可以使用以下命令：

- `quit` 或 `exit` - 退出程序
- `clear` - 清空对话历史
- `models` - 查看可用模型列表
- `switch <模型名>` - 切换当前使用的模型
- `history` - 查看对话历史

## 注意事项

1. **API成本**: 使用真实API会产生费用，请注意使用量
2. **API限制**: 不同模型有不同的速率限制和上下文长度限制
3. **网络要求**: 需要稳定的网络连接访问OpenRouter服务
4. **密钥安全**: 不要将API密钥提交到公共代码仓库

## 故障排除

### 常见错误

1. **401 Unauthorized**
   - 检查API密钥是否正确
   - 确认API密钥是否有效且未过期

2. **429 Too Many Requests**
   - 请求过于频繁，等待一段时间后重试
   - 考虑降低请求频率

3. **404 Not Found**
   - 检查模型名称是否正确
   - 确认模型是否可用

4. **网络连接错误**
   - 检查网络连接
   - 确认能够访问OpenRouter服务

### 调试建议

1. **使用演示版本**: 先运行 `ai_router_demo.py` 确认基本功能正常
2. **检查配置**: 确认 `config.yaml` 文件格式正确
3. **测试连接**: 使用简单的测试消息验证API连接

## 开发计划

- [ ] 支持更多AI提供商
- [ ] 添加对话保存和加载功能
- [ ] 实现Web界面
- [ ] 添加图像生成功能
- [ ] 支持文件上传和分析

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 许可证

MIT License
