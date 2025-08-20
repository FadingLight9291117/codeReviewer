#!/usr/bin/env python3
"""
AI路由器模块 - 通过OpenRouter调用各种大模型
支持多种模型的统一接口和智能路由
"""

from config import ConfigManager, AIClient
from typing import Dict, Any, List, Optional
import json
from datetime import datetime
from enum import Enum


class ModelProvider(Enum):
    """模型提供商枚举"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    META = "meta-llama"
    MISTRAL = "mistralai"
    QWEN = "qwen"


class AIRouter:
    """AI路由器 - 通过OpenRouter统一调用多种大模型"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_manager = ConfigManager(config_path)
        self.ai_client = AIClient(self.config_manager)
        self.conversation_history = []
        self.current_model = self.config_manager.get_model()
    
    def switch_model(self, model_name: str) -> bool:
        """切换当前使用的模型"""
        self.current_model = model_name
        print(f"✅ 已切换到模型: {model_name}")
        return True
    
    def create_completion(self, 
                         messages: List[Dict[str, str]], 
                         model: Optional[str] = None,
                         **kwargs) -> str:
        """创建聊天补全"""
        try:
            model = model or self.current_model
            
            # 设置默认参数
            default_params = {
                # 'temperature': 0.7,
                # 'max_tokens': 2000,
                # 'top_p': 1.0,
                # 'frequency_penalty': 0.0,
                # 'presence_penalty': 0.0
            }
            
            # 合并用户参数
            params = {**default_params, **kwargs, 'model': model}
            
            print(f"🤖 使用模型: {model}")
            
            return self.ai_client.create_chat_completion(messages, **params)
            
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg:
                raise Exception(f"API密钥无效或已过期。请检查config.yaml中的api_key配置。\n详细错误: {e}")
            elif "403" in error_msg:
                raise Exception(f"API访问被拒绝。请检查API密钥权限。\n详细错误: {e}")
            elif "404" in error_msg:
                raise Exception(f"模型 '{model}' 不存在或不可用。\n详细错误: {e}")
            elif "429" in error_msg:
                raise Exception(f"API请求过于频繁，请稍后再试。\n详细错误: {e}")
            else:
                raise Exception(f"AI请求失败: {e}")
    
    def test_connection(self) -> bool:
        """测试API连接"""
        try:
            test_messages = [{"role": "user", "content": "Hello"}]
            response = self.create_completion(test_messages)
            print(f"✅ API连接测试成功")
            return True
        except Exception as e:
            print(f"❌ API连接测试失败: {e}")
            return False
    
    def chat(self, 
             user_message: str, 
             system_prompt: Optional[str] = None,
             model: Optional[str] = None,
             use_history: bool = True) -> str:
        """与模型进行对话"""
        
        # 构建消息列表
        messages = []
        
        # 添加系统提示
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # 添加对话历史（如果启用）
        if use_history:
            messages.extend(self.conversation_history)
        
        # 添加当前用户消息
        messages.append({
            "role": "user", 
            "content": user_message
        })
        
        # 获取AI响应
        response = self.create_completion(messages, model)
        
        # 更新对话历史（如果启用）
        if use_history:
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
        print("✅ 对话历史已清空")
    
    def get_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self.conversation_history.copy()
    
    def save_conversation(self, filename: str = None):
        """保存对话到文件"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
        
        conversation_data = {
            "timestamp": datetime.now().isoformat(),
            "model": self.current_model,
            "conversation": self.conversation_history
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 对话已保存到: {filename}")
    
    def load_conversation(self, filename: str):
        """从文件加载对话"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                conversation_data = json.load(f)
            
            self.conversation_history = conversation_data.get("conversation", [])
            if "model" in conversation_data:
                self.current_model = conversation_data["model"]
            
            print(f"📂 已加载对话: {filename}")
            print(f"🤖 模型: {self.current_model}")
            print(f"💬 消息数: {len(self.conversation_history)}")
            
        except Exception as e:
            print(f"❌ 加载对话失败: {e}")


class InteractiveChat:
    """交互式聊天界面"""
    
    def __init__(self, ai_router: AIRouter):
        self.ai_router = ai_router
        self.session_start_time = datetime.now()
    
    def start(self):
        """启动交互式聊天"""
        print("=" * 70)
        print("🤖 AI助手 - 通过OpenRouter连接多种大模型")
        print("=" * 70)
        print(f"当前模型: {self.ai_router.current_model}")
        print("\n📝 可用命令:")
        print("  'quit' 或 'exit' - 退出")
        print("  'clear' - 清空对话历史")
        print("  'models' - 查看可用模型")
        print("  'switch <模型名>' - 切换模型")
        print("  'save [文件名]' - 保存对话")
        print("  'load <文件名>' - 加载对话")
        print("  'history' - 查看对话历史")
        print("-" * 70)
        
        # 默认系统提示
        system_prompt = """你是一个专业、友好、有帮助的AI助手。请用中文回答问题，并尽量提供详细和准确的信息。
对于代码相关的问题，请提供清晰的解释和示例。"""
        
        while True:
            try:
                user_input = input("\n👤 你: ").strip()
                
                if not user_input:
                    continue
                
                # 处理特殊命令
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("\n👋 再见！")
                    break
                elif user_input.lower() == 'clear':
                    self.ai_router.clear_history()
                    continue
                elif user_input.lower() == 'models':
                    self._show_models()
                    continue
                elif user_input.lower().startswith('switch '):
                    model_name = user_input[7:].strip()
                    self.ai_router.switch_model(model_name)
                    continue
                elif user_input.lower().startswith('save'):
                    parts = user_input.split(' ', 1)
                    filename = parts[1] if len(parts) > 1 else None
                    self.ai_router.save_conversation(filename)
                    continue
                elif user_input.lower().startswith('load '):
                    filename = user_input[5:].strip()
                    self.ai_router.load_conversation(filename)
                    continue
                elif user_input.lower() == 'history':
                    self._show_history()
                    continue
                
                print("\n🤖 AI助手正在思考...")
                
                # 获取AI响应
                response = self.ai_router.chat(user_input, system_prompt)
                
                print(f"\n🤖 AI助手: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                break
            except Exception as e:
                print(f"\n❌ 错误: {e}")
    
    def _show_models(self):
        """显示当前模型信息"""
        print(f"\n📋 当前使用的模型: {self.ai_router.current_model}")
        print("\n� 提示: 你可以使用 'switch <模型名>' 切换到任何OpenRouter支持的模型")
        print("   常用模型示例:")
        print("   - openai/gpt-4o")
        print("   - anthropic/claude-3-sonnet")
        print("   - meta-llama/llama-3-70b-instruct")
        print("   - mistralai/mixtral-8x7b-instruct")
        print("使用 'switch <模型名>' 切换模型")
    
    def _show_history(self):
        """显示对话历史"""
        history = self.ai_router.get_history()
        
        if not history:
            print("📭 暂无对话历史")
            return
        
        print(f"\n📚 对话历史 ({len(history)} 条消息):")
        print("-" * 50)
        
        for i, msg in enumerate(history, 1):
            role_icon = "👤" if msg["role"] == "user" else "🤖"
            role_name = "你" if msg["role"] == "user" else "AI助手"
            content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            print(f"{i:2d}. {role_icon} {role_name}: {content}")
        
        print("-" * 50)


def demo_code_review():
    """演示代码审查功能"""
    try:
        ai_router = AIRouter()
        
        print("🔍 代码审查演示")
        print("-" * 40)
        
        code_sample = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 使用示例
for i in range(10):
    print(f"fibonacci({i}) = {fibonacci(i)}")
        '''
        
        review_prompt = """你是一位资深的代码审查专家。请分析以下代码并提供详细的审查意见，包括：
1. 代码质量评估
2. 性能问题分析
3. 潜在的bug或问题
4. 改进建议和最佳实践
5. 重构建议（如果需要）"""
        
        question = f"请审查以下Python代码：\n```python{code_sample}\n```"
        
        response = ai_router.chat(question, review_prompt, use_history=False)
        print(f"\n🤖 代码审查结果:\n{response}")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")


def demo_model_comparison():
    """演示不同模型的对比"""
    try:
        ai_router = AIRouter()
        
        print("⚖️  模型对比演示")
        print("-" * 40)
        
        question = "请解释一下什么是机器学习，并给出一个简单的例子。"
        models_to_test = ["openai/gpt-4o", "anthropic/claude-3-sonnet", "meta-llama/llama-3-70b-instruct"]
        
        for model in models_to_test:
            try:
                print(f"\n🤖 使用模型: {model}")
                print("-" * 30)
                response = ai_router.chat(question, model=model, use_history=False)
                print(f"回答: {response[:200]}...")
            except Exception as e:
                print(f"❌ 模型 {model} 调用失败: {e}")
        
    except Exception as e:
        print(f"❌ 对比演示失败: {e}")


def main():
    """主函数"""
    try:
        print("🚀 AI路由器 - 多模型对话平台")
        print("=" * 50)
        
        # 初始化AI路由器
        ai_router = AIRouter()
        
        # 首先测试API连接
        print("� 正在测试API连接...")
        if not ai_router.test_connection():
            print("\n❌ API连接失败，请检查以下配置:")
            print("1. config.yaml 文件是否存在")
            print("2. API密钥是否正确且有效")
            print("3. base_url 是否正确")
            print("4. 网络连接是否正常")
            return
        
        print("\n选择功能:")
        print("1. 交互式聊天")
        print("2. 代码审查演示")
        print("3. 模型对比演示")
        print("4. 单次问答")
        print("5. 退出")
        
        while True:
            choice = input("\n请选择 (1-5): ").strip()
            
            if choice == '1':
                chat = InteractiveChat(ai_router)
                chat.start()
                break
            elif choice == '2':
                demo_code_review()
                break
            elif choice == '3':
                demo_model_comparison()
                break
            elif choice == '4':
                question = input("请输入你的问题: ")
                response = ai_router.chat(question, use_history=False)
                print(f"\n🤖 AI回答: {response}")
                break
            elif choice == '5':
                print("👋 再见！")
                break
            else:
                print("❌ 无效选择，请重新输入")
    
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("\n💡 提示:")
        print("1. 请确保 config.yaml 文件存在且配置正确")
        print("2. 请检查 API 密钥是否有效")
        print("3. 请确保网络连接正常")


if __name__ == "__main__":
    main()