#!/usr/bin/env python3
"""
📝 Markdown报告生成器模块

提供统一的Markdown报告生成功能，支持：
- 单前缀代码审查报告
- 多前缀综合审查报告
- 自定义报告格式
- 统计信息和摘要生成
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
import os


class MarkdownReportGenerator:
    """Markdown报告生成器"""
    
    def __init__(self):
        self.default_emojis = {
            'title': '🔍',
            'summary': '📊', 
            'info': '📋',
            'files': '📂',
            'details': '🔍',
            'file': '📄',
            'conclusion': '📈',
            'complete': '✅',
            'no_record': 'ℹ️',
            'prefix': '🏷️'
        }
    
    def generate_single_prefix_report(self, 
                                    review_result: Dict[str, Any], 
                                    title: str = "智能代码审查报告") -> str:
        """
        生成单前缀审查报告
        
        Args:
            review_result: 审查结果数据
            title: 报告标题
            
        Returns:
            Markdown格式的报告字符串
        """
        md_content = []
        
        # 报告标题和基本信息
        md_content.append(f"# {self.default_emojis['title']} {title}")
        md_content.append(f"\n**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 审查范围
        if 'prefix' in review_result:
            md_content.append(f"\n**审查范围**: {review_result['prefix']}")
        
        # 审查摘要
        if 'summary' in review_result:
            summary = review_result['summary']
            md_content.append(f"\n## {self.default_emojis['summary']} 审查摘要")
            md_content.append(f"- 审查文件数: {summary.get('files_reviewed', 0)}")
            md_content.append(f"- 发现问题数: {summary.get('total_issues_found', 0)}")
            md_content.append(f"- 高优先级问题: {summary.get('high_priority_issues', 0)}")
        
        # 详细审查结果
        md_content.append(f"\n## {self.default_emojis['details']} 详细审查结果")
        
        for file_path, file_result in review_result.get('reviews', {}).items():
            if 'error' in file_result:
                continue
                
            md_content.append(f"\n### {self.default_emojis['file']} {file_path}")
            md_content.append(f"**语言**: {file_result.get('language', 'unknown')}")
            
            # 处理多种审查类型
            if 'reviews' in file_result:
                for review_type, review_data in file_result['reviews'].items():
                    if 'error' not in review_data:
                        md_content.append(f"\n#### {review_type.replace('_', ' ').title()}")
                        md_content.append(review_data.get('ai_response', ''))
            elif 'review' in file_result:
                # 单一审查结果
                md_content.append(f"\n#### 审查结果")
                md_content.append(file_result['review'].get('ai_response', ''))
        
        return '\n'.join(md_content)
    
    def generate_multi_prefix_report(self, 
                                   all_results: Dict[str, Dict[str, Any]], 
                                   prefixes: List[str],
                                   project_path: Optional[str] = None,
                                   time_range: str = "最近2周") -> str:
        """
        生成多前缀综合审查报告
        
        Args:
            all_results: 所有前缀的审查结果
            prefixes: 前缀列表
            project_path: 项目路径
            time_range: 时间范围描述
            
        Returns:
            Markdown格式的报告字符串
        """
        # 报告头部
        report = f"""# {self.default_emojis['title']} 多前缀Git提交代码审查报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**项目路径**: {project_path or '当前目录'}
**审查范围**: {time_range}的提交记录
**匹配前缀**: {', '.join(prefixes)}

---

## {self.default_emojis['summary']} 审查概览

| 前缀类型 | 审查文件数 | 分析提交数 | 状态 |
|---------|-----------|-----------|------|
"""
        
        total_files = 0
        total_commits = 0
        
        # 添加统计表格
        for prefix in prefixes:
            if prefix in all_results:
                result = all_results[prefix]
                files_count = result.get('files_reviewed', 0)
                commits_count = result.get('commits_analyzed', 0)
                total_files += files_count
                total_commits += commits_count
                status = f"{self.default_emojis['complete']} 完成"
            else:
                files_count = 0
                commits_count = 0
                status = f"{self.default_emojis['no_record']} 无记录"
            
            report += f"| `{prefix}` | {files_count} | {commits_count} | {status} |\n"
        
        report += f"""
**总计**: {total_files} 个文件，{total_commits} 个提交

---

"""
        
        # 为每个前缀生成详细报告
        for prefix in prefixes:
            if prefix not in all_results:
                continue
                
            result = all_results[prefix]
            report += f"""## {self.default_emojis['prefix']} {prefix} 相关提交审查

### {self.default_emojis['info']} 基本信息
- **审查文件数**: {result.get('files_reviewed', 0)}
- **分析提交数**: {result.get('commits_analyzed', 0)}
- **审查时间**: {result.get('review_time', 'N/A')}

### {self.default_emojis['files']} 涉及文件列表
"""
            
            # 列出审查的文件
            if 'reviews' in result:
                for file_path, file_result in result['reviews'].items():
                    if 'error' not in file_result:
                        language = file_result.get('language', 'unknown')
                        report += f"- `{file_path}` ({language})\n"
            
            report += f"\n### {self.default_emojis['details']} 审查结果详情\n\n"
            
            # 添加每个文件的审查结果
            report += self._generate_file_reviews(result.get('reviews', {}))
            
            report += "---\n\n"
        
        # 添加报告尾部
        report += self._generate_summary_and_suggestions(total_files, total_commits, prefixes, all_results)
        
        return report
    
    def _generate_file_reviews(self, reviews: Dict[str, Any]) -> str:
        """生成文件审查详情部分"""
        content = ""
        
        for file_path, file_result in reviews.items():
            if 'error' in file_result:
                continue
                
            content += f"#### {self.default_emojis['file']} {file_path}\n\n"
            
            # 添加每种审查类型的结果
            if 'reviews' in file_result:
                for review_type, review_data in file_result['reviews'].items():
                    if 'error' not in review_data:
                        ai_response = review_data.get('ai_response', '')
                        content += f"**{review_type.replace('_', ' ').title()}**:\n\n"
                        content += f"{ai_response}\n\n"
            elif 'review' in file_result:
                # 单一审查结果
                ai_response = file_result['review'].get('ai_response', '')
                content += f"{ai_response}\n\n"
        
        return content
    
    def _generate_summary_and_suggestions(self, 
                                        total_files: int, 
                                        total_commits: int, 
                                        prefixes: List[str], 
                                        all_results: Dict[str, Any]) -> str:
        """生成总结与建议部分"""
        
        matched_prefixes = [p for p in prefixes if p in all_results]
        
        return f"""## {self.default_emojis['conclusion']} 总结与建议

### {self.default_emojis['summary']} 审查总览
本次多前缀审查共分析了 **{total_files}** 个文件和 **{total_commits}** 个提交，覆盖了以下提交类型：
{', '.join([f"`{p}`" for p in matched_prefixes])}

### 💡 改进建议
基于本次审查结果，建议关注以下方面：
1. **代码质量**: 持续关注代码规范和最佳实践
2. **安全性检查**: 定期进行安全漏洞扫描
3. **性能优化**: 关注潜在的性能瓶颈
4. **文档完善**: 保持代码文档的及时更新

### 🔄 后续行动
- [ ] 审查并修复发现的问题
- [ ] 更新相关文档
- [ ] 优化代码结构
- [ ] 加强测试覆盖

---
*报告由智能代码审查系统自动生成*
"""
    
    def generate_custom_report(self, 
                             title: str,
                             sections: List[Dict[str, str]],
                             metadata: Optional[Dict[str, str]] = None) -> str:
        """
        生成自定义格式报告
        
        Args:
            title: 报告标题
            sections: 报告章节列表，每个章节包含 {'title': '标题', 'content': '内容'}
            metadata: 元数据信息
            
        Returns:
            Markdown格式的报告字符串
        """
        md_content = []
        
        # 标题
        md_content.append(f"# {title}")
        md_content.append(f"\n**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 添加元数据
        if metadata:
            for key, value in metadata.items():
                md_content.append(f"**{key}**: {value}")
        
        md_content.append("\n---\n")
        
        # 添加章节
        for section in sections:
            section_title = section.get('title', '未命名章节')
            section_content = section.get('content', '')
            
            md_content.append(f"## {section_title}")
            md_content.append(f"{section_content}\n")
        
        return '\n'.join(md_content)
    
    def save_report(self, 
                   report_content: str, 
                   filename: Optional[str] = None,
                   output_dir: str = ".") -> str:
        """
        保存报告到文件
        
        Args:
            report_content: 报告内容
            filename: 文件名，如不指定则自动生成
            output_dir: 输出目录
            
        Returns:
            保存的文件路径
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"code_review_report_{timestamp}.md"
        
        # 确保文件名以.md结尾
        if not filename.endswith('.md'):
            filename += '.md'
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        file_path = os.path.join(output_dir, filename)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            return file_path
        except Exception as e:
            raise Exception(f"保存报告失败: {e}")


# 便捷函数
def generate_single_report(review_result: Dict[str, Any], 
                         title: str = "智能代码审查报告") -> str:
    """便捷函数：生成单前缀报告"""
    generator = MarkdownReportGenerator()
    return generator.generate_single_prefix_report(review_result, title)


def generate_multi_report(all_results: Dict[str, Dict[str, Any]], 
                        prefixes: List[str],
                        project_path: Optional[str] = None,
                        time_range: str = "最近2周") -> str:
    """便捷函数：生成多前缀报告"""
    generator = MarkdownReportGenerator()
    return generator.generate_multi_prefix_report(all_results, prefixes, project_path, time_range)


def save_markdown_report(report_content: str, 
                        filename: Optional[str] = None,
                        output_dir: str = ".") -> str:
    """便捷函数：保存报告"""
    generator = MarkdownReportGenerator()
    return generator.save_report(report_content, filename, output_dir)


if __name__ == "__main__":
    # 示例用法
    print("📝 Markdown报告生成器模块")
    print("=" * 50)
    
    # 创建示例报告
    generator = MarkdownReportGenerator()
    
    # 示例：自定义报告
    custom_sections = [
        {
            'title': '📊 测试结果概览',
            'content': '本次测试包含了多个模块的功能验证...'
        },
        {
            'title': '🔍 详细分析',
            'content': '经过深入分析，发现以下关键问题...'
        }
    ]
    
    custom_report = generator.generate_custom_report(
        title="📝 测试报告示例",
        sections=custom_sections,
        metadata={
            "项目": "智能代码审查系统",
            "版本": "v1.0",
            "测试环境": "Windows 11"
        }
    )
    
    print("✅ 示例报告生成成功!")
    print("💡 使用方法:")
    print("   from markdown_generator import MarkdownReportGenerator")
    print("   generator = MarkdownReportGenerator()")
    print("   report = generator.generate_single_prefix_report(data)")
