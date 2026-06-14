"""测试 output_guard 对退休人员返聘协议审查报告的检测 - 完整流程"""
import sys
import os
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from security.output_guard import OutputGuard, check_output_leak, SLIDING_WINDOW_SIZE, LEAK_CONFIRM_THRESHOLD

def main():
    # 1. 加载系统提示词并初始化 OutputGuard
    from layers.inference_layer import InferenceLayer
    temp_layer = InferenceLayer()
    system_prompt = temp_layer.prompt_template

    guard = OutputGuard(system_prompt)
    print(f"[INFO] 系统提示词长度: {len(system_prompt)} 字符")
    print(f"[INFO] 片段哈希数量: {len(guard._fragment_hashes)}")
    print(f"[INFO] 滑动窗口大小: {SLIDING_WINDOW_SIZE}")
    print(f"[INFO] 泄露阈值: {LEAK_CONFIRM_THRESHOLD}")

    # 2. 加载原始审查报告
    review_file = r"f:\ai\Sage\退休人员返聘协议（模板）.docx_review.txt"
    with open(review_file, 'r', encoding='utf-8') as f:
        raw_report = f.read()
    print(f"\n[INFO] 原始审查报告长度: {len(raw_report)} 字符")

    # 3. 调用 output_layer._filter_internal_content 过滤
    from layers.output_layer import OutputLayer
    output_layer = OutputLayer()
    filtered_report = output_layer._filter_internal_content(raw_report)

    # 4. 保存过滤后的内容
    filtered_file = r"f:\ai\Sage\test_filtered_output.txt"
    with open(filtered_file, 'w', encoding='utf-8') as f:
        f.write(filtered_report)
    print(f"[INFO] 过滤后内容已保存到: {filtered_file}")
    print(f"[INFO] 过滤后内容长度: {len(filtered_report)} 字符")

    # 5. 对过滤后的内容做泄露检测
    print(f"\n[TEST] 对过滤后内容进行泄露检测...")
    detect_content = guard._extract_detect_sections(filtered_report)
    print(f"[INFO] 提取检测章节长度: {len(detect_content)} 字符")

    passed, detail = guard.check_output(filtered_report)
    print(f"[RESULT] 通过: {passed}, 详情: {detail}")

    if not passed:
        # 详细分析
        content_len = len(detect_content)
        matched_positions = []
        whitelisted_matches = 0

        for i in range(content_len - SLIDING_WINDOW_SIZE + 1):
            fragment = detect_content[i:i + SLIDING_WINDOW_SIZE]
            if guard._is_whitelisted_fragment(fragment):
                whitelisted_matches += 1
                continue
            import hashlib
            fragment_hash = hashlib.sha256(fragment.encode('utf-8')).hexdigest()
            if fragment_hash in guard._fragment_hashes:
                matched_positions.append((i, fragment))

        print(f"\n[DEBUG] 白名单匹配数: {whitelisted_matches}")
        print(f"[DEBUG] 实际匹配位置数: {len(matched_positions)}")

        if matched_positions:
            print(f"\n[DEBUG] 前20个匹配片段:")
            for idx, (pos, frag) in enumerate(matched_positions[:20]):
                print(f"  [{idx}] 位置 {pos}: {repr(frag)}")

            total_consecutive = guard._calculate_consecutive_length([p[0] for p in matched_positions])
            print(f"\n[DEBUG] 连续匹配累计长度: {total_consecutive}")

            # 找出连续匹配的区域
            positions = sorted([p[0] for p in matched_positions])
            print(f"\n[DEBUG] 连续匹配区域详情:")
            if positions:
                current_start = positions[0]
                current_end = positions[0] + SLIDING_WINDOW_SIZE
                for i in range(1, len(positions)):
                    if positions[i] <= positions[i-1] + SLIDING_WINDOW_SIZE:
                        current_end = positions[i] + SLIDING_WINDOW_SIZE
                    else:
                        print(f"  区域: {current_start} - {current_end} (长度: {current_end - current_start})")
                        print(f"  内容: {repr(detect_content[current_start:current_end])}")
                        current_start = positions[i]
                        current_end = positions[i] + SLIDING_WINDOW_SIZE
                print(f"  区域: {current_start} - {current_end} (长度: {current_end - current_start})")
                print(f"  内容: {repr(detect_content[current_start:current_end])}")

    # 6. 额外测试：对原始未过滤内容做检测（对比）
    print(f"\n[COMPARE] 对原始未过滤内容进行泄露检测（对比）...")
    raw_passed, raw_detail = guard.check_output(raw_report)
    print(f"[RESULT] 原始内容 - 通过: {raw_passed}, 详情: {raw_detail}")

if __name__ == "__main__":
    main()
