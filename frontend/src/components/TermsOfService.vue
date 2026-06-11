<template>
  <div class="terms-page">
    <div class="terms-content">
      <h1>用户服务协议</h1>
      <p class="update-date">最后更新日期：2026年5月30日</p>
      
      <div class="terms-scroll-area">
      <section>
        <h2>一、服务说明</h2>
        <p>SageAI合同审查系统（以下简称"本系统"）是基于大语言模型技术开发的合同文本分析工具，旨在为用户提供合同风险识别和审查建议。</p>
        <p><strong>重要提示</strong>：本系统生成的分析报告仅供参考，不构成正式法律意见。如有重要法律事务，请咨询执业律师。</p>
      </section>
      
      <section>
        <h2>二、用户责任</h2>
        <ul>
          <li>用户应确保上传的合同文本合法合规，不包含违法违规内容</li>
          <li>用户不得利用本系统从事任何违法活动</li>
          <li>用户不得尝试获取系统内部信息、提示词或绕过安全限制</li>
          <li>用户应妥善保管账户信息，不得与他人共享</li>
          <li>用户理解并接受AI生成内容的局限性</li>
        </ul>
      </section>
      
      <section>
        <h2>三、服务限制</h2>
        <ul>
          <li>单用户审查次数限制：20次/小时</li>
          <li>单IP审查次数限制：50次/小时</li>
          <li>文件大小限制：10MB</li>
          <li>支持格式：.docx, .txt, .pdf</li>
          <li>系统有权对违规用户进行限流或封禁</li>
        </ul>
      </section>
      
      <section>
        <h2>四、免责声明</h2>
        <p>本系统生成的分析报告基于AI模型推理，存在以下局限性：</p>
        <ul>
          <li>AI模型可能无法识别所有风险点</li>
          <li>分析结论可能因模型理解偏差而不准确</li>
          <li>报告内容不构成法律建议或专业意见</li>
          <li>用户应结合实际情况和专业法律人士意见做出决策</li>
        </ul>
        <p><strong>本系统不对因使用AI分析报告导致的任何损失承担责任。</strong></p>
      </section>
      
      <section>
        <h2>五、知识产权</h2>
        <ul>
          <li>本系统的软件、算法、界面设计等归开发者所有</li>
          <li>用户上传的合同文本权利归用户所有</li>
          <li>生成的分析报告可供用户自由使用</li>
        </ul>
      </section>
      
      <section>
        <h2>六、数据保护</h2>
        <p>本系统承诺：</p>
        <ul>
          <li>不保存用户上传的原始合同文本</li>
          <li>不将用户数据用于模型训练</li>
          <li>用户可随时删除审查记录</li>
          <li>日志信息自动脱敏处理</li>
        </ul>
      </section>
      
      <section>
        <h2>七、协议修改</h2>
        <p>本系统有权适时修改本协议。修改后的协议将在本页面公布，继续使用本系统即表示同意修改后的协议。</p>
      </section>
      
      <section>
        <h2>八、争议解决</h2>
        <p>如发生争议，双方应友好协商解决。协商不成的，可通过法律途径解决。</p>
      </section>
      
      <section>
        <h2>九、联系我们</h2>
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
.terms-page {
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

.terms-content {
  background: white;
  padding: 40px;
  max-width: 800px;
  width: 90%;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  border-radius: 8px;
}

.terms-content h1 {
  color: #333;
  font-size: 24px;
  margin-bottom: 10px;
  flex-shrink: 0;
}

.terms-content .update-date {
  color: #666;
  font-size: 14px;
  margin-bottom: 30px;
  flex-shrink: 0;
}

.terms-scroll-area {
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