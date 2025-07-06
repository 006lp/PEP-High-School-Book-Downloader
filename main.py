import requests
import os
import time

# 基本配置

# 注意此处页数是包含封面扉页的，并不是书籍下标
# 以七年级上册数学为例，下载目录页到第一章末
# start_page= 6 
# stop_page= 31
start_page= 
stop_page= 

#你要下载的具体链接，Cookie等，请通过浏览器的开发者工具箱查看，例如
# base_url = "https://book.pep.com.cn/1321001101241/files/mobile/{}.jpg?240828095025"
# referer = "https://book.pep.com.cn/1321001101241/mobile/index.html"
# acw_sc__v3= "686a0adb9f209e20d77559ecb9d0b5a66355e4c3"
base_url = ""
referer = ""
acw_sc__v3= ""

def download_images():
    """
    批量下载图片的函数
    """
    
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': referer,
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cookie': f'acw_sc__v3={acw_sc__v3}'
    }
    
    # 创建保存图片的文件夹
    save_dir = "downloaded_images"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"创建文件夹: {save_dir}")
    
    # 下载统计
    success_count = 0
    failed_count = 0
    
    print("开始下载图片...")
    print("-" * 50)
    
    # 循环下载图片
    for d in range(start_page, stop_page+1):
        try:
            # 构造URL
            url = base_url.format(d)
            
            # 发送GET请求
            print(f"正在下载第 {d} 张图片...")
            response = requests.get(url, headers=headers, timeout=30)
            
            # 检查响应状态
            if response.status_code == 200:
                # 构造文件名
                filename = f"image_{d:02d}.jpg"
                filepath = os.path.join(save_dir, filename)
                
                # 保存图片
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"✓ 成功下载: {filename} ({len(response.content)} 字节)")
                success_count += 1
                
            else:
                print(f"✗ 下载失败: 第 {d} 张图片 (状态码: {response.status_code})")
                failed_count += 1
                
        except requests.exceptions.RequestException as e:
            print(f"✗ 网络错误: 第 {d} 张图片 - {str(e)}")
            failed_count += 1
        except Exception as e:
            print(f"✗ 未知错误: 第 {d} 张图片 - {str(e)}")
            failed_count += 1
        
        # 添加延时，避免请求过于频繁
        time.sleep(0.5)
    
    # 打印下载结果
    print("-" * 50)
    print(f"下载完成！")
    print(f"成功下载: {success_count} 张图片")
    print(f"下载失败: {failed_count} 张图片")
    print(f"图片保存在: {os.path.abspath(save_dir)} 文件夹中")

if __name__ == "__main__":
    download_images()