import json
import logging
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent, ImageContent

from src.tools import register_tools
from src.resources import register_resources
from src.data_handler import DataHandler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建 MCP 服务器
mcp = FastMCP("EU5ModifierMCP")

# 初始化数据处理器
data_handler = None


def initialize_data_handler():
    """初始化数据处理器"""
    global data_handler
    try:
        # 获取 mcp-data 目录路径
        base_path = Path(__file__).parent / "mcp-data"
        data_handler = DataHandler(base_path)
        logger.info(f"Data handler initialized with path: {base_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize data handler: {e}")
        return False


def register_all_features():
    """注册所有功能（工具和资源）"""
    if not initialize_data_handler():
        logger.warning("Data handler initialization failed, some features may be unavailable")
    
    # 注册工具
    register_tools(mcp, data_handler)
    logger.info("Tools registered successfully")
    
    # 注册资源
    register_resources(mcp, data_handler)
    logger.info("Resources registered successfully")


@mcp.tool()
def ping() -> str:
    """
    检查服务器是否正常运行
    
    Returns:
        str: 服务器状态确认
    """
    return "EU5 Modifier MCP Server is running successfully!"


@mcp.tool()
def get_server_info() -> str:
    """
    获取服务器信息和功能概览
    
    Returns:
        str: 服务器信息和可用功能列表
    """
    info = {
        "name": "EU5 Modifier MCP Server",
        "version": "2.0.0",
        "description": "Model Context Protocol server for Europa Universalis V modding",
        "features": [
            "搜索修改器（Modifiers）",
            "搜索游戏效果（Effects）",
            "搜索触发条件（Triggers）",
            "搜索事件目标（Event Targets）",
            "按作用域（Scopes）搜索",
            "按类别搜索数据类型",
            "模糊搜索和高级搜索",
            "获取数据统计和文件列表"
        ],
        "data_sources": {
            "total_entries": 29122,
            "by_type": {
                "data_type": 24442,
                "effect": 1324,
                "modifier": 1855,
                "trigger": 1500,
                "event_target": 1
            }
        },
        "data_files": [
            "index.json - 按名称快速索引（27085 条）",
            "all_data.json - 全量数据（29122 条）",
            "data_types_common.json - 通用数据类型",
            "data_types_gui.json - GUI 数据类型",
            "data_types_internalclausewitzgui.json - 内部 GUI 数据类型",
            "data_types_script.json - 脚本数据类型",
            "data_types_uncategorized.json - 未分类数据类型",
            "effects.json - 游戏效果（1324 条）",
            "triggers.json - 触发条件（1500 条）",
            "modifiers.json - 修改器（1855 条）",
            "event_targets.json - 事件目标"
        ]
    }
    return json.dumps(info, ensure_ascii=False, indent=2)






def main():
    """MCP 服务器入口点"""
    logger.info("Starting EU5 Modifier MCP Server...")
    
    # 注册所有功能
    register_all_features()
    
    # 运行服务器
    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
