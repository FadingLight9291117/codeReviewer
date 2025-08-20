#!/usr/bin/env python3
"""
多前缀Git提交代码审查工具
支持同时匹配多个提交前缀并生成综合Markdown报告
"""

from ai_code_reviewer import SmartCodeReviewer
from markdown_generator import MarkdownReportGenerator
from datetime import datetime
import sys
import os


def multi_prefix_review(prefixes=None, time_range="2 weeks ago", output_file=None, project_path=None, config_path="config.yaml"):
    """
    多前缀Git提交代码审查
    
    Args:
        prefixes: 提交前缀列表，默认为常用前缀
        time_range: 时间范围，默认为2周
        output_file: 输出文件名，默认自动生成
        project_path: 待审查项目路径，默认为当前目录
        config_path: 配置文件路径，默认为config.yaml
    
    Returns:
        生成的报告文件路径
    """
    
    # 默认前缀列表
    if prefixes is None:
        prefixes = [
            "feat:",      # 新功能
            "fix:",       # 修复bug
            "refactor:",  # 重构
            "docs:",      # 文档更新
            "style:",     # 代码格式
            "test:",      # 测试相关
            "chore:",     # 杂项任务
        ]
    
    # 处理项目路径
    if project_path is None:
        project_path = "."
    
    # 验证项目路径
    if not os.path.exists(project_path):
        print(f"❌ 错误: 项目路径不存在: {project_path}")
        return None
    
    # 检查是否为Git仓库
    git_path = os.path.join(project_path, '.git')
    if not os.path.exists(git_path):
        print(f"❌ 错误: 指定路径不是Git仓库: {project_path}")
        return None
    
    # 获取绝对路径
    project_path = os.path.abspath(project_path)
    
    print("🔍 多前缀Git提交代码审查工具")
    print("=" * 50)
    print(f"📁 项目路径: {project_path}")
    print(f"📝 匹配前缀: {', '.join(prefixes)}")
    print(f"⏰ 时间范围: {time_range}")
    print("=" * 50)
    
    try:
        # 初始化审查器，指定项目路径和配置文件
        reviewer = SmartCodeReviewer(repo_path=project_path, config_path=config_path)
        
        all_results = {}
        total_files = 0
        total_commits = 0
        
        # 对每个前缀进行审查
        for i, prefix in enumerate(prefixes, 1):
            print(f"\n[{i}/{len(prefixes)}] 🏷️ 处理前缀: {prefix}")
            
            try:
                # 审查特定前缀的提交
                result = reviewer.review_by_commit_prefix(
                    prefix=prefix,
                    since=time_range,
                    review_types=['code_review', 'bug_detection', 'security_check']
                )
                
                files_count = result.get('files_reviewed', 0)
                commits_count = result.get('commits_analyzed', 0)
                
                if files_count > 0:
                    all_results[prefix] = result
                    total_files += files_count
                    total_commits += commits_count
                    
                    print(f"     ✅ 找到 {files_count} 个文件，{commits_count} 个提交")
                else:
                    print(f"     ℹ️ 未找到 {prefix} 相关的提交")
                    
            except Exception as e:
                print(f"     ❌ 处理 {prefix} 时出错: {e}")
        
        # 生成综合报告
        if all_results:
            print(f"\n📊 审查汇总:")
            print(f"   📂 总计文件: {total_files}")
            print(f"   📝 总计提交: {total_commits}")
            print(f"   🏷️ 匹配前缀: {len(all_results)}/{len(prefixes)}")
            
            # 使用模块化报告生成器
            report_generator = MarkdownReportGenerator()
            markdown_report = report_generator.generate_multi_prefix_report(
                all_results=all_results,
                prefixes=prefixes,
                project_path=project_path,
                time_range=time_range
            )
            
            # 确定输出文件名
            if output_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"multi_prefix_review_{timestamp}.md"
            
            # 保存报告
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_report)
            
            print(f"\n✅ 多前缀审查报告已生成: {output_file}")
            print(f"📋 报告包含 {len(all_results)} 种前缀的详细审查结果")
            
            # 显示简要统计
            print(f"\n📈 前缀统计:")
            for prefix in prefixes:
                if prefix in all_results:
                    result = all_results[prefix]
                    files = result.get('files_reviewed', 0)
                    commits = result.get('commits_analyzed', 0)
                    print(f"   {prefix:<12} {files} 文件, {commits} 提交")
            
            return output_file
        else:
            print("\n⚠️ 未找到任何匹配的提交记录")
            print("💡 建议:")
            print("   - 检查Git仓库状态")
            print("   - 调整时间范围")
            print("   - 确认提交消息格式")
            return None
            
    except Exception as e:
        print(f"❌ 多前缀审查失败: {e}")
        return None


def main():
    """命令行入口"""
    
    if len(sys.argv) > 1:
        # 处理命令行参数
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("""
🔍 多前缀Git提交代码审查工具

用法:
    python multi_prefix_review.py [options]

选项:
    --help, -h      显示帮助信息
    --prefixes      指定前缀列表 (逗号分隔)
    --time          指定时间范围 (默认: 2 weeks ago)
    --output        指定输出文件名
    --project       指定待审查项目路径 (默认: 当前目录)

示例:
    python multi_prefix_review.py
    python multi_prefix_review.py --prefixes "feat:,fix:,docs:"
    python multi_prefix_review.py --time "1 month ago"
    python multi_prefix_review.py --output "my_review.md"
    python multi_prefix_review.py --project "/path/to/project"
    python multi_prefix_review.py --project "C:\\Projects\\MyApp" --prefixes "feat:,fix:"
            """)
            return
        
        # 解析参数
        prefixes = None
        time_range = "2 weeks ago"
        output_file = None
        project_path = None
        
        i = 1
        while i < len(sys.argv):
            if sys.argv[i] == "--prefixes" and i + 1 < len(sys.argv):
                prefixes = [p.strip() for p in sys.argv[i + 1].split(",")]
                i += 2
            elif sys.argv[i] == "--time" and i + 1 < len(sys.argv):
                time_range = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--output" and i + 1 < len(sys.argv):
                output_file = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--project" and i + 1 < len(sys.argv):
                project_path = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        
        # 执行审查
        multi_prefix_review(prefixes, time_range, output_file, project_path)
    else:
        # 默认执行
        multi_prefix_review()


if __name__ == "__main__":
    main()
