#!/usr/bin/env python3
"""
模糊查询 mcp-data 中的数据
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from difflib import SequenceMatcher


class DataSearcher:
    """数据模糊查询类"""
    
    def __init__(self, data_dir: str = 'mcp-data'):
        """初始化查询器"""
        self.data_dir = Path(data_dir)
        self.index = {}
        self.all_data = []
        self._load_data()
    
    def _load_data(self):
        """加载所有数据"""
        index_file = self.data_dir / 'index.json'
        all_data_file = self.data_dir / 'all_data.json'
        
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                self.index = json.load(f)
        
        if all_data_file.exists():
            with open(all_data_file, 'r', encoding='utf-8') as f:
                self.all_data = json.load(f)
    
    def search_by_name(self, name: str, fuzzy: bool = True) -> List[Dict[str, Any]]:
        """
        按名称搜索数据
        
        Args:
            name: 搜索名称
            fuzzy: 是否使用模糊匹配
            
        Returns:
            匹配的条目列表
        """
        name_lower = name.lower()
        
        # 精确匹配
        if name_lower in self.index:
            return self.index[name_lower]
        
        if not fuzzy:
            return []
        
        # 模糊匹配
        results = []
        for key, entries in self.index.items():
            similarity = SequenceMatcher(None, name_lower, key).ratio()
            if similarity > 0.6:  # 相似度阈值
                for entry in entries:
                    entry['similarity'] = similarity
                    results.append(entry)
        
        # 按相似度排序
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:20]  # 返回前 20 条
    
    def search_by_regex(self, pattern: str) -> List[Dict[str, Any]]:
        """
        使用正则表达式搜索
        
        Args:
            pattern: 正则表达式模式
            
        Returns:
            匹配的条目列表
        """
        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error:
            return []
        
        results = []
        for entry in self.all_data:
            if regex.search(entry['name']):
                results.append(entry)
        
        return results
    
    def search_by_type(self, return_type: str) -> List[Dict[str, Any]]:
        """
        按返回类型搜索（适用于 data_type 条目）
        
        Args:
            return_type: 返回类型名称
            
        Returns:
            匹配的条目列表
        """
        return [e for e in self.all_data if e.get('return_type', '').lower() == return_type.lower()]
    
    def search_by_scopes(self, scope: str, entry_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        按支持的作用域搜索（适用于 effect、trigger 等）
        
        Args:
            scope: 作用域名称
            entry_type: 条目类型（effect/trigger/event_target）
            
        Returns:
            匹配的条目列表
        """
        results = []
        scope_lower = scope.lower()
        
        for e in self.all_data:
            # 检查 supported_scopes
            supported_scopes = e.get('supported_scopes', [])
            if any(s.lower() == scope_lower for s in supported_scopes):
                if entry_type is None or e.get('type', '').lower() == entry_type.lower():
                    results.append(e)
        
        return results
    
    def search_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        按类别搜索
        
        Args:
            category: 类别名称
            
        Returns:
            匹配的条目列表
        """
        return [e for e in self.all_data if e['category'].lower() == category.lower()]
    
    def search_by_description(self, keyword: str) -> List[Dict[str, Any]]:
        """
        按描述关键词搜索
        
        Args:
            keyword: 关键词
            
        Returns:
            匹配的条目列表
        """
        keyword_lower = keyword.lower()
        return [e for e in self.all_data if keyword_lower in e['description'].lower()]
    
    def advanced_search(self, **kwargs) -> List[Dict[str, Any]]:
        """
        高级搜索（支持多条件组合）
        
        Args:
            name: 名称（支持模糊）
            return_type: 返回类型
            category: 类别
            description: 描述关键词
            
        Returns:
            匹配的条目列表
        """
        results = self.all_data.copy()
        
        if 'name' in kwargs:
            name_results = self.search_by_name(kwargs['name'], fuzzy=True)
            result_names = {e['name'] for e in name_results}
            results = [e for e in results if e['name'] in result_names]
        
        if 'return_type' in kwargs:
            results = [e for e in results if e['return_type'].lower() == kwargs['return_type'].lower()]
        
        if 'category' in kwargs:
            results = [e for e in results if e['category'].lower() == kwargs['category'].lower()]
        
        if 'description' in kwargs:
            keyword = kwargs['description'].lower()
            results = [e for e in results if keyword in e['description'].lower()]
        
        return results


def demo():
    """演示查询功能"""
    searcher = DataSearcher()
    
    print("=" * 70)
    print("模糊查询演示 - EU5-Modifier-Mcp")
    print("=" * 70)
    
    # 演示 1: 精确搜索数据类型
    print("\n1️⃣  精确搜索数据类型 'DATE':")
    results = searcher.search_by_name('DATE', fuzzy=False)
    for r in results[:3]:
        print(f"   {r['name']} ({r['type']}) -> {r.get('return_type', 'N/A')}")
    
    # 演示 2: 模糊搜索
    print("\n2️⃣  模糊搜索 'add':")
    results = searcher.search_by_name('add', fuzzy=True)
    for r in results[:5]:
        print(f"   {r['name']} ({r['type']}) - {r.get('description', '')[:50]}...")
    
    # 演示 3: 搜索 Effects（效果）
    print("\n3️⃣  搜索 Effects 中的 'add':")
    results = [e for e in searcher.all_data if e.get('type') == 'effect' and 'add' in e['name'].lower()]
    print(f"   找到 {len(results)} 条 effect 记录")
    for r in results[:5]:
        print(f"   - {r['name']}")
    
    # 演示 4: 搜索支持某个 Scope 的 Effects
    print("\n4️⃣  搜索支持 'country' 作用域的 effects:")
    results = searcher.search_by_scopes('country', 'effect')
    print(f"   找到 {len(results)} 条记录")
    for r in results[:5]:
        print(f"   - {r['name']}")
    
    # 演示 5: 搜索修饰符
    print("\n5️⃣  搜索修饰符 'army':")
    results = [e for e in searcher.all_data if e.get('type') == 'modifier' and 'army' in e['name'].lower()]
    print(f"   找到 {len(results)} 条记录")
    for r in results[:5]:
        print(f"   - {r['name']}")
    
    # 演示 6: 搜索 Triggers
    print("\n6️⃣  搜索 Triggers 中的 'character':")
    results = [e for e in searcher.all_data if e.get('type') == 'trigger' and 'character' in e['name'].lower()]
    print(f"   找到 {len(results)} 条记录")
    for r in results[:5]:
        print(f"   - {r['name']}")
    
    # 演示 7: 按类别搜索
    print("\n7️⃣  搜索类别统计:")
    categories = {}
    for e in searcher.all_data:
        cat = e.get('type', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"   {cat}: {count} 条")


if __name__ == '__main__':
    demo()
