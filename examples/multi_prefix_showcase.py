#!/usr/bin/env python3
"""
🎭 多前缀Git提交代码审查 - 功能展示

本文件展示多前缀Git提交代码审查工具的各种高级功能和使用场景：
- 基本多前缀审查操作
- 自定义前缀配置策略
- 项目路径灵活指定
- 多种时间范围分析
- 综合代码质量评估
- 完整的错误处理机制

这是一个全面的功能展示脚本，演示了从基础到高级的所有使用场景。
"""

import sys
import os
import time

# 添加父目录到路径，以便导入主模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multi_prefix_review import multi_prefix_review

# 项目根目录路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.yaml")



def demo_basic_usage():
    """演示基本使用"""
    
    print("🎯 演示1: 基本多前缀审查")
    print("=" * 40)
    
    # 使用默认前缀
    print("📝 使用常见前缀进行审查...")
    report_file = multi_prefix_review(
        prefixes=["feat:", "fix:"],
        time_range="2 weeks ago",
        project_path=PROJECT_ROOT,
        config_path=CONFIG_PATH
    )
    
    if report_file:
        print(f"✅ 基本审查完成，报告: {report_file}")
    else:
        print("⚠️ 未找到匹配的提交")
    
    return report_file


def demo_custom_prefixes():
    """演示自定义前缀"""
    
    print("\n🎯 演示2: 自定义前缀审查")
    print("=" * 40)
    
    # 自定义前缀列表
    custom_prefixes = [
        "feat:",      # 新功能
        "bugfix:",    # Bug修复
        "hotfix:",    # 热修复
        "security:",  # 安全修复
    ]
    
    print(f"📝 使用自定义前缀: {', '.join(custom_prefixes)}")
    report_file = multi_prefix_review(
        prefixes=custom_prefixes,
        time_range="1 month ago",
        output_file="custom_prefix_review.md",
        project_path="."  # 明确指定当前目录
    )
    
    if report_file:
        print(f"✅ 自定义前缀审查完成，报告: {report_file}")
    else:
        print("⚠️ 未找到匹配的提交")
    
    return report_file


def demo_project_path():
    """演示指定项目路径功能"""
    
    print("\n🎯 演示3: 指定项目路径审查")
    print("=" * 40)
    
    # 演示不同的项目路径
    project_paths = [
        (".", "当前目录"),
        (os.path.abspath("."), "当前目录(绝对路径)"),
    ]
    
    print("📝 演示不同项目路径的审查...")
    
    for project_path, description in project_paths:
        print(f"\n📁 {description}: {project_path}")
        
        try:
            report_file = multi_prefix_review(
                prefixes=["feat:", "fix:"],
                time_range="1 week ago",
                output_file=f"path_review_{description.replace('(', '').replace(')', '').replace(' ', '_')}.md",
                project_path=project_path
            )
            
            if report_file:
                file_size = os.path.getsize(report_file) if os.path.exists(report_file) else 0
                print(f"   ✅ 审查完成: {report_file} ({file_size} bytes)")
            else:
                print(f"   ℹ️ 无匹配提交")
                
        except Exception as e:
            print(f"   ❌ 审查失败: {e}")
    
    # 演示错误处理
    print(f"\n🧪 测试错误处理:")
    print("📝 测试不存在的路径...")
    try:
        result = multi_prefix_review(
            prefixes=["feat:"],
            project_path="/non/existent/path"
        )
        if not result:
            print("   ✅ 正确处理不存在的路径")
    except Exception as e:
        print(f"   ✅ 正确捕获错误: {e}")


def demo_time_ranges():
    """演示不同时间范围"""
    
    print("\n🎯 演示4: 不同时间范围审查")
    print("=" * 40)
    
    time_ranges = [
        ("3 days ago", "最近3天"),
        ("1 week ago", "最近1周"),
        ("2 weeks ago", "最近2周"),
    ]
    
    for time_range, description in time_ranges:
        print(f"\n📅 {description} ({time_range}):")
        
        try:
            report_file = multi_prefix_review(
                prefixes=["feat:", "fix:"],
                time_range=time_range,
                output_file=f"review_{time_range.replace(' ', '_')}.md"
            )
            
            if report_file:
                # 获取文件大小
                file_size = os.path.getsize(report_file) if os.path.exists(report_file) else 0
                print(f"   ✅ 报告生成: {report_file} ({file_size} bytes)")
            else:
                print(f"   ℹ️ 该时间范围内无匹配提交")
                
        except Exception as e:
            print(f"   ❌ 审查失败: {e}")


def demo_comprehensive_review():
    """演示综合审查"""
    
    print("\n🎯 演示5: 综合代码审查")
    print("=" * 40)
    
    # 全面的前缀列表
    comprehensive_prefixes = [
        "feat:",      # 新功能
        "fix:",       # 修复
        "refactor:",  # 重构
        "docs:",      # 文档
        "style:",     # 格式
        "test:",      # 测试
        "chore:",     # 杂项
        "perf:",      # 性能
        "ci:",        # CI/CD
        "build:",     # 构建
    ]
    
    print(f"📝 使用完整前缀列表 ({len(comprehensive_prefixes)} 种前缀)")
    print("⏰ 分析最近1个月的所有提交...")
    
    start_time = time.time()
    
    report_file = multi_prefix_review(
        prefixes=comprehensive_prefixes,
        time_range="1 month ago",
        output_file="comprehensive_review.md"
    )
    
    end_time = time.time()
    duration = end_time - start_time
    
    if report_file:
        file_size = os.path.getsize(report_file) if os.path.exists(report_file) else 0
        print(f"✅ 综合审查完成")
        print(f"📊 报告文件: {report_file}")
        print(f"📁 报告大小: {file_size:,} bytes")
        print(f"⏱️ 耗时: {duration:.2f} 秒")
        
        # 显示报告预览
        if os.path.exists(report_file):
            print(f"\n📋 报告预览:")
            with open(report_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:10]
                for line in lines:
                    print(f"   {line.rstrip()}")
                if len(lines) >= 10:
                    print("   ...")
    else:
        print("⚠️ 未找到匹配的提交")


def demo_error_handling():
    """演示错误处理"""
    
    print("\n🎯 演示6: 错误处理展示")
    print("=" * 40)
    
    # 测试无效的时间范围
    print("📝 测试无效时间范围...")
    try:
        report_file = multi_prefix_review(
            prefixes=["feat:"],
            time_range="invalid_time",
            output_file="error_test.md"
        )
    except Exception as e:
        print(f"   ✅ 正确捕获错误: {e}")
    
    # 测试空前缀列表
    print("\n📝 测试空前缀列表...")
    try:
        report_file = multi_prefix_review(
            prefixes=[],
            time_range="1 week ago"
        )
        if not report_file:
            print("   ✅ 正确处理空前缀列表")
    except Exception as e:
        print(f"   ✅ 正确捕获错误: {e}")


def show_summary():
    """显示演示总结"""
    
    print("\n🎉 演示完成总结")
    print("=" * 50)
    
    # 列出生成的文件
    generated_files = []
    for file in os.listdir('.'):
        if file.endswith('.md') and ('review' in file or 'prefix' in file):
            generated_files.append(file)
    
    if generated_files:
        print("📁 生成的报告文件:")
        for file in sorted(generated_files):
            file_size = os.path.getsize(file)
            print(f"   📄 {file} ({file_size:,} bytes)")
    
    print(f"\n💡 使用建议:")
    print("   1. 定期运行多前缀审查监控代码质量")
    print("   2. 根据项目需求自定义前缀列表")
    print("   3. 将报告集成到代码审查流程中")
    print("   4. 使用不同时间范围进行阶段性分析")
    
    print(f"\n🔧 命令行使用:")
    print("   python multi_prefix_review.py --prefixes 'feat:,fix:' --time '1 week ago'")
    print("   python multi_prefix_review.py --help")


def main():
    """运行所有功能展示"""
    
    print("� 多前缀Git提交代码审查 - 功能展示")
    print("=" * 60)
    print("🎯 本展示将演示多前缀代码审查工具的各种高级功能")
    print("⏰ 预计耗时: 2-3分钟")
    print("=" * 60)
    
    try:
        # 演示1: 基本使用
        demo_basic_usage()
        
        # 演示2: 自定义前缀
        demo_custom_prefixes()
        
        # 演示3: 项目路径
        demo_project_path()
        
        # 演示4: 时间范围
        demo_time_ranges()
        
        # 演示5: 综合审查
        demo_comprehensive_review()
        
        # 演示6: 错误处理
        demo_error_handling()
        
        # 显示总结
        show_summary()
        
        print("\n🎉 所有演示完成！")
        print("📖 查看生成的Markdown报告了解详细审查结果")
        
    except KeyboardInterrupt:
        print("\n⏹️ 演示被用户中断")
    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")


if __name__ == "__main__":
    main()
