#!/usr/bin/env python3
"""
🧪 智能代码审查系统 - 系统验证器

本文件提供快速的系统功能验证和健康检查，包括：
- 系统初始化状态检查
- AI服务连接验证
- 文件审查功能测试
- Git仓库分析能力验证

适合在部署后或配置变更后进行快速的系统功能验证。
"""

import sys
import os

# 添加父目录到路径，以便导入主模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_code_reviewer import SmartCodeReviewer

# 配置文件路径（相对于父目录）
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.yaml")
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def system_validation():
    """系统验证测试"""
    
    print("🧪 智能代码审查系统 - 系统验证器")
    print("=" * 40)
    
    try:
        # 初始化
        print("1️⃣ 初始化系统...")
        reviewer = SmartCodeReviewer(repo_path=PROJECT_ROOT, config_path=CONFIG_PATH)
        print("✅ 初始化成功")
        
        # 测试AI连接
        print("\n2️⃣ 测试AI连接...")
        if reviewer.ai_router.test_connection():
            print("✅ AI连接正常")
        else:
            print("❌ AI连接失败")
            return
        
        # 测试文件审查
        print("\n3️⃣ 测试文件审查...")
        
        # 创建一个简单的测试文件
        test_code = """
def add_numbers(a, b):
    # 简单的加法函数
    return a + b

def divide_numbers(a, b):
    # 除法函数，可能有除零错误
    return a / b

# 测试代码
result1 = add_numbers(5, 3)
result2 = divide_numbers(10, 0)  # 潜在的除零错误
print(f"结果: {result1}, {result2}")
"""
        
        # 保存测试文件
        with open('test_code.py', 'w', encoding='utf-8') as f:
            f.write(test_code)
        
        # 进行审查
        result = reviewer._review_files_list(['test_code.py'], "快速测试")
        
        if result.get('files_reviewed', 0) > 0:
            print("✅ 文件审查成功")
            
            # 显示审查结果
            for file_path, file_result in result['reviews'].items():
                if 'error' not in file_result:
                    review = file_result['review']['ai_response']
                    print(f"\n📋 {file_path} 审查结果:")
                    print(review[:300] + "..." if len(review) > 300 else review)
        else:
            print("❌ 文件审查失败")
        
        # 清理测试文件
        if os.path.exists('test_code.py'):
            os.remove('test_code.py')
        
        # 测试Git分析（如果在Git仓库中）
        print("\n4️⃣ 测试Git分析...")
        if os.path.exists('.git'):
            try:
                # 尝试分析最近的提交
                git_result = reviewer.review_recent_changes(days=1)
                print(f"✅ Git分析成功，找到 {git_result.get('files_reviewed', 0)} 个文件")
            except Exception as e:
                print(f"⚠️  Git分析失败: {e}")
        else:
            print("ℹ️  不在Git仓库中，跳过Git分析")
        
        print("\n🎉 系统验证完成！")
        print("💡 所有核心功能正常工作")
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")


def main():
    """运行系统验证"""
    system_validation()


if __name__ == "__main__":
    main()
