import time
import json
from onvif_device_manage import checkPwdAndGetCam, ptzChangeByClient, OnvifClient, ws_discovery

import httpx
from mcp.server import FastMCP

# # 初始化 FastMCP 服务器
app = FastMCP('onvif-mcp')

@app.tool()
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
    

@app.tool()
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
    time.sleep(10)
    return {'status': 'movement_started'}

@app.tool()
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

@app.tool()
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

@app.tool()
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

@app.tool()
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




def main():
    print("Hello from onvif-mcp!")

    # 设备发现
    print(ws_discovery())

    # client = OnvifClient('10.17.20.88', 80, 'admin', 'admin123', needSnapImg=False)
    # client = OnvifClient('10.17.20.77', 80, 'admin', 'admin123', needSnapImg=False)
    # client = OnvifClient('10.17.20.66', 80, 'admin', 'admin123', needSnapImg=False)
    client = OnvifClient('10.17.20.110', 80, 'admin', 'qwer1234', needSnapImg=False)
    # 如果要控制特定摄像头，可以下边这样写
    # client = OnvifClient('192.168.1.10', 80, 'admin', '123456', token="ProfileToken002", sourceToken= "VideoSourceToken002", nodeToken="NodeToken002", needSnapImg=False)

    # 获取所有画面所有码流的RTSP地址、token(即ProfileToken)、sourceToken、nodeToken等信息

    # 获取设备信息
    print(json.dumps(client.get_deviceInfo()))

    # # 设置时间
    # client.set_cam_time()

    # 云台与聚焦控制
    # 云台上移
    ptzChangeByClient(client, 'Down', 1)
    # 移动一秒
    time.sleep(10)
    # 然后停止
    ptzChangeByClient(client, 'Up', 0)
    time.sleep(10)


if __name__ == "__main__":
    # main()
    app.run(transport='stdio')
