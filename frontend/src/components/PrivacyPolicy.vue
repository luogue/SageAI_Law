<template>
  <div class="policy-page">
    <div class="policy-content">
      <h1>隐私政策</h1>
      <p class="update-date">最后更新日期：2026年5月31日</p>
      
      <div class="policy-scroll-area">
      <section>
        <h2>一、我们收集的信息</h2>
        <p>SageAI合同审查系统（以下简称"本系统"）在提供服务过程中会收集以下信息：</p>
        <ul>
          <li><strong>手机号码</strong>：用于用户注册和登录身份验证</li>
          <li><strong>合同文本</strong>：仅用于合同审查分析，处理完成后立即丢弃，不保存到服务器（除非您主动选择上传用于模型训练）</li>
          <li><strong>用户反馈</strong>：包括评价、建议、问题分类等，用于改进服务质量</li>
          <li><strong>操作记录</strong>：包括审查记录、文件名、操作时间等（不含合同原文）</li>
          <li><strong>日志信息</strong>：请求ID、用户标识（脱敏）、IP地址（脱敏）、操作路径、耗时等</li>
        </ul>
      </section>
      
      <section>
        <h2>二、信息使用目的</h2>
        <p>我们收集的信息仅用于以下目的：</p>
        <ul>
          <li>提供合同审查服务</li>
          <li>维护用户账户安全</li>
          <li>改进服务质量</li>
          <li>遵守法律法规要求</li>
        </ul>
        <p><strong>重要声明</strong>：您的合同文本通常仅用于临时审查分析，不会被保存、存储或用于模型训练。审查完成后，合同原文立即从内存中清除。</p>
        <div class="highlight-box">
          <p><strong>用户反馈激励计划</strong>：当您主动提交反馈并勾选上传合同文本时，您提供的合同内容将仅用于模型训练和错误分析，不会与您的身份信息关联，也不会用于其他目的。您可以随时要求我们删除您提交的数据。</p>
        </div>
      </section>
      
      <section>
        <h2>三、信息存储与保护</h2>
        <ul>
          <li>用户密码采用bcrypt哈希存储，无法还原为原始密码</li>
          <li>审查报告存储于数据库，用户可随时删除</li>
          <li>日志信息自动脱敏处理，不记录合同原文</li>
          <li>系统采用限流、黑名单等安全机制防止滥用</li>
        </ul>
      </section>
      
      <section>
        <h2>四、用户权利</h2>
        <p>您对个人信息享有以下权利：</p>
        <ul>
          <li><strong>查看权</strong>：可查看自己的审查记录</li>
          <li><strong>删除权</strong>：可删除单条或全部审查记录</li>
          <li><strong>注销权</strong>：可申请注销账户（需联系管理员）</li>
        </ul>
      </section>
      
      <section>
        <h2>五、数据安全提示</h2>
        <div class="highlight-box">
          <p>为保护您的数据隐私，上传的合同文本仅在审查过程中临时使用，不会保存到服务器。刷新页面后，您需要重新上传。</p>
        </div>
      </section>
      
      <section>
        <h2>六、未成年人保护</h2>
        <p>本系统仅面向年满18周岁的用户提供服务。如果您是未成年人，请在监护人指导下使用。</p>
      </section>
      
      <section>
        <h2>七、政策更新</h2>
        <p>我们可能会适时修订本隐私政策。修订后的政策将在本页面公布，请定期查阅。</p>
      </section>
      
      <section>
        <h2>八、联系我们</h2>
        <p>如有任何疑问或建议，请联系系统管理员。</p>
      </section>
      </div>
      
      <button class="confirm-btn" @click="$emit('close')">确认</button>
    </div>
  </div>
</template>

<script setup>
defineEmits(['close'])
</script>

<style scoped>
.policy-page {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.policy-content {
  background: white;
  padding: 40px;
  max-width: 800px;
  width: 90%;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  border-radius: 8px;
}

.policy-content h1 {
  color: #333;
  font-size: 24px;
  margin-bottom: 10px;
  flex-shrink: 0;
}

.policy-content .update-date {
  color: #666;
  font-size: 14px;
  margin-bottom: 30px;
  flex-shrink: 0;
}

.policy-scroll-area {
  flex: 1;
  overflow-y: auto;
  padding-right: 10px;
}

section {
  margin-bottom: 25px;
}

h2 {
  color: #4080FF;
  font-size: 18px;
  margin-bottom: 15px;
}

p {
  color: #333;
  line-height: 1.6;
  margin-bottom: 10px;
}

ul {
  color: #333;
  line-height: 1.8;
  padding-left: 20px;
}

li {
  margin-bottom: 8px;
}

.highlight-box {
  background: #fff3cd;
  border: 1px solid #ffc107;
  padding: 15px;
  border-radius: 4px;
  margin: 15px 0;
}

.highlight-box p {
  color: #856404;
  margin: 0;
}

.confirm-btn {
  background: #4080FF;
  color: white;
  border: none;
  padding: 12px 40px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  flex-shrink: 0;
}

.confirm-btn:hover {
  background: #3060dd;
}
</style>