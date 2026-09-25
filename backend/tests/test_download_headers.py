"""Real download handlers must emit valid headers for Chinese contract names."""
import uuid
from urllib.parse import unquote

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize('format', ['md', 'docx', 'pdf'])
def test_chinese_filename_task_and_record_download(format):
    import main
    from storage.crud import create_user, create_record
    from tasks import create_task, update_task, TaskStatus
    from auth.utils import create_access_token

    user = create_user('export-' + uuid.uuid4().hex, 'not-used')
    filename = '退休人员返聘协议（模板）.docx'
    markdown = '# 审查报告\n\n中文合同文件名导出测试。'
    record_id = create_record(user.id, filename, markdown, {})
    task = create_task(filename, 100, user.id)
    update_task(task.task_id, status=TaskStatus.COMPLETED, result=markdown, record_id=record_id)
    headers = {'Authorization': 'Bearer ' + create_access_token({'user_id': user.id})}
    with TestClient(main.app) as client:
        for path in (f'/api/task/{task.task_id}/download', f'/api/download/{record_id}'):
            response = client.get(path, params={'format': format}, headers=headers)
            assert response.status_code == 200, response.text
            disposition = response.headers['content-disposition']
            assert disposition.isascii()
            assert '退休人员返聘协议（模板）' in unquote(disposition)
            assert response.content
