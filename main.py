import time
import json
from src.onvif_device_manage import checkPwdAndGetCam, ptzChangeByClient, OnvifClient, ws_discovery

from mcp.server import FastMCP, Server
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
import uvicorn

# # 初始化 FastMCP 服务器
mcp = FastMCP('onvif-mcp')

@mcp.tool()
async def handle_discover_devices():
    """
    Discover ONVIF devices on the network

    Args:
        no args

    Returns:
        devices: List of discovered devices
    """
    try:
        devices = ws_discovery()
        return {
            'status': 'success',
            'devices': [str(d) for d in devices]  # Convert WS-Discovery objects to strings
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    

@mcp.tool()
async def handle_ptz_control(host: str, port: int = 80, usr: str = 'admin', pwd: str = 'admin', direction: str = 'Up', speed: float = 50):
    """
    Control camera PTZ movements

    Args:
        host: Camera IP address
        port: Camera port
        usr: Camera username
        pwd: Camera password
        direction: PTZ direction (e.g., 'Up', 'Right', 'Down', 'Left', 'LeftUp', 'RightUp', 'LeftDown', 'RightDown', 'ZoomWide', 'ZoomTele')
        speed: Movement speed (optional, default is 0.5)
    Returns:
        movement_started
    """
    client = OnvifClient(host, port, usr, pwd, needSnapImg=False)
    ptzChangeByClient(
        client=client,
        codeStr=direction,
        status=1,
        speed=speed
    )
    time.sleep(3)
    ptzChangeByClient(
        client=client,
        codeStr=direction,
        status=0,
        speed=speed
    )
    return {'status': 'movement_started'}

@mcp.tool()
async def get_rtsp(host: str, port: int = 80, usr: str = 'admin', pwd: str = 'admin'):
    """
    Get camera RTSP address
    
    Args:
        host: Camera IP address
        port: Camera port
        usr: Camera username
        pwd: Camera password
    Returns:
        rtsp_url
    """
    client = OnvifClient(host, port, usr, pwd, needSnapImg=False)
    return client.get_rtsp()

@mcp.tool()
async def get_deviceInfo(host: str, port: int = 80, usr: str = 'admin', pwd: str = 'admin'):
    """
    Get camera DeviceInfo
    
    Args:
        host: Camera IP address
        port: Camera port
        usr: Camera username
        pwd: Camera password
    Returns:
        deviceInfo
    """
    client = OnvifClient(host, port, usr, pwd, needSnapImg=False)
    return client.get_deviceInfo()

# @mcp.tool()
# async def snap_image(host: str, port: int = 80, usr: str = 'admin', pwd: str = 'admin'):
#     """
#     Snap an image from the camera
    
#     Args:
#         host: Camera IP address
#         port: Camera port
#         usr: Camera username
#         pwd: Camera password
#     Returns:
#         image base64 string
#     """
#     client = OnvifClient(host, port, usr, pwd, needSnapImg=True)
#     return client.snap_image()

@mcp.tool()
async def snap_image_to_minio(host: str, port: int = 80, usr: str = 'admin', pwd: str = 'admin'):
    """
    Snap an image from the camera, and upload to minio
    
    Args:
        host: Camera IP address
        port: Camera port
        usr: Camera username
        pwd: Camera password
    Returns:
        image url by minio
    """
    client = OnvifClient(host, port, usr, pwd, needSnapImg=True)
    image_base64 = client.snap_image()

    # 上传到minio
    # minio_key = upload_to_minio(image)
    from src.utils.minio import upload_to_minio
    # 将base64编码的字符串转换为二进制数据
    import base64
    image_bytes = base64.b64decode(image_base64)
    return upload_to_minio(image_bytes)


@mcp.tool()
async def focus_move(host: str, port: int = 80, usr: str = 'admin', pwd: str = 'admin', speed: float = 1):
    """
    focus_move from the camera
    
    Args:
        host: Camera IP address
        port: Camera port
        usr: Camera username
        pwd: Camera password
        speed: float 正数：聚焦+，拉近；负数：聚焦-，拉远；None：停止聚焦
    Returns:
        deviceInfo
    """
    client = OnvifClient(host, port, usr, pwd, needSnapImg=False)
    return client.focus_move(speed=speed)

# 获取摄像头列表
@mcp.tool()
async def get_camera_list():
    """
    Get camera list
    
    Args:
        no args
    Returns:
        camera list
    """

    return [
        {
                'name': '大厅门口摄像头',
                'host': '10.17.20.110',
                'port': 80,
                'usr': 'admin',
                'pwd': 'qwer1234',
                'http_flv': "https://ai.isstech.com/agent/live/test.live.flv",
                # "http_flv": "http://10.156.195.44:8080/live/test.live.flv",
                # "http_hls": "http://10.156.195.44:8080/live/test/hls.m3u8"
                "location": [116.281031, 40.049938]
                },{
                    'name': '办公区摄像头',
                    'host': '10.17.20.110',
                    'port': 80,
                    'usr': 'admin',
                    'pwd': 'qwer1234',
                    'http_flv': "https://ai.isstech.com/agent/live/test.live.flv",
                    # "http_flv": "http://10.156.195.44:8080/live/test.live.flv",
                    # "http_hls": "http://10.156.195.44:8080/live/test/hls.m3u8"
                    "location": [116.285481, 40.044352]
                },{
                    'name': '楼梯口摄像头',
                    'host': '10.17.20.110',
                    'port': 80,
                    'usr': 'admin',
                    'pwd': 'qwer1234',
                    'http_flv': "https://ai.isstech.com/agent/live/test.live.flv",
                    # "http_flv": "http://10.156.195.44:8080/live/test.live.flv",
                    # "http_hls": "http://10.156.195.44:8080/live/test/hls.m3u8"
                    "location": [116.464888, 39.946901]
                }
        ]
# 获取摄像头直播流播放地址
@mcp.tool()
async def get_camera_live(name: str):
    """
    Get camera live stream url
    
    Args:
        name: camera name
    Returns:
        camera live stream url
    """

    return  {
                'name': name,
                'host': '10.17.20.110',
                'port': 80,
                'usr': 'admin',
                'pwd': 'qwer1234',
                'http_flv': "https://ai.isstech.com/agent/live/test.live.flv",
                # "http_flv": "http://10.156.195.44:8080/live/test.live.flv",
                # "http_hls": "http://10.156.195.44:8080/live/test/hls.m3u8"
            }

def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application that can server the provied mcp server with SSE."""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,  # noqa: SLF001
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

# if __name__ == "__main__":
#     mcp.run(transport='stdio')

if __name__ == "__main__":
    mcp_server = mcp._mcp_server   

    import argparse
    
    parser = argparse.ArgumentParser(description='Run MCP SSE-based server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8020, help='Port to listen on')
    args = parser.parse_args()

    # Bind SSE request handling to MCP server
    starlette_app = create_starlette_app(mcp_server, debug=True)

    uvicorn.run(starlette_app, host=args.host, port=args.port)