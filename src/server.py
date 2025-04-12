from mcp.server.fastmcp import FastMCP
import os
import json
from typing import Dict, Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 从环境变量或默认值获取工作目录
DEFAULT_WORKING_DIR = "~/accounting_data"
WORKING_DIR = os.getenv("ACCOUNTING_WORKING_DIR", DEFAULT_WORKING_DIR)

# 确保目录存在
os.makedirs(WORKING_DIR, exist_ok=True)

# 数据文件路径
DATA_FILE = os.path.join(WORKING_DIR, "accounting_data.json")

# 初始数据（如果文件不存在）
INITIAL_DATA = {
    "total_income": 0,
    "total_expense": 0,
    "balance": 0
}

def load_data() -> Dict:
    """从文件中加载数据，如果文件不存在则创建默认数据"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(INITIAL_DATA, f, indent=4)
            return INITIAL_DATA
    except Exception as e:
        logger.error(f"Failed to load data: {str(e)}")
        return INITIAL_DATA

def save_data(data: Dict) -> None:
    """将数据保存到文件"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to save data: {str(e)}")

# 创建 MCP 服务器
mcp = FastMCP("money-track-mcp", log_level="ERROR")

# 工具：记录收入和支出
@mcp.tool()
def record_transaction(income: Optional[int] = 0, expense: Optional[int] = 0) -> Dict:
    """记录今天的收入和支出，更新账户余额"""
    if not isinstance(income, (int, float)) or not isinstance(expense, (int, float)):
        return {"error": "Income and expense must be numbers"}

    data = load_data()
    data["total_income"] += income
    data["total_expense"] += expense
    data["balance"] = data["total_income"] - data["total_expense"]
    save_data(data)

    return {
        "message": "Transaction recorded successfully",
        "total_income": data["total_income"],
        "total_expense": data["total_expense"],
        "balance": data["balance"]
    }

# 资源：获取当前账户状态
@mcp.resource("accounting://status")
def get_account_status() -> Dict:
    """获取当前账户的收入、支出和余额"""
    data = load_data()
    return {
        "total_income": data["total_income"],
        "total_expense": data["total_expense"],
        "balance": data["balance"]
    }

# 提示：格式化账户报告
@mcp.prompt()
def format_account_report(status: Dict) -> str:
    """格式化账户状态为易读的报告"""
    return f"""
    === 账户报告 ===
    总收入: ${status["total_income"]:.2f}
    总支出: ${status["total_expense"]:.2f}
    当前余额: ${status["balance"]:.2f}
    ================
    """

def run_server():
    """运行 MCP 服务器"""
    print("=== Money Track MCP 服务启动 ===")
    logging.info("Money Track MCP 服务启动")
    print(f"当前工作目录: {os.getcwd()}")

    mcp.run(transport='stdio')
