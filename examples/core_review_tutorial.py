#!/usr/bin/env python3
"""
🎓 智能代码审查系统 - 核心功能教程

本文件提供智能代码审查系统的核心功能教程，包括：
- 基础代码审查功能
- 最近变更审查技巧
- 自定义文件审查方法
- Markdown报告生成演示
- AI模型配置和测试

适合初学者学习和理解系统核心功能的完整教程。
注意：多前缀审查功能请参考 multi_prefix_showcase.py
"""

import sys
import os
# 添加父目录到路径，以便导入主模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_code_reviewer import SmartCodeReviewer
import json

# 配置文件路径（相对于父目录）
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.yaml")
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def example_basic_code_review():
    """示例1：基础代码审查功能"""
    
    print("📝 示例1: 基础代码审查")
    print("=" * 40)
    
    try:
        # 初始化智能审查器
        reviewer = SmartCodeReviewer(repo_path=PROJECT_ROOT, config_path=CONFIG_PATH)
        
        # 审查指定前缀的提交
        result = reviewer.review_by_commit_prefix(
            prefix="feat:", 
            since="1 week ago",
            review_types=['code_review', 'bug_detection']
        )
        
        # 显示结果摘要
        files_count = result.get('files_reviewed', 0)
        commits_count = result.get('commits_analyzed', 0)
        
        print(f"✅ 审查完成!")
        print(f"📂 审查了 {files_count} 个文件")
        print(f"📝 分析了 {commits_count} 个提交")
        
        # 显示审查结果预览
        if result.get('reviews') and files_count > 0:
            print("\n📋 审查结果预览:")
            for file_path, file_result in list(result['reviews'].items())[:2]:
                if 'error' not in file_result:
                    language = file_result.get('language', 'unknown')
                    print(f"\n📄 {file_path} ({language})")
                    
                    # 显示审查内容摘要
                    if 'reviews' in file_result:
                        for review_type, review_data in file_result['reviews'].items():
                            if 'error' not in review_data:
                                response = review_data['ai_response'][:100]
                                print(f"  {review_type}: {response}...")
        else:
            print("ℹ️  未找到相关提交进行审查")
        
        return result
        
    except Exception as e:
        print(f"❌ 示例执行失败: {e}")
        return None


def example_recent_changes_review():
    """示例2：审查最近的代码变更"""
    
    print("\n📝 示例2: 审查最近的代码变更")
    print("=" * 40)
    
    try:
        reviewer = SmartCodeReviewer(repo_path=PROJECT_ROOT, config_path=CONFIG_PATH)
        
        # 审查最近3天的变更
        result = reviewer.review_recent_changes(days=3)
        
        files_count = result.get('files_reviewed', 0)
        print(f"✅ 审查完成! 审查了 {files_count} 个文件")
        
        # 显示审查结果预览
        if result.get('reviews') and files_count > 0:
            print("\n📋 审查结果预览:")
            # 只显示第一个文件的结果
            first_file = list(result['reviews'].items())[0]
            file_path, file_result = first_file
            
            if 'error' not in file_result:
                response = file_result['review']['ai_response'][:150]
                print(f"📄 {file_path}: {response}...")
        else:
            print("ℹ️  最近没有代码变更或审查失败")
        
        return result
        
    except Exception as e:
        print(f"❌ 示例执行失败: {e}")
        return None


def example_custom_file_review():
    """示例3：自定义文件审查"""
    
    print("\n📝 示例3: 自定义文件审查")
    print("=" * 40)
    
    try:
        reviewer = SmartCodeReviewer(repo_path=PROJECT_ROOT, config_path=CONFIG_PATH)
        
        # 审查指定的文件列表
        files_to_review = []
        potential_files = ['ai_router.py', 'ai_prompt.py', 'code_reader.py']
        
        # 检查文件是否存在
        for file_path in potential_files:
            full_path = os.path.join(PROJECT_ROOT, file_path)
            if os.path.exists(full_path):
                files_to_review.append(file_path)
        
        if not files_to_review:
            print("⚠️  未找到可审查的文件")
            return None
        
        print(f"🔍 准备审查文件: {', '.join(files_to_review)}")
        
        # 执行审查
        result = reviewer._review_files_list(files_to_review, "自定义文件审查")
        
        # 显示结果
        if result.get('reviews'):
            print(f"\n✅ 审查完成! 审查了 {len(result['reviews'])} 个文件")
            
            for file_path, file_result in result['reviews'].items():
                if 'error' not in file_result:
                    language = file_result.get('language', 'unknown')
                    review_data = file_result['review']
                    response_preview = review_data['ai_response'][:100]
                    print(f"\n📄 {file_path} ({language})")
                    print(f"   📋 {response_preview}...")
                else:
                    print(f"\n❌ {file_path}: {file_result['error']}")
        else:
            print("❌ 未能获取审查结果")
        
        return result
        
    except Exception as e:
        print(f"❌ 示例执行失败: {e}")
        return None


def example_markdown_report_generation():
    """示例4：Markdown报告生成"""
    
    print("\n📝 示例4: 生成Markdown报告")
    print("=" * 40)
    
    try:
        reviewer = SmartCodeReviewer(repo_path=PROJECT_ROOT, config_path=CONFIG_PATH)
        
        # 进行一次代码审查
        print("🔍 正在进行代码审查...")
        result = reviewer.review_by_commit_prefix("feat:", since="1 week ago")
        
        files_count = result.get('files_reviewed', 0)
        
        if files_count > 0:
            # 生成并保存Markdown报告
            print("📝 正在生成Markdown报告...")
            markdown_report = reviewer.generate_markdown_report(result)
            
            # 保存报告文件
            report_filename = f"tutorial_review_report_{reviewer.get_timestamp()}.md"
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(markdown_report)
            
            print(f"✅ Markdown报告已生成: {report_filename}")
            
            # 显示报告预览
            print("\n📋 报告预览:")
            preview_lines = markdown_report.split('\n')[:10]
            for line in preview_lines:
                print(f"   {line}")
            print("   ...")
            
            return report_filename
        else:
            print("ℹ️  未找到相关代码进行审查，无法生成报告")
            return None
        
    except Exception as e:
        print(f"❌ 示例执行失败: {e}")
        return None


def example_ai_model_testing():
    """示例5：AI模型配置和测试"""
    
    print("\n📝 示例5: AI模型配置和测试")
    print("=" * 40)
    
    try:
        reviewer = SmartCodeReviewer(repo_path=PROJECT_ROOT, config_path=CONFIG_PATH)
        
        # 准备测试代码片段
        test_code = '''
def calculate_sum(numbers):
    """计算数字列表的总和"""
    total = 0
    for num in numbers:
        total += num  # 可能的改进：使用内置sum()函数
    return total

def process_data(data):
    # 缺少输入验证
    result = []
    for item in data:
        result.append(item * 2)
    return result
'''
        
        print("🤖 正在测试AI模型审查能力...")
        
        # 测试当前配置的模型
        try:
            # 进行代码审查
            review_result = reviewer._perform_single_review(
                test_code, "python", "code_review", "test_example.py"
            )
            
            if 'error' not in review_result:
                model_name = reviewer.ai_router.current_model
                response = review_result['ai_response']
                
                print(f"✅ 当前模型 ({model_name}) 测试成功")
                print(f"\n📋 审查结果预览:")
                print(f"   {response[:200]}...")
                
                # 测试连接状态
                if reviewer.ai_router.test_connection():
                    print("🔗 AI连接状态: 正常")
                else:
                    print("⚠️  AI连接状态: 异常")
                    
            else:
                print(f"❌ 模型测试失败: {review_result['error']}")
                
        except Exception as e:
            print(f"❌ 模型测试出错: {e}")
            
        # 显示当前配置信息
        print(f"\n⚙️  当前配置:")
        print(f"   模型: {reviewer.ai_router.current_model}")
        print(f"   API状态: {'正常' if reviewer.ai_router.test_connection() else '异常'}")
        
    except Exception as e:
        print(f"❌ 示例执行失败: {e}")


def main():
    """运行核心功能教程"""
    
    print("🎓 智能代码审查系统 - 核心功能教程")
    print("=" * 50)
    print("💡 提示: 多前缀审查功能请使用 multi_prefix_showcase.py")
    print("")
    
    # 运行核心示例
    try:
        # 示例1: 基础代码审查
        example_basic_code_review()
        
        # 示例2: 审查最近变更  
        example_recent_changes_review()
        
        # 示例3: 自定义文件审查
        example_custom_file_review()
        
        # 示例4: 生成Markdown报告
        report_file = example_markdown_report_generation()
        
        # 示例5: AI模型测试
        example_ai_model_testing()
        
        print("\n🎉 所有核心教程完成!")
        
        if report_file:
            print(f"📋 生成的报告文件: {report_file}")
        
        print("\n💡 更多功能:")
        print("   📚 多前缀审查: python ../multi_prefix_review.py")
        print("   🎯 多前缀展示: python multi_prefix_showcase.py") 
        print("   🧪 系统验证: python system_validator.py")
        
    except Exception as e:
        print(f"❌ 教程运行失败: {e}")


if __name__ == "__main__":
    main()
