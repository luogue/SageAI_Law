"""使用cat命令直接复制文件"""
import paramiko
import base64

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"
LOCAL_DIST = "f:/ai/Sage/frontend/dist"

def main():
    print("=" * 60)
    print("使用cat命令直接复制文件")
    print("=" * 60)
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=60)
    
    try:
        import os
        
        # 遍历上传
        for root, dirs, files in os.walk(LOCAL_DIST):
            for file in files:
                local_path = os.path.join(root, file)
                rel_path = os.path.relpath(local_path, LOCAL_DIST)
                remote_path = f"/app/frontend/{rel_path.replace(chr(92), '/')}"
                remote_dir = os.path.dirname(remote_path)
                
                # 确保目录存在
                ssh.exec_command(f"mkdir -p '{remote_dir}'")
                
                # 读取本地文件并用base64传输
                with open(local_path, 'rb') as f:
                    content = f.read()
                encoded = base64.b64encode(content).decode('utf-8')
                
                # 在服务器上解码并写入文件
                cmd = f"echo '{encoded}' | base64 -d > '{remote_path}'"
                stdin, stdout, stderr = ssh.exec_command(cmd)
                stdout.channel.recv_exit_status()
                
                print(f"  [OK] {rel_path}")
        
        # 验证
        print("\n[验证] 检查文件...")
        stdin, stdout, stderr = ssh.exec_command("docker exec sageai ls /app/frontend/static/*.js | wc -l")
        stdout.channel.recv_exit_status()
        count = stdout.read().decode('utf-8').strip()
        print(f"  JS文件数量: {count}")
        
        stdin, stdout, stderr = ssh.exec_command("docker exec sageai grep -c 'user_id' /app/frontend/static/*.js 2>/dev/null || echo '0'")
        stdout.channel.recv_exit_status()
        print(f"  包含user_id: {stdout.read().decode('utf-8').strip()}")
        
        print("\n" + "=" * 60)
        print("文件复制完成！")
        print("请强制刷新浏览器 (Ctrl+F5)")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()

if __name__ == "__main__":
    main()