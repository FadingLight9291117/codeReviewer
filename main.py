import yaml
import os
from openai import OpenAI
from typing import Dict, Any


class ConfigManager:
    """配置管理器，负责加载和管理YAML配置文件"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载YAML配置文件"""
        try:
            if not os.path.exists(self.config_path):
                raise FileNotFoundError(f"配置文件 {self.config_path} 不存在")
            
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                return config
        except yaml.YAMLError as e:
            raise ValueError(f"YAML配置文件格式错误: {e}")
        except Exception as e:
            raise Exception(f"加载配置文件失败: {e}")
    
    def get_openai_config(self) -> Dict[str, str]:
        """获取OpenAI相关配置"""
        return self.config.get('config', {}).get('openai', {})
    
    def get_api_key(self) -> str:
        """获取API密钥"""
        return self.get_openai_config().get('api_key', '')
    
    def get_base_url(self) -> str:
        """获取API基础URL"""
        return self.get_openai_config().get('base_url', '')
    
    def get_model(self) -> str:
        """获取模型名称"""
        return self.get_openai_config().get('model', 'gpt-3.5-turbo')
    
    def get_organization(self) -> str:
        """获取组织名称"""
        return self.get_openai_config().get('organization', '')


class AIClient:
    """AI客户端封装类"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.client = self._initialize_client()
    
    def _initialize_client(self) -> OpenAI:
        """初始化OpenAI客户端"""
        config = self.config_manager.get_openai_config()
        
        client_kwargs = {
            'base_url': config.get('base_url'),
            'api_key': config.get('api_key')
        }
        
        # 如果有组织配置，添加到参数中
        if config.get('organization'):
            client_kwargs['organization'] = config.get('organization')

        return OpenAI(
            base_url=client_kwargs.get('base_url'),
            api_key=client_kwargs.get('api_key'),
        )

    def create_chat_completion(self, messages: list, **kwargs) -> str:
        """创建聊天补全"""
        try:
            model = kwargs.get('model', self.config_manager.get_model())

            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                **{k: v for k, v in kwargs.items() if k != 'model'}
            )
       
            return completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"AI请求失败: {e}")


def main():
    """主函数"""
    try:
        # 初始化配置管理器
        config_manager = ConfigManager()
        
        # 初始化AI客户端
        ai_client = AIClient(config_manager)
        
        # 测试消息
        messages = [
            {
                "role": "user",
                "content": "生活的意义是什么"
            }
        ]
        
        # 发送请求并获取响应
        response = ai_client.create_chat_completion(messages)
        print(response)
        
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()
