"""
数据处理器 - 加载和管理所有游戏数据
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class DataHandler:
    """数据处理和检索类"""
    
    def __init__(self, data_dir: Path):
        """
        初始化数据处理器
        
        Args:
            data_dir: 数据目录路径
        """
        self.data_dir = Path(data_dir)
        self.index: Dict[str, List[Dict[str, Any]]] = {}
        self.all_data: List[Dict[str, Any]] = []
        self.modifiers: List[Dict[str, Any]] = []
        self.effects: List[Dict[str, Any]] = []
        self.triggers: List[Dict[str, Any]] = []
        self.event_targets: List[Dict[str, Any]] = []
        self.data_types_by_category: Dict[str, List[Dict[str, Any]]] = {}
        
        self._load_all_data()
    
    def _load_all_data(self):
        """加载所有数据文件"""
        try:
            # 加载索引
            index_file = self.data_dir / "index.json"
            if index_file.exists():
                with open(index_file, 'r', encoding='utf-8') as f:
                    self.index = json.load(f)
                logger.info(f"Loaded index with {len(self.index)} entries")
            
            # 加载全量数据
            all_data_file = self.data_dir / "all_data.json"
            if all_data_file.exists():
                with open(all_data_file, 'r', encoding='utf-8') as f:
                    self.all_data = json.load(f)
                logger.info(f"Loaded {len(self.all_data)} data entries")
            
            # 加载修改器
            modifiers_file = self.data_dir / "modifiers.json"
            if modifiers_file.exists():
                with open(modifiers_file, 'r', encoding='utf-8') as f:
                    self.modifiers = json.load(f)
                logger.info(f"Loaded {len(self.modifiers)} modifiers")
            
            # 加载效果
            effects_file = self.data_dir / "effects.json"
            if effects_file.exists():
                with open(effects_file, 'r', encoding='utf-8') as f:
                    self.effects = json.load(f)
                logger.info(f"Loaded {len(self.effects)} effects")
            
            # 加载触发条件
            triggers_file = self.data_dir / "triggers.json"
            if triggers_file.exists():
                with open(triggers_file, 'r', encoding='utf-8') as f:
                    self.triggers = json.load(f)
                logger.info(f"Loaded {len(self.triggers)} triggers")
            
            # 加载事件目标
            event_targets_file = self.data_dir / "event_targets.json"
            if event_targets_file.exists():
                with open(event_targets_file, 'r', encoding='utf-8') as f:
                    self.event_targets = json.load(f)
                logger.info(f"Loaded {len(self.event_targets)} event targets")
            
            # 加载各类数据类型
            for category in ["common", "gui", "internalclausewitzgui", "script", "uncategorized"]:
                data_type_file = self.data_dir / f"data_types_{category}.json"
                if data_type_file.exists():
                    with open(data_type_file, 'r', encoding='utf-8') as f:
                        self.data_types_by_category[category] = json.load(f)
                    logger.info(f"Loaded {len(self.data_types_by_category[category])} data_types_{category}")
        
        except Exception as e:
            logger.error(f"Error loading data: {e}", exc_info=True)
            raise
    
    def search_by_name(self, name: str, fuzzy: bool = True, limit: int = 20) -> List[Dict[str, Any]]:
        """
        按名称搜索数据
        
        Args:
            name: 搜索名称
            fuzzy: 是否使用模糊匹配
            limit: 返回结果数量限制
            
        Returns:
            匹配的条目列表
        """
        name_lower = name.lower()
        
        # 精确匹配
        if name_lower in self.index:
            return self.index[name_lower][:limit]
        
        if not fuzzy:
            return []
        
        # 模糊匹配
        results = []
        for key, entries in self.index.items():
            similarity = SequenceMatcher(None, name_lower, key).ratio()
            if similarity > 0.6:  # 相似度阈值
                for entry in entries:
                    entry_copy = entry.copy()
                    entry_copy['similarity'] = similarity
                    results.append(entry_copy)
        
        # 按相似度排序
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:limit]
    
    def search_modifiers(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        搜索修改器
        
        Args:
            query: 搜索查询
            limit: 返回结果数量限制
            
        Returns:
            匹配的修改器列表
        """
        query_lower = query.lower()
        results = []
        
        for modifier in self.modifiers:
            if query_lower in modifier.get('name', '').lower() or \
               query_lower in modifier.get('description', '').lower():
                results.append(modifier)
        
        return results[:limit]
    
    def search_effects(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        搜索效果
        
        Args:
            query: 搜索查询
            limit: 返回结果数量限制
            
        Returns:
            匹配的效果列表
        """
        query_lower = query.lower()
        results = []
        
        for effect in self.effects:
            if query_lower in effect.get('name', '').lower() or \
               query_lower in effect.get('description', '').lower():
                results.append(effect)
        
        return results[:limit]
    
    def search_triggers(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        搜索触发条件
        
        Args:
            query: 搜索查询
            limit: 返回结果数量限制
            
        Returns:
            匹配的触发条件列表
        """
        query_lower = query.lower()
        results = []
        
        for trigger in self.triggers:
            if query_lower in trigger.get('name', '').lower() or \
               query_lower in trigger.get('description', '').lower():
                results.append(trigger)
        
        return results[:limit]
    
    def search_event_targets(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        搜索事件目标
        
        Args:
            query: 搜索查询
            limit: 返回结果数量限制
            
        Returns:
            匹配的事件目标列表
        """
        query_lower = query.lower()
        results = []
        
        for target in self.event_targets:
            if query_lower in target.get('name', '').lower() or \
               query_lower in target.get('description', '').lower():
                results.append(target)
        
        return results[:limit]
    
    def get_data_types_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        获取特定类别的数据类型
        
        Args:
            category: 数据类型类别
            
        Returns:
            该类别的数据类型列表
        """
        return self.data_types_by_category.get(category, [])
    
    def get_data_by_type(self, data_type: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        按类型获取数据
        
        Args:
            data_type: 数据类型
            limit: 返回结果数量限制
            
        Returns:
            该类型的数据列表
        """
        results = [item for item in self.all_data if item.get('type') == data_type]
        return results[:limit]
    
    def get_data_by_scope(self, scope: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        按作用域获取数据
        
        Args:
            scope: 作用域名称
            limit: 返回结果数量限制
            
        Returns:
            该作用域的数据列表
        """
        results = [item for item in self.all_data if scope in item.get('scopes', [])]
        return results[:limit]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取数据统计信息
        
        Returns:
            统计信息字典
        """
        return {
            "total_entries": len(self.all_data),
            "data_types": len([item for item in self.all_data if item.get('type') == 'data_type']),
            "effects": len(self.effects),
            "triggers": len(self.triggers),
            "modifiers": len(self.modifiers),
            "event_targets": len(self.event_targets),
            "data_type_categories": {
                "common": len(self.data_types_by_category.get('common', [])),
                "gui": len(self.data_types_by_category.get('gui', [])),
                "internalclausewitzgui": len(self.data_types_by_category.get('internalclausewitzgui', [])),
                "script": len(self.data_types_by_category.get('script', [])),
                "uncategorized": len(self.data_types_by_category.get('uncategorized', []))
            }
        }
