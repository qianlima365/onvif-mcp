**ONVIF MCP** 是一个基于ONVIF协议实现的设备控制与管理平台（Media Control Platform），旨在为网络音视频设备（如IP摄像头、NVR等）提供标准化的控制接口。通过集成ONVIF核心规范，该项目支持以下功能：

- **设备发现**：自动扫描局域网内符合ONVIF标准的设备并获取基础信息（如型号、固件版本）
- **PTZ控制**：通过ONVIF PTZ服务实现云台旋转、镜头变焦等操作
- **媒体流管理**：获取设备实时视频流URL，支持RTSP/RTMP等协议
- **事件订阅**：接收并处理设备推送的运动检测、输入触发等事件
- **配置管理**：远程修改设备参数（分辨率、帧率、编码格式等）

项目采用Python实现ONVIF WS-Discovery与SOAP协议交互，提供CLI工具快速启动服务：
```shell
mcp dev main.py  # 启动设备探测与控制服务
或者
python run main.py --host 0.0.0.0 --port 8020
```