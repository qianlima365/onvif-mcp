from mcp.server import FastMCP
from main import *

# # 初始化 FastMCP 服务器
mcp = FastMCP('onvif-mcp')

if __name__ == "__main__":
    mcp.run(transport='stdio')