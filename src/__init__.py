"""
EU5 Modifier MCP Server - 欧陆风云5模组修改器 MCP 服务器

这是一个 Model Context Protocol (MCP) 服务器，为 Claude 等 AI 助手提供欧陆风云 V 游戏数据访问接口。
"""

__version__ = "2.0.0"
__author__ = "GlossMod"
__all__ = ["DataHandler", "register_tools", "register_resources"]

from .data_handler import DataHandler
from .tools import register_tools
from .resources import register_resources
