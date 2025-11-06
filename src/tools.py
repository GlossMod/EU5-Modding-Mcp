"""
MCP 工具模块 - 定义服务器提供的所有工具
"""

import json
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def register_tools(mcp, data_handler):
    """
    注册所有 MCP 工具
    
    Args:
        mcp: FastMCP 服务器实例
        data_handler: 数据处理器实例
    """
    
    @mcp.tool()
    def search_by_name(name: str, fuzzy: bool = True, limit: int = 20) -> str:
        """
        按名称搜索数据条目（支持模糊匹配）
        
        Args:
            name: 搜索名称
            fuzzy: 是否使用模糊匹配（默认为 True）
            limit: 返回结果数量限制（默认为 20）
        
        Returns:
            JSON 格式的搜索结果
        """
        if not data_handler:
            return json.dumps({"error": "Data handler not initialized"}, ensure_ascii=False)
        
        try:
            results = data_handler.search_by_name(name, fuzzy=fuzzy, limit=limit)
            return json.dumps({
                "query": name,
                "fuzzy": fuzzy,
                "count": len(results),
                "results": results
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error in search_by_name: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.tool()
    def search_modifiers(query: str, limit: int = 10) -> str:
        """
        搜索修改器（Modifiers）
        
        Args:
            query: 搜索查询
            limit: 返回结果数量限制（默认为 10）
        
        Returns:
            JSON 格式的修改器列表
        """
        if not data_handler:
            return json.dumps({"error": "Data handler not initialized"}, ensure_ascii=False)
        
        try:
            results = data_handler.search_modifiers(query, limit=limit)
            return json.dumps({
                "query": query,
                "count": len(results),
                "results": results
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error in search_modifiers: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.tool()
    def search_effects(query: str, limit: int = 10) -> str:
        """
        搜索游戏效果（Effects）
        
        Args:
            query: 搜索查询
            limit: 返回结果数量限制（默认为 10）
        
        Returns:
            JSON 格式的效果列表
        """
        if not data_handler:
            return json.dumps({"error": "Data handler not initialized"}, ensure_ascii=False)
        
        try:
            results = data_handler.search_effects(query, limit=limit)
            return json.dumps({
                "query": query,
                "count": len(results),
                "results": results
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error in search_effects: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.tool()
    def search_triggers(query: str, limit: int = 10) -> str:
        """
        搜索触发条件（Triggers）
        
        Args:
            query: 搜索查询
            limit: 返回结果数量限制（默认为 10）
        
        Returns:
            JSON 格式的触发条件列表
        """
        if not data_handler:
            return json.dumps({"error": "Data handler not initialized"}, ensure_ascii=False)
        
        try:
            results = data_handler.search_triggers(query, limit=limit)
            return json.dumps({
                "query": query,
                "count": len(results),
                "results": results
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error in search_triggers: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.tool()
    def search_event_targets(query: str, limit: int = 10) -> str:
        """
        搜索事件目标（Event Targets）
        
        Args:
            query: 搜索查询
            limit: 返回结果数量限制（默认为 10）
        
        Returns:
            JSON 格式的事件目标列表
        """
        if not data_handler:
            return json.dumps({"error": "Data handler not initialized"}, ensure_ascii=False)
        
        try:
            results = data_handler.search_event_targets(query, limit=limit)
            return json.dumps({
                "query": query,
                "count": len(results),
                "results": results
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error in search_event_targets: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.tool()
    def search_by_type(data_type: str, limit: int = 20) -> str:
        """
        按数据类型搜索数据
        
        Args:
            data_type: 数据类型（如 'data_type', 'effect', 'trigger', 'modifier'）
            limit: 返回结果数量限制（默认为 20）
        
        Returns:
            JSON 格式的数据列表
        """
        if not data_handler:
            return json.dumps({"error": "Data handler not initialized"}, ensure_ascii=False)
        
        try:
            results = data_handler.get_data_by_type(data_type, limit=limit)
            return json.dumps({
                "data_type": data_type,
                "count": len(results),
                "results": results
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error in search_by_type: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.tool()
    def search_by_scope(scope: str, limit: int = 20) -> str:
        """
        按作用域（Scope）搜索数据
        
        Args:
            scope: 作用域名称（如 'country', 'province', 'global'）
            limit: 返回结果数量限制（默认为 20）
        
        Returns:
            JSON 格式的数据列表
        """
        if not data_handler:
            return json.dumps({"error": "Data handler not initialized"}, ensure_ascii=False)
        
        try:
            results = data_handler.get_data_by_scope(scope, limit=limit)
            return json.dumps({
                "scope": scope,
                "count": len(results),
                "results": results
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error in search_by_scope: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.tool()
    def get_data_types_by_category(category: str) -> str:
        """
        获取特定类别的数据类型
        
        Args:
            category: 数据类型类别（common, gui, internalclausewitzgui, script, uncategorized）
        
        Returns:
            JSON 格式的数据类型列表
        """
        if not data_handler:
            return json.dumps({"error": "Data handler not initialized"}, ensure_ascii=False)
        
        try:
            results = data_handler.get_data_types_by_category(category)
            return json.dumps({
                "category": category,
                "count": len(results),
                "results": results
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error in get_data_types_by_category: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.tool()
    def get_statistics() -> str:
        """
        获取数据统计信息
        
        Returns:
            JSON 格式的统计信息
        """
        if not data_handler:
            return json.dumps({"error": "Data handler not initialized"}, ensure_ascii=False)
        
        try:
            stats = data_handler.get_statistics()
            return json.dumps({
                "statistics": stats
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error in get_statistics: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    logger.info("Tools registered successfully")
