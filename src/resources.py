"""
MCP 资源模块 - 定义服务器提供的所有资源
"""

import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def register_resources(mcp, data_handler):
    """
    注册所有 MCP 资源
    
    Args:
        mcp: FastMCP 服务器实例
        data_handler: 数据处理器实例
    """
    
    @mcp.resource("modifiers://")
    def get_all_modifiers() -> str:
        """
        获取所有修改器列表资源
        
        Returns:
            JSON 格式的所有修改器
        """
        if not data_handler:
            return json.dumps({"error": "Data handler not initialized"}, ensure_ascii=False)
        
        try:
            return json.dumps({
                "type": "modifiers",
                "count": len(data_handler.modifiers),
                "data": data_handler.modifiers[:100]  # 返回前100个以避免超大响应
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error in get_all_modifiers: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.resource("effects://")
    def get_all_effects() -> str:
        """
        获取所有效果列表资源
        
        Returns:
            JSON 格式的所有效果
        """
        if not data_handler:
            return json.dumps({"error": "Data handler not initialized"}, ensure_ascii=False)
        
        try:
            return json.dumps({
                "type": "effects",
                "count": len(data_handler.effects),
                "data": data_handler.effects[:100]  # 返回前100个以避免超大响应
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error in get_all_effects: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.resource("triggers://")
    def get_all_triggers() -> str:
        """
        获取所有触发条件列表资源
        
        Returns:
            JSON 格式的所有触发条件
        """
        if not data_handler:
            return json.dumps({"error": "Data handler not initialized"}, ensure_ascii=False)
        
        try:
            return json.dumps({
                "type": "triggers",
                "count": len(data_handler.triggers),
                "data": data_handler.triggers[:100]  # 返回前100个以避免超大响应
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error in get_all_triggers: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.resource("event-targets://")
    def get_all_event_targets() -> str:
        """
        获取所有事件目标列表资源
        
        Returns:
            JSON 格式的所有事件目标
        """
        if not data_handler:
            return json.dumps({"error": "Data handler not initialized"}, ensure_ascii=False)
        
        try:
            return json.dumps({
                "type": "event_targets",
                "count": len(data_handler.event_targets),
                "data": data_handler.event_targets
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error in get_all_event_targets: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.resource("data-types-common://")
    def get_data_types_common() -> str:
        """
        获取通用数据类型资源
        
        Returns:
            JSON 格式的通用数据类型
        """
        if not data_handler:
            return json.dumps({"error": "Data handler not initialized"}, ensure_ascii=False)
        
        try:
            data = data_handler.get_data_types_by_category('common')
            return json.dumps({
                "type": "data_types_common",
                "count": len(data),
                "data": data[:100]  # 返回前100个以避免超大响应
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error in get_data_types_common: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.resource("data-types-gui://")
    def get_data_types_gui() -> str:
        """
        获取 GUI 数据类型资源
        
        Returns:
            JSON 格式的 GUI 数据类型
        """
        if not data_handler:
            return json.dumps({"error": "Data handler not initialized"}, ensure_ascii=False)
        
        try:
            data = data_handler.get_data_types_by_category('gui')
            return json.dumps({
                "type": "data_types_gui",
                "count": len(data),
                "data": data[:100]  # 返回前100个以避免超大响应
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error in get_data_types_gui: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.resource("data-types-script://")
    def get_data_types_script() -> str:
        """
        获取脚本数据类型资源
        
        Returns:
            JSON 格式的脚本数据类型
        """
        if not data_handler:
            return json.dumps({"error": "Data handler not initialized"}, ensure_ascii=False)
        
        try:
            data = data_handler.get_data_types_by_category('script')
            return json.dumps({
                "type": "data_types_script",
                "count": len(data),
                "data": data[:100]  # 返回前100个以避免超大响应
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error in get_data_types_script: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.resource("statistics://")
    def get_server_statistics() -> str:
        """
        获取服务器数据统计资源
        
        Returns:
            JSON 格式的数据统计信息
        """
        if not data_handler:
            return json.dumps({"error": "Data handler not initialized"}, ensure_ascii=False)
        
        try:
            stats = data_handler.get_statistics()
            return json.dumps({
                "type": "statistics",
                "data": stats
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error in get_server_statistics: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    logger.info("Resources registered successfully")
