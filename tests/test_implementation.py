#!/usr/bin/env python3
"""
EU5 Modifier MCP Server 功能测试脚本
"""

import json
import logging
from pathlib import Path
from src.data_handler import DataHandler
from src.tools import register_tools
from src.resources import register_resources
from mcp.server.fastmcp import FastMCP

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_data_handler():
    """测试数据处理器"""
    print("\n" + "="*60)
    print("Test 1: DataHandler 功能测试")
    print("="*60)
    
    data_dir = Path(__file__).parent / "mcp-data"
    handler = DataHandler(data_dir)
    
    # 测试统计
    stats = handler.get_statistics()
    print(f"\nData Statistics:")
    print(f"  Total entries: {stats['total_entries']}")
    print(f"  Data types: {stats['data_types']}")
    print(f"  Effects: {stats['effects']}")
    print(f"  Triggers: {stats['triggers']}")
    print(f"  Modifiers: {stats['modifiers']}")
    print(f"  Event targets: {stats['event_targets']}")
    
    # 测试搜索功能
    print(f"\nSearch Tests:")
    
    # 按名称搜索
    results = handler.search_by_name('country', fuzzy=True, limit=3)
    print(f"  Search 'country': Found {len(results)} results")
    
    # 搜索修改器
    mod_results = handler.search_modifiers('tax', limit=3)
    print(f"  Search modifiers 'tax': Found {len(mod_results)} results")
    
    # 搜索效果
    eff_results = handler.search_effects('gain', limit=3)
    print(f"  Search effects 'gain': Found {len(eff_results)} results")
    
    # 搜索触发条件
    trig_results = handler.search_triggers('is_', limit=3)
    print(f"  Search triggers 'is_': Found {len(trig_results)} results")
    
    # 按类型获取
    type_results = handler.get_data_by_type('data_type', limit=3)
    print(f"  Get by type 'data_type': Found {len(type_results)} results")
    
    print("\n[PASS] DataHandler tests completed")


def test_mcp_server():
    """测试 MCP 服务器初始化"""
    print("\n" + "="*60)
    print("Test 2: MCP Server 初始化测试")
    print("="*60)
    
    try:
        # 创建服务器
        mcp = FastMCP("EU5ModifierMCP")
        print("\n[OK] FastMCP server created")
        
        # 初始化数据处理器
        data_dir = Path(__file__).parent / "mcp-data"
        data_handler = DataHandler(data_dir)
        print("[OK] DataHandler initialized")
        
        # 注册工具和资源
        register_tools(mcp, data_handler)
        print("[OK] Tools registered")
        
        register_resources(mcp, data_handler)
        print("[OK] Resources registered")
        
        print("\n[PASS] MCP Server fully initialized")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("EU5 Modifier MCP Server - 功能测试")
    print("="*60)
    
    try:
        test_data_handler()
        test_mcp_server()
        
        print("\n" + "="*60)
        print("所有测试完成!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
