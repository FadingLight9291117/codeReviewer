#!/usr/bin/env python3
"""
智能代码审查系统 - 整合AI路由器、提示词模板和Git分析器
自动分析Git提交记录并进行AI代码审查
"""

import os
import sys
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

# 导入项目模块
from ai_router import AIRouter
from ai_prompt import (
    AIPromptManager, 
    CodeReviewPromptBuilder,
    create_code_review_prompt,
    create_bug_detection_prompt,
    create_security_check_prompt,
    create_performance_analysis_prompt
)
from git_commit_analyzer import (
    GitAnalyzer, 
    RequirementAnalyzer,
    get_files_for_review_by_prefix
)
from markdown_generator import MarkdownReportGenerator


class SmartCodeReviewer:
    """智能代码审查器"""
    
    def __init__(self, repo_path: str = ".", config_path: str = "config.yaml"):
        """
        初始化智能代码审查器
        
        Args:
            repo_path: Git仓库路径
            config_path: AI配置文件路径
        """
        self.repo_path = os.path.abspath(repo_path)
        self.ai_router = AIRouter(config_path)
        self.prompt_manager = AIPromptManager()
        self.prompt_builder = CodeReviewPromptBuilder(self.prompt_manager)
        self.git_analyzer = GitAnalyzer(repo_path)
        self.requirement_analyzer = RequirementAnalyzer(repo_path)
    
    def review_by_commit_prefix(self, 
                               prefix: str, 
                               since: str = "1 week ago",
                               review_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        根据提交前缀进行智能代码审查
        
        Args:
            prefix: 提交消息前缀 (如: 'feat:', 'fix:', 'JIRA-123:')
            since: 时间范围
            review_types: 审查类型列表 ['code_review', 'bug_detection', 'security_check', 'performance_analysis']
            
        Returns:
            审查结果字典
        """
        print(f"🔍 开始分析提交前缀: {prefix}")
        print(f"⏰ 时间范围: {since}")
        
        # 默认审查类型
        if review_types is None:
            review_types = ['code_review', 'bug_detection', 'performance_analysis']
        
        # 1. 获取相关文件
        try:
            analysis_result = self.requirement_analyzer.analyze_requirement_by_prefix(prefix, since)
            files_to_review = list(analysis_result['files'])
            commits = analysis_result['commits']
            
            print(f"📂 找到 {len(files_to_review)} 个相关文件")
            print(f"📝 涉及 {len(commits)} 个提交")
            
            if not files_to_review:
                return {
                    'prefix': prefix,
                    'files_reviewed': [],
                    'reviews': {},
                    'summary': '未找到相关文件'
                }
        
        except Exception as e:
            print(f"❌ Git分析失败: {e}")
            return {
                'prefix': prefix,
                'error': str(e),
                'files_reviewed': [],
                'reviews': {}
            }
        
        # 2. 对每个文件进行代码审查
        review_results = {}
        successful_reviews = 0
        
        for file_path in files_to_review:
            print(f"\n📄 正在审查文件: {file_path}")
            
            # 读取文件内容
            full_path = os.path.join(self.repo_path, file_path)
            if not os.path.exists(full_path):
                print(f"⚠️  文件不存在，跳过: {file_path}")
                continue
            
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()
                
                if not file_content.strip():
                    print(f"⚠️  文件为空，跳过: {file_path}")
                    continue
                
                # 检测编程语言
                language = self._detect_language(file_path)
                
                # 进行多种类型的审查
                file_reviews = {}
                for review_type in review_types:
                    try:
                        review_result = self._perform_single_review(
                            file_content, language, review_type, file_path
                        )
                        file_reviews[review_type] = review_result
                        print(f"✅ {review_type} 审查完成")
                    except Exception as e:
                        print(f"❌ {review_type} 审查失败: {e}")
                        file_reviews[review_type] = {'error': str(e)}
                
                review_results[file_path] = {
                    'language': language,
                    'reviews': file_reviews,
                    'file_size': len(file_content)
                }
                successful_reviews += 1
                
            except Exception as e:
                print(f"❌ 读取文件失败 {file_path}: {e}")
                review_results[file_path] = {'error': str(e)}
        
        # 3. 生成综合报告
        summary = self._generate_summary_report(
            prefix, commits, review_results, successful_reviews
        )
        
        return {
            'prefix': prefix,
            'timestamp': datetime.now().isoformat(),
            'commits_analyzed': len(commits),
            'files_reviewed': successful_reviews,
            'total_files_found': len(files_to_review),
            'reviews': review_results,
            'summary': summary,
            'git_analysis': analysis_result
        }
    
    def _perform_single_review(self, 
                              code: str, 
                              language: str, 
                              review_type: str,
                              file_path: str) -> Dict[str, Any]:
        """执行单项审查"""
        
        # 生成对应的提示词
        if review_type == 'code_review':
            prompt = self.prompt_builder.build_review_prompt(
                code=code,
                language=language,
                focus_areas=[
                    f"文件 {file_path} 的代码质量",
                    "可读性和可维护性",
                    "潜在的改进机会"
                ]
            )
        elif review_type == 'bug_detection':
            prompt = create_bug_detection_prompt(code, language)
        elif review_type == 'security_check':
            prompt = create_security_check_prompt(code, language)
        elif review_type == 'performance_analysis':
            prompt = create_performance_analysis_prompt(code, language)
        else:
            raise ValueError(f"不支持的审查类型: {review_type}")
        
        # 使用AI进行分析
        ai_response = self.ai_router.chat(prompt, use_history=False)
        
        return {
            'type': review_type,
            'file_path': file_path,
            'language': language,
            'ai_response': ai_response,
            'timestamp': datetime.now().isoformat()
        }
    
    def _detect_language(self, file_path: str) -> str:
        """检测文件的编程语言"""
        extension = os.path.splitext(file_path)[1].lower()
        
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.html': 'html',
            '.css': 'css',
            '.sql': 'sql',
            '.sh': 'bash',
            '.yml': 'yaml',
            '.yaml': 'yaml',
            '.json': 'json',
            '.xml': 'xml',
            '.md': 'markdown'
        }
        
        return language_map.get(extension, 'text')
    
    def _generate_summary_report(self, 
                                prefix: str, 
                                commits: List, 
                                review_results: Dict,
                                successful_reviews: int) -> Dict[str, Any]:
        """生成综合报告摘要"""
        
        # 统计审查结果
        total_issues = 0
        high_priority_issues = 0
        language_stats = {}
        
        for file_path, file_result in review_results.items():
            if 'error' in file_result:
                continue
            
            language = file_result.get('language', 'unknown')
            language_stats[language] = language_stats.get(language, 0) + 1
            
            # 简单的问题统计（基于关键词）
            for review_type, review_data in file_result.get('reviews', {}).items():
                if 'error' in review_data:
                    continue
                
                response = review_data.get('ai_response', '').lower()
                if any(keyword in response for keyword in ['错误', 'bug', '问题', '风险', '漏洞']):
                    total_issues += 1
                
                if any(keyword in response for keyword in ['严重', '高风险', '紧急', '重要']):
                    high_priority_issues += 1
        
        return {
            'prefix': prefix,
            'total_commits': len(commits),
            'files_reviewed': successful_reviews,
            'total_issues_found': total_issues,
            'high_priority_issues': high_priority_issues,
            'languages_analyzed': language_stats,
            'review_timestamp': datetime.now().isoformat()
        }
    
    def review_recent_changes(self, 
                             days: int = 7,
                             author: Optional[str] = None) -> Dict[str, Any]:
        """审查最近的代码变更"""
        
        since = f"{days} days ago"
        print(f"🔍 审查最近 {days} 天的代码变更")
        
        # 获取最近的提交
        try:
            command = ['log', '--oneline', '--pretty=format:%H|%an|%ae|%ad|%s', 
                      '--date=iso', f'--since={since}']
            
            if author:
                command.extend(['--author', author])
            
            output = self.git_analyzer._run_git_command(command)
            
            if not output:
                return {'message': '未找到最近的提交记录'}
            
            # 获取修改的文件
            recent_files = set()
            commit_count = 0
            
            for line in output.split('\n')[:10]:  # 限制最近10个提交
                if not line.strip():
                    continue
                
                commit_hash = line.split('|')[0]
                
                # 获取该提交修改的文件
                files_output = self.git_analyzer._run_git_command([
                    'show', '--name-only', '--format=', commit_hash
                ])
                
                for file_path in files_output.split('\n'):
                    if file_path.strip() and self._is_code_file(file_path.strip()):
                        recent_files.add(file_path.strip())
                
                commit_count += 1
            
            # 对文件进行审查
            return self._review_files_list(list(recent_files), f"最近{days}天的变更")
            
        except Exception as e:
            return {'error': f'获取最近变更失败: {e}'}
    
    def _is_code_file(self, file_path: str) -> bool:
        """判断是否为代码文件"""
        code_extensions = {
            '.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', 
            '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala'
        }
        
        extension = os.path.splitext(file_path)[1].lower()
        return extension in code_extensions
    
    def _review_files_list(self, files: List[str], context: str) -> Dict[str, Any]:
        """审查指定的文件列表"""
        print(f"📂 开始审查 {len(files)} 个文件 - {context}")
        
        review_results = {}
        successful_reviews = 0
        
        for file_path in files:
            full_path = os.path.join(self.repo_path, file_path)
            
            if not os.path.exists(full_path):
                continue
            
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                if len(content.strip()) < 50:  # 跳过太短的文件
                    continue
                
                language = self._detect_language(file_path)
                
                # 进行代码审查
                review_result = self._perform_single_review(
                    content, language, 'code_review', file_path
                )
                
                review_results[file_path] = {
                    'language': language,
                    'review': review_result,
                    'file_size': len(content)
                }
                successful_reviews += 1
                print(f"✅ 完成审查: {file_path}")
                
            except Exception as e:
                print(f"❌ 审查失败 {file_path}: {e}")
                review_results[file_path] = {'error': str(e)}
        
        return {
            'context': context,
            'files_reviewed': successful_reviews,
            'total_files': len(files),
            'reviews': review_results,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_timestamp(self) -> str:
        """获取当前时间戳字符串"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def export_review_report(self, review_result: Dict[str, Any], 
                           output_file: Optional[str] = None) -> str:
        """导出审查报告"""
        
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"code_review_report_{timestamp}.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(review_result, f, ensure_ascii=False, indent=2)
            
            print(f"📋 审查报告已导出: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"❌ 导出报告失败: {e}")
            return ""
    
    def generate_markdown_report(self, review_result: Dict[str, Any]) -> str:
        """生成Markdown格式的审查报告"""
        report_generator = MarkdownReportGenerator()
        return report_generator.generate_single_prefix_report(review_result)


def interactive_review_menu():
    """交互式审查菜单"""
    
    print("🤖 智能代码审查系统")
    print("=" * 50)
    
    # 初始化审查器
    try:
        reviewer = SmartCodeReviewer()
        print("✅ 系统初始化成功")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return
    
    while True:
        print("\n📝 请选择审查方式:")
        print("1. 根据提交前缀审查 (如: feat:, fix:, JIRA-123:)")
        print("2. 审查最近的代码变更")
        print("3. 审查指定文件")
        print("4. 测试AI连接")
        print("5. 退出")
        
        choice = input("\n请选择 (1-5): ").strip()
        
        if choice == '1':
            prefix = input("请输入提交前缀 (如: feat:, fix:): ").strip()
            if not prefix:
                print("❌ 前缀不能为空")
                continue
            
            since = input("时间范围 (默认: 1 week ago): ").strip() or "1 week ago"
            
            print(f"\n🔍 开始审查提交前缀: {prefix}")
            try:
                result = reviewer.review_by_commit_prefix(prefix, since)
                
                # 显示结果摘要
                print(f"\n📊 审查完成:")
                print(f"- 审查文件数: {result.get('files_reviewed', 0)}")
                print(f"- 发现文件数: {result.get('total_files_found', 0)}")
                
                # 询问是否导出报告
                export = input("\n是否导出详细报告? (y/n): ").strip().lower()
                if export == 'y':
                    report_file = reviewer.export_review_report(result)
                    if report_file:
                        print(f"✅ 报告已保存: {report_file}")
                
            except Exception as e:
                print(f"❌ 审查失败: {e}")
        
        elif choice == '2':
            days = input("审查最近几天的变更 (默认: 7): ").strip()
            try:
                days = int(days) if days else 7
            except ValueError:
                days = 7
            
            print(f"\n🔍 开始审查最近 {days} 天的变更")
            try:
                result = reviewer.review_recent_changes(days)
                
                print(f"\n📊 审查完成:")
                print(f"- 审查文件数: {result.get('files_reviewed', 0)}")
                
                # 询问是否导出报告
                export = input("\n是否导出详细报告? (y/n): ").strip().lower()
                if export == 'y':
                    report_file = reviewer.export_review_report(result)
                    if report_file:
                        print(f"✅ 报告已保存: {report_file}")
                
            except Exception as e:
                print(f"❌ 审查失败: {e}")
        
        elif choice == '3':
            file_path = input("请输入文件路径: ").strip()
            if not file_path:
                print("❌ 文件路径不能为空")
                continue
            
            if not os.path.exists(file_path):
                print("❌ 文件不存在")
                continue
            
            try:
                result = reviewer._review_files_list([file_path], f"指定文件: {file_path}")
                
                print(f"\n📊 审查完成:")
                print(f"- 审查文件数: {result.get('files_reviewed', 0)}")
                
                # 显示审查结果
                for path, review in result.get('reviews', {}).items():
                    if 'error' not in review:
                        print(f"\n📄 {path}:")
                        print(review['review']['ai_response'][:200] + "...")
                
            except Exception as e:
                print(f"❌ 审查失败: {e}")
        
        elif choice == '4':
            print("\n🔧 测试AI连接...")
            try:
                if reviewer.ai_router.test_connection():
                    print("✅ AI连接正常")
                else:
                    print("❌ AI连接失败")
            except Exception as e:
                print(f"❌ 测试失败: {e}")
        
        elif choice == '5':
            print("👋 再见！")
            break
        
        else:
            print("❌ 无效选择，请重新输入")


def demo_smart_review():
    """演示智能审查功能"""
    
    print("🎬 智能代码审查演示")
    print("=" * 40)
    
    try:
        # 初始化审查器
        reviewer = SmartCodeReviewer()
        
        # 演示1: 审查当前项目的文件
        print("\n1️⃣ 演示: 审查当前项目的Python文件")
        
        current_files = []
        for file in os.listdir('.'):
            if file.endswith('.py') and not file.startswith('test_'):
                current_files.append(file)
        
        if current_files:
            # 选择一个文件进行演示
            demo_file = current_files[0]
            print(f"📄 演示审查文件: {demo_file}")
            
            result = reviewer._review_files_list([demo_file], "演示审查")
            
            print(f"✅ 审查完成，文件数: {result.get('files_reviewed', 0)}")
            
            # 显示部分结果
            for path, review in result.get('reviews', {}).items():
                if 'error' not in review:
                    response = review['review']['ai_response']
                    print(f"\n📋 {path} 审查结果预览:")
                    print(response[:300] + "..." if len(response) > 300 else response)
        
        # 演示2: 如果是Git仓库，演示按前缀审查
        if os.path.exists('.git'):
            print(f"\n2️⃣ 演示: Git提交前缀审查")
            
            # 尝试一些常见的前缀
            common_prefixes = ['feat:', 'fix:', 'update:', 'add:']
            
            for prefix in common_prefixes:
                try:
                    result = reviewer.review_by_commit_prefix(prefix, since="1 month ago")
                    if result.get('files_reviewed', 0) > 0:
                        print(f"✅ 找到前缀 '{prefix}' 的提交，审查了 {result['files_reviewed']} 个文件")
                        break
                except:
                    continue
            else:
                print("ℹ️  未找到最近的提交记录")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")


def main():
    """主函数"""
    
    print("🚀 智能代码审查系统")
    print("=" * 50)
    print("整合 AI路由器 + 提示词模板 + Git分析器")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        # 命令行模式
        if sys.argv[1] == 'demo':
            demo_smart_review()
        elif sys.argv[1] == 'interactive':
            interactive_review_menu()
        elif sys.argv[1] == 'prefix' and len(sys.argv) > 2:
            prefix = sys.argv[2]
            since = sys.argv[3] if len(sys.argv) > 3 else "1 week ago"
            
            reviewer = SmartCodeReviewer()
            result = reviewer.review_by_commit_prefix(prefix, since)
            print(f"审查完成，文件数: {result.get('files_reviewed', 0)}")
            reviewer.export_review_report(result)
        else:
            print("使用方法:")
            print("  python ai_code_reviewer.py demo        - 运行演示")
            print("  python ai_code_reviewer.py interactive - 交互式模式")
            print("  python ai_code_reviewer.py prefix <前缀> [时间] - 按前缀审查")
    else:
        # 默认交互式模式
        interactive_review_menu()


if __name__ == "__main__":
    main()
