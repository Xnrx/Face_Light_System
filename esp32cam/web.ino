#include <esp32cam.h>   // 引用 ESP32-CAM 库
#include <WebServer.h>  // 引用 WebServer 库
#include <WiFi.h>       // 引用 WiFi 库

const char* WIFI_SSID = "12345678";  // WiFi SSID，改成自己的 Wi-Fi 名称
const char* WIFI_PASS = "qwe12345";  // WiFi 密码，改成自己的 Wi-Fi 密码

WebServer server(80);  // 创建 Web 服务器实例，端口为 80

// 预定义两个分辨率
static auto loRes = esp32cam::Resolution::find(320, 240);
static auto hiRes = esp32cam::Resolution::find(640, 480);

// 处理 BMP 图片请求
void handleBmp()
{
  // 将相机分辨率设置为低分辨率
  if (!esp32cam::Camera.changeResolution(loRes)) {
    Serial.println("SET-LO-RES FAIL");  // 更改分辨率失败
  }

  // 捕获一帧图像
  auto frame = esp32cam::capture();
  if (frame == nullptr) {
    Serial.println("CAPTURE FAIL");  // 捕获图像失败
    server.send(503, "", "");  // 发送 HTTP 状态码 503
    return;
  }
  Serial.printf("CAPTURE OK %dx%d %db\n", frame->getWidth(), frame->getHeight(),
                static_cast<int>(frame->size()));  // 打印捕获的图像信息

  // 将图像转换为 BMP 格式
  if (!frame->toBmp()) {
    Serial.println("CONVERT FAIL");  // 转换格式失败
    server.send(503, "", "");  // 发送 HTTP 状态码 503
    return;
  }
  Serial.printf("CONVERT OK %dx%d %db\n", frame->getWidth(), frame->getHeight(),
                static_cast<int>(frame->size()));  // 打印转换后的图像信息

  // 设置 HTTP 响应头
  server.setContentLength(frame->size());
  server.send(200, "image/bmp");  // 发送 HTTP 状态码 200 和 MIME 类型
  WiFiClient client = server.client();
  frame->writeTo(client);  // 将图像数据写入客户端
}

// 发送 JPEG 图片
void serveJpg()
{
  auto frame = esp32cam::capture(); // 捕获一张图像
  if (frame == nullptr) { // 如果图像捕获失败
    Serial.println("CAPTURE FAIL"); // 在串口打印错误信息
    server.send(503, "", ""); // 向客户端发送503错误响应
    return;
  }
  Serial.printf("CAPTURE OK %dx%d %db\n", frame->getWidth(), frame->getHeight(),
                static_cast<int>(frame->size())); // 在串口打印图像信息

  server.setContentLength(frame->size()); // 设置HTTP响应正文的长度
  server.send(200, "image/jpeg"); // 向客户端发送HTTP响应头和状态码
  WiFiClient client = server.client(); // 获取客户端连接的WiFiClient对象

  // 将图像数据通过客户端连接发送给浏览器
  frame->writeTo(client);
}

// 处理 JPEG 图片请求（高分辨率）
void handleJpgHi()
{
  // 将相机分辨率设置为高分辨率
  if (!esp32cam::Camera.changeResolution(hiRes)) {
    Serial.println("SET-HI-RES FAIL");  // 更改分辨率失败
  }

  // 发送 JPEG 图片
  serveJpg();
}

// 处理 JPEG 图片请求（低分辨率）
void handleJpgLo()
{
  // 将相机分辨率设置为低分辨率
  if (!esp32cam::Camera.changeResolution(loRes)) {
    Serial.println("SET-LO-RES FAIL");  // 更改分辨率失败
  }

  // 发送 JPEG 图片
  serveJpg();
}

void handleJpg()
{
  server.sendHeader("Location", "/cam-hi.jpg"); // 将HTTP响应头Location设置为/cam-hi.jpg
  server.send(302, "", ""); // 发送HTTP响应状态码302表示重定向，不带响应内容
}

void handleMjpeg()
{
  if (!esp32cam::Camera.changeResolution(hiRes)) { // 设置相机分辨率为高分辨率
    Serial.println("SET-HI-RES FAIL");
  }

  Serial.println("STREAM BEGIN"); // 在串口监视器上输出"STREAM BEGIN"
  WiFiClient client = server.client(); // 为当前连接的客户端创建一个WiFiClient对象
  auto startTime = millis(); // 记录开始时间
  int res = esp32cam::Camera.streamMjpeg(client); // 调用esp32cam库中的streamMjpeg函数，将MJPEG格式的视频流发送到客户端

  if (res <= 0) { // 如果streamMjpeg函数返回值小于等于0，说明发送失败
    Serial.printf("STREAM ERROR %d\n", res); // 在串口监视器上输出"STREAM ERROR"和错误码
    return;
  }
  auto duration = millis() - startTime; // 记录发送时间
  Serial.printf("STREAM END %dfrm %0.2ffps\n", res, 1000.0 * res / duration); // 在串口监视器上输出"STREAM END"、帧数和帧率
}

void setup()
{
  Serial.begin(115200); // 初始化串口通信
  Serial.println();

  {
    using namespace esp32cam;
    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(hiRes);
    cfg.setBufferCount(2);
    cfg.setJpeg(80);


    bool ok = Camera.begin(cfg); // 初始化esp32cam库中的Camera对象
    Serial.println(ok ? "CAMERA OK" : "CAMERA FAIL"); // 在串口监视器上输出摄像头是否初始化成功
  }

  WiFi.persistent(false); // 关闭WiFi的持久化功能
  WiFi.mode(WIFI_AP); // 设置WiFi模式为STA模式（客户端模式）
  WiFi.begin(WIFI_SSID, WIFI_PASS); // 连接WiFi网络
  while (WiFi.status() != WL_CONNECTED) { // 等待WiFi连接成功
    delay(500);
  }

  Serial.print("http://");
  Serial.println(WiFi.localIP());
  Serial.println("  /cam-hi.jpg");

  server.on("/cam-hi.jpg", handleJpgHi);

  server.begin();
}


void loop()
{
  server.handleClient();
}