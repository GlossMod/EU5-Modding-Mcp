#!/usr/bin/env python3
"""
将 docs 中的数据文件转换为 JSON 格式，便于模糊查询
支持: data_types/*.txt 和 *.log 文件
"""

import json
import os
import re
from pathlib import Path
from typing import List, Dict, Any


def parse_data_type_file(file_path: str) -> List[Dict[str, Any]]:
    """
    解析数据类型文本文件 (data_types/*.txt)，返回结构化数据列表
    
    Args:
        file_path: 文本文件路径
        
    Returns:
        包含解析数据的列表
    """
    entries = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用 "-----------------------" 作为分隔符分割条目
    items = content.split('-----------------------\n')
    
    for item in items:
        item = item.strip()
        if not item:
            continue
        
        lines = item.split('\n')
        entry = {
            'name': '',
            'description': '',
            'definition_type': '',
            'return_type': '',
            'args': [],
            'type': 'data_type'
        }
        
        # 第一行通常是名称（可能包含参数）
        first_line = lines[0].strip()
        
        # 检查是否包含函数参数
        match = re.match(r'(\w+)\(\s*(.*?)\s*\)', first_line)
        if match:
            entry['name'] = match.group(1)
            args_str = match.group(2)
            if args_str:
                entry['args'] = [arg.strip() for arg in args_str.split(',')]
        else:
            entry['name'] = first_line
        
        # 解析其他行
        for line in lines[1:]:
            line = line.strip()
            if line.startswith('Description:'):
                entry['description'] = line.replace('Description:', '').strip()
            elif line.startswith('Definition type:'):
                entry['definition_type'] = line.replace('Definition type:', '').strip()
            elif line.startswith('Return type:'):
                entry['return_type'] = line.replace('Return type:', '').strip()
        
        if entry['name']:
            entries.append(entry)
    
    return entries


def parse_markdown_log_file(file_path: str) -> List[Dict[str, Any]]:
    """
    解析 Markdown 格式的 log 文件 (effects.log, triggers.log 等)
    
    Args:
        file_path: log 文件路径
        
    Returns:
        包含解析数据的列表
    """
    entries = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否包含 ## 标记（Markdown h2）
    if '##' not in content:
        return entries
    
    # 按 ## 分割条目
    items = re.split(r'\n##\s+', content)
    
    for item in items:
        if not item.strip():
            continue
        
        lines = item.split('\n')
        # 第一行是名称
        name = lines[0].strip()
        
        if not name:
            continue
        
        entry = {
            'name': name,
            'description': '',
            'supported_scopes': [],
            'supported_targets': [],
            'type': 'effect'  # 默认，会被覆盖
        }
        
        # 解析描述和其他字段
        description_lines = []
        for line in lines[1:]:
            line = line.rstrip()
            if line.startswith('**Supported Scopes**:'):
                scopes_str = line.replace('**Supported Scopes**:', '').strip()
                entry['supported_scopes'] = [s.strip() for s in scopes_str.split(',') if s.strip()]
            elif line.startswith('**Supported Targets**:'):
                targets_str = line.replace('**Supported Targets**:', '').strip()
                entry['supported_targets'] = [t.strip() for t in targets_str.split(',') if t.strip()]
            elif line and not line.startswith('**'):
                description_lines.append(line)
        
        entry['description'] = '\n'.join(description_lines).strip()
        
        if entry['name']:
            entries.append(entry)
    
    return entries


def parse_modifier_log_file(file_path: str) -> List[Dict[str, Any]]:
    """
    解析修饰符 log 文件 (modifiers.log)
    格式: Tag: name, Categories: cat1, cat2, ...
    
    Args:
        file_path: log 文件路径
        
    Returns:
        包含解析数据的列表
    """
    entries = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('Printing'):
            continue
        
        # 解析格式: Tag: name, Categories: cat1, cat2, ...
        match = re.match(r'Tag:\s*([^,]+),\s*Categories:\s*(.*)', line)
        if match:
            name = match.group(1).strip()
            categories_str = match.group(2).strip()
            # 提取类别（通常以逗号分隔，最后可能有 All 或空值）
            categories = [c.strip() for c in categories_str.split(',') if c.strip() and c.strip() != 'All']
            
            entry = {
                'name': name,
                'description': '',
                'categories': categories,
                'type': 'modifier'
            }
            
            entries.append(entry)
    
    return entries


def parse_log_file(file_path: str) -> List[Dict[str, Any]]:
    """
    根据文件内容类型选择合适的解析器
    
    Args:
        file_path: log 文件路径
        
    Returns:
        包含解析数据的列表
    """
    file_name = Path(file_path).stem
    
    if file_name == 'modifiers':
        return parse_modifier_log_file(file_path)
    else:
        # effects, triggers, event_targets, on_actions, custom_localization
        return parse_markdown_log_file(file_path)


def convert_all_data():
    """
    转换所有数据文件 (data_types/*.txt 和 *.log)，生成优化的 JSON 文件
    """
    docs_dir = Path('e:/GitHub/GlossMod/EU5-Modifier-Mcp/docs')
    data_types_dir = docs_dir / 'data_types'
    output_dir = Path('e:/GitHub/GlossMod/EU5-Modifier-Mcp/mcp-data')
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_data = {}
    total_count = 0
    
    # 处理 data_types 文本文件
    print("📄 处理 data_types 文件:")
    for txt_file in sorted(data_types_dir.glob('*.txt')):
        print(f"  {txt_file.name}")
        
        entries = parse_data_type_file(str(txt_file))
        category = txt_file.stem
        
        all_data[category] = entries
        total_count += len(entries)
        
        # 为每个类别生成单独的 JSON 文件
        output_file = output_dir / f"{category}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        
        print(f"    ✓ {len(entries)} 条记录")
    
    # 处理 log 文件
    print("\n📋 处理 log 文件:")
    log_files = [
        'effects.log',
        'triggers.log',
        'event_targets.log',
        'on_actions.log',
        'modifiers.log',
        'custom_localization.log'
    ]
    
    for log_filename in log_files:
        log_file = docs_dir / log_filename
        if not log_file.exists():
            continue
        
        print(f"  {log_filename}")
        entries = parse_log_file(str(log_file))
        
        if entries:
            category = log_file.stem
            all_data[category] = entries
            total_count += len(entries)
            
            # 为每个类别生成单独的 JSON 文件
            output_file = output_dir / f"{category}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(entries, f, ensure_ascii=False, indent=2)
            
            print(f"    ✓ {len(entries)} 条记录")
    
    # 生成索引文件：按名称建立快速查找表
    print("\n🔍 生成索引...")
    index_by_name = {}
    for category, entries in all_data.items():
        for entry in entries:
            name = entry['name'].lower()
            if name not in index_by_name:
                index_by_name[name] = []
            
            # 根据条目类型提取关键信息
            indexed_entry = {
                'category': category,
                'name': entry['name'],
                'description': entry.get('description', ''),
                'type': entry.get('type', 'unknown')
            }
            
            # 根据条目类型添加特定字段
            if entry.get('type') == 'data_type':
                indexed_entry['definition_type'] = entry.get('definition_type', '')
                indexed_entry['return_type'] = entry.get('return_type', '')
                indexed_entry['args'] = entry.get('args', [])
            elif entry.get('type') in ['effect', 'trigger']:
                indexed_entry['supported_scopes'] = entry.get('supported_scopes', [])
                indexed_entry['supported_targets'] = entry.get('supported_targets', [])
            elif entry.get('type') == 'event_target':
                indexed_entry['input_scopes'] = entry.get('input_scopes', [])
                indexed_entry['output_scopes'] = entry.get('output_scopes', [])
            elif entry.get('type') == 'modifier':
                indexed_entry['categories'] = entry.get('categories', [])
            
            index_by_name[name].append(indexed_entry)
    
    index_file = output_dir / 'index.json'
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_by_name, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 生成索引文件 index.json ({len(index_by_name)} 条索引)")
    
    # 生成全量数据文件用于模糊搜索
    print("\n📦 生成全量数据文件...")
    all_entries = []
    for category, entries in all_data.items():
        for entry in entries:
            entry_copy = entry.copy()
            entry_copy['category'] = category
            all_entries.append(entry_copy)
    
    all_data_file = output_dir / 'all_data.json'
    with open(all_data_file, 'w', encoding='utf-8') as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 生成全量数据文件 all_data.json ({len(all_entries)} 条记录)")
    
    print("\n" + "="*60)
    print("✅ 数据转换完成！")
    print("="*60)
    print(f"📊 总计: {total_count} 条记录")
    print(f"📁 输出目录: {output_dir}")
    print(f"📄 输出文件数: {len(list(output_dir.glob('*.json')))}")


if __name__ == '__main__':
    convert_all_data()
