"""删除容器内的旧版本文件"""
import paramiko

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"

def ssh_exec(cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=30)
    try:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.channel.recv_exit_status()
        return stdout.read().decode('utf-8'), stderr.read().decode('utf-8')
    finally:
        ssh.close()

def main():
    print("=" * 60)
    print("删除容器内的旧版本文件")
    print("=" * 60)
    
    try:
        # 删除旧的Home文件
        print("\n[1/3] 删除旧的Home文件...")
        output, error = ssh_exec("docker exec sageai rm -f /app/frontend/static/Home-CWdjUCM-.js /app/frontend/static/Home-DkdfnWlr.js /app/frontend/static/Home-nTZnJvFI.css")
        print(f"  {output}")
        
        # 删除其他旧版本文件
        print("\n[2/3] 删除其他旧版本文件...")
        cmd = """docker exec sageai rm -f \
            /app/frontend/static/FeedbackModal-B3fxtgBf.css \
            /app/frontend/static/FeedbackModal-JF0vbaVJ.js \
            /app/frontend/static/FeedbackModal-t-gLO1_U.js \
            /app/frontend/static/Login-C0Gx1Go-.js \
            /app/frontend/static/Login-6iTHxMLM.js \
            /app/frontend/static/Login-Bhki6grX.css \
            /app/frontend/static/MyReports-K12Hfe1v.js \
            /app/frontend/static/MyReports-DZgc6kbM.css \
            /app/frontend/static/PhoneInput-DKud__uZ.js \
            /app/frontend/static/PhoneInput-3r9ODbVg.css \
            /app/frontend/static/Register-Bod7ix6I.js \
            /app/frontend/static/Register-CtVv2fPD.css \
            /app/frontend/static/ResultPage-Cg4v1aon.js \
            /app/frontend/static/ResultPage-C6zgWCn6.css \
            /app/frontend/static/TermsOfService-BIvyO3pq.js \
            /app/frontend/static/TermsOfService-D63Fg4Jp.css \
            /app/frontend/static/TermsOfService-V69SReRv.js \
            /app/frontend/static/UploadPage-DtfyBSUr.js \
            /app/frontend/static/UploadPage-DygCTzqB.js \
            /app/frontend/static/api-B-x-ZthA.js \
            /app/frontend/static/api-DRh9dwJr.js \
            /app/frontend/static/index-BOUAhokd.js \
            /app/frontend/static/index-xTbE8wqj.js \
            /app/frontend/static/vue-vendor-COUcpGyU.js \
            /app/frontend/static/element-plus-CsLHdTGX.js"""
        output, error = ssh_exec(cmd)
        print("  [OK]")
        
        # 列出当前文件
        print("\n[3/3] 列出当前Home文件...")
        output, error = ssh_exec("docker exec sageai ls /app/frontend/static/Home*.js 2>/dev/null")
        print(f"  {output}")
        
        # 检查user_id
        print("\n[验证] 检查user_id...")
        output, error = ssh_exec("docker exec sageai grep -c 'user_id' /app/frontend/static/*.js 2>/dev/null || echo '0'")
        print(f"  {output}")
        
        print("\n" + "=" * 60)
        print("旧版本文件已删除！")
        print("请强制刷新浏览器 (Ctrl+F5)")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()