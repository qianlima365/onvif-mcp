from mcp.server import FastMCP
from main import *

# # 初始化 FastMCP 服务器
mcp = FastMCP('onvif-mcp')

@mcp.tool()
async def onvif_tool(device_url, username, password, service_name):
    """
    执行 ONVIF 服务操作
    """
    return ""

if __name__ == "__main__":
    mcp.run(transport='stdio')