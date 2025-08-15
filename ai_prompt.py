from typing import Dict, List, Optional, Any
import json


class PromptTemplate:
    """提示词模板类"""
    
    def __init__(self, template: str, variables: Optional[List[str]] = None):
        self.template = template
        self.variables = variables or []
    
    def format(self, **kwargs) -> str:
        """格式化模板，填入变量"""
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"缺少必需的变量: {e}")


class AIPromptManager:
    """AI提示词管理器"""
    
    def __init__(self):
        self.templates = self._initialize_templates()
    
    def _initialize_templates(self) -> Dict[str, PromptTemplate]:
        """初始化所有提示词模板"""
        return {
            "code_review": PromptTemplate(
                template=self._get_code_review_template(),
                variables=["code", "language", "focus_areas"]
            ),
            "bug_detection": PromptTemplate(
                template=self._get_bug_detection_template(),
                variables=["code", "language"]
            ),
            "performance_analysis": PromptTemplate(
                template=self._get_performance_analysis_template(),
                variables=["code", "language"]
            ),
            "security_check": PromptTemplate(
                template=self._get_security_check_template(),
                variables=["code", "language"]
            ),
            "code_improvement": PromptTemplate(
                template=self._get_code_improvement_template(),
                variables=["code", "language", "improvement_type"]
            ),
            "documentation_review": PromptTemplate(
                template=self._get_documentation_review_template(),
                variables=["code", "language"]
            ),
            "architecture_analysis": PromptTemplate(
                template=self._get_architecture_analysis_template(),
                variables=["code", "language", "context"]
            )
        }
    
    def _get_code_review_template(self) -> str:
        """通用代码审查模板"""
        return """你是一位资深的代码审查专家。请对以下{language}代码进行全面的代码审查。

代码内容:
```{language}
{code}
```

请重点关注以下方面：
{focus_areas}

请提供详细的审查报告，包括：
1. 代码质量评估（1-10分）
2. 发现的问题和潜在风险
3. 具体的改进建议
4. 最佳实践建议
5. 如果有严重问题，请提供修改后的代码示例

请用中文回复，格式要清晰易读。"""
    
    def _get_bug_detection_template(self) -> str:
        """Bug检测模板"""
        return """你是一位专业的Bug检测专家。请仔细分析以下{language}代码，查找可能存在的Bug和逻辑错误。

代码内容:
```{language}
{code}
```

请重点检查：
1. 空指针/空引用异常
2. 数组越界
3. 逻辑错误
4. 异常处理不当
5. 资源泄漏
6. 并发问题
7. 类型错误
8. 边界条件处理

对于发现的每个问题，请提供：
- 问题描述
- 问题位置（行号）
- 严重程度（高/中/低）
- 修复建议
- 修复后的代码示例

请用中文回复。"""
    
    def _get_performance_analysis_template(self) -> str:
        """性能分析模板"""
        return """你是一位性能优化专家。请分析以下{language}代码的性能表现，识别潜在的性能瓶颈。

代码内容:
```{language}
{code}
```

请分析以下性能方面：
1. 时间复杂度分析
2. 空间复杂度分析
3. 算法效率
4. 数据结构选择
5. 循环优化机会
6. 内存使用效率
7. I/O操作优化
8. 缓存机会

对于每个性能问题，请提供：
- 问题描述
- 当前复杂度
- 优化建议
- 优化后的预期复杂度
- 优化代码示例

请用中文回复。"""
    
    def _get_security_check_template(self) -> str:
        """安全检查模板"""
        return """你是一位网络安全专家。请对以下{language}代码进行安全审计，识别潜在的安全漏洞。

代码内容:
```{language}
{code}
```

请重点检查以下安全问题：
1. SQL注入风险
2. XSS（跨站脚本）漏洞
3. CSRF（跨站请求伪造）风险
4. 输入验证不足
5. 敏感信息泄露
6. 认证和授权问题
7. 加密和哈希安全性
8. 文件操作安全性
9. 命令注入风险
10. 依赖库安全性

对于发现的每个安全问题，请提供：
- 漏洞类型
- 风险等级（严重/高/中/低）
- 攻击场景描述
- 修复建议
- 安全的代码实现示例

请用中文回复。"""
    
    def _get_code_improvement_template(self) -> str:
        """代码改进模板"""
        return """你是一位代码重构专家。请对以下{language}代码提供{improvement_type}方面的改进建议。

代码内容:
```{language}
{code}
```

请关注以下改进方向：
- 代码可读性提升
- 代码结构优化
- 设计模式应用
- 代码复用性
- 维护性改善
- 测试友好性

请提供：
1. 当前代码的问题分析
2. 具体的改进建议
3. 重构后的代码示例
4. 改进后的优势说明
5. 重构的注意事项

请用中文回复。"""
    
    def _get_documentation_review_template(self) -> str:
        """文档审查模板"""
        return """你是一位技术文档专家。请评估以下{language}代码的文档质量。

代码内容:
```{language}
{code}
```

请评估以下方面：
1. 注释的完整性和准确性
2. 函数/方法文档字符串
3. 类和模块说明
4. 复杂逻辑的解释
5. 参数和返回值说明
6. 异常情况说明
7. 使用示例
8. TODO和FIXME标记

请提供：
- 文档质量评分（1-10分）
- 缺失的文档内容
- 改进建议
- 文档模板示例
- 标准化建议

请用中文回复。"""
    
    def _get_architecture_analysis_template(self) -> str:
        """架构分析模板"""
        return """你是一位软件架构师。请分析以下{language}代码的架构设计。

代码内容:
```{language}
{code}
```

项目上下文：
{context}

请分析以下架构方面：
1. 模块划分和职责分离
2. 依赖关系和耦合度
3. 设计模式的使用
4. 可扩展性和可维护性
5. 代码组织结构
6. 接口设计
7. 错误处理策略
8. 配置管理

请提供：
- 架构优势分析
- 存在的架构问题
- 改进建议
- 重构方案
- 最佳实践建议

请用中文回复。"""
    
    def get_prompt(self, template_name: str, **kwargs) -> str:
        """获取格式化后的提示词"""
        if template_name not in self.templates:
            raise ValueError(f"未知的模板名称: {template_name}")
        
        template = self.templates[template_name]
        return template.format(**kwargs)
    
    def get_available_templates(self) -> List[str]:
        """获取所有可用的模板名称"""
        return list(self.templates.keys())
    
    def add_custom_template(self, name: str, template: str, variables: Optional[List[str]] = None):
        """添加自定义模板"""
        self.templates[name] = PromptTemplate(template, variables)
    
    def get_template_variables(self, template_name: str) -> List[str]:
        """获取模板所需的变量"""
        if template_name not in self.templates:
            raise ValueError(f"未知的模板名称: {template_name}")
        
        return self.templates[template_name].variables


class CodeReviewPromptBuilder:
    """代码审查提示词构建器"""
    
    def __init__(self, prompt_manager: AIPromptManager):
        self.prompt_manager = prompt_manager
    
    def build_review_prompt(self, 
                          code: str, 
                          language: str, 
                          review_type: str = "code_review",
                          focus_areas: Optional[List[str]] = None,
                          **kwargs) -> str:
        """构建代码审查提示词"""
        
        # 默认关注领域
        if focus_areas is None:
            focus_areas = [
                "代码质量和可读性",
                "性能优化机会", 
                "潜在的Bug和错误",
                "安全性问题",
                "最佳实践建议"
            ]
        
        focus_areas_text = "\n".join([f"- {area}" for area in focus_areas])
        
        # 构建参数字典
        prompt_kwargs = {
            "code": code,
            "language": language,
            "focus_areas": focus_areas_text,
            **kwargs
        }
        
        return self.prompt_manager.get_prompt(review_type, **prompt_kwargs)
    
    def build_multi_file_review_prompt(self, 
                                     files: Dict[str, str], 
                                     language: str,
                                     context: str = "") -> str:
        """构建多文件代码审查提示词"""
        
        files_content = []
        for filename, content in files.items():
            files_content.append(f"文件: {filename}\n```{language}\n{content}\n```\n")
        
        combined_code = "\n".join(files_content)
        
        return self.build_review_prompt(
            code=combined_code,
            language=language,
            review_type="architecture_analysis",
            context=context
        )


# 便捷函数
def create_code_review_prompt(code: str, 
                            language: str, 
                            focus_areas: Optional[List[str]] = None) -> str:
    """创建代码审查提示词的便捷函数"""
    prompt_manager = AIPromptManager()
    builder = CodeReviewPromptBuilder(prompt_manager)
    return builder.build_review_prompt(code, language, focus_areas=focus_areas)


def create_bug_detection_prompt(code: str, language: str) -> str:
    """创建Bug检测提示词的便捷函数"""
    prompt_manager = AIPromptManager()
    return prompt_manager.get_prompt("bug_detection", code=code, language=language)


def create_security_check_prompt(code: str, language: str) -> str:
    """创建安全检查提示词的便捷函数"""
    prompt_manager = AIPromptManager()
    return prompt_manager.get_prompt("security_check", code=code, language=language)


def create_performance_analysis_prompt(code: str, language: str) -> str:
    """创建性能分析提示词的便捷函数"""
    prompt_manager = AIPromptManager()
    return prompt_manager.get_prompt("performance_analysis", code=code, language=language)


if __name__ == "__main__":
    # 示例用法
    prompt_manager = AIPromptManager()
    
    # 示例代码
    sample_code = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
    """
    
    # 生成不同类型的提示词
    print("=== 代码审查提示词 ===")
    code_review_prompt = create_code_review_prompt(sample_code, "python")
    print(code_review_prompt[:200] + "...")
    
    print("\n=== Bug检测提示词 ===")
    bug_detection_prompt = create_bug_detection_prompt(sample_code, "python")
    print(bug_detection_prompt[:200] + "...")
    
    print("\n=== 性能分析提示词 ===")
    performance_prompt = create_performance_analysis_prompt(sample_code, "python")
    print(performance_prompt[:200] + "...")

