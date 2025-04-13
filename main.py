import time
import json
from onvif_device_manage import checkPwdAndGetCam, ptzChangeByClient, OnvifClient, ws_discovery

from mcp.server import FastMCP

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
    return json.dumps(client.get_rtsp())

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
    return json.dumps(client.get_deviceInfo())

@mcp.tool()
async def snap_image(host: str, port: int = 80, usr: str = 'admin', pwd: str = 'admin'):
    """
    Snap an image from the camera
    
    Args:
        host: Camera IP address
        port: Camera port
        usr: Camera username
        pwd: Camera password
    Returns:
        image base64 string
    """
    client = OnvifClient(host, port, usr, pwd, needSnapImg=False)
    bytearray = client.snap_image()
    # bytes转str
    return bytearray.decode('utf-8')

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
    return client.focus_move()

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

    return [{
        'host': '10.17.20.110',
        'port': 80,
        'usr': 'admin',
        'pwd': 'qwer1234'
    }]

if __name__ == "__main__":
    mcp.run(transport='stdio')
