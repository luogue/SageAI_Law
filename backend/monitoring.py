"""监控模块 - 提供健康检查和性能指标"""
import time
import psutil
from typing import Dict, Any
from datetime import datetime
from collections import defaultdict

# 全局统计数据
metrics = {
    'requests': {
        'total': 0,
        'success': 0,
        'failed': 0,
        'status_codes': defaultdict(int),
        'latency': {
            'total': 0.0,
            'count': 0,
            'min': float('inf'),
            'max': 0.0
        },
        'endpoints': defaultdict(lambda: {
            'total': 0,
            'success': 0,
            'failed': 0,
            'latency': {
                'total': 0.0,
                'count': 0
            }
        })
    },
    'tasks': {
        'total': 0,
        'completed': 0,
        'failed': 0,
        'pending': 0,
        'processing': 0
    },
    'errors': {
        'total': 0,
        'types': defaultdict(int)
    }
}

# 服务启动时间
START_TIME = time.time()

def record_request(endpoint: str, method: str, status_code: int, latency: float):
    """记录请求统计"""
    metrics['requests']['total'] += 1
    metrics['requests']['status_codes'][status_code] += 1
    metrics['requests']['latency']['total'] += latency
    metrics['requests']['latency']['count'] += 1
    metrics['requests']['latency']['min'] = min(metrics['requests']['latency']['min'], latency)
    metrics['requests']['latency']['max'] = max(metrics['requests']['latency']['max'], latency)
    
    if status_code >= 200 and status_code < 400:
        metrics['requests']['success'] += 1
    else:
        metrics['requests']['failed'] += 1
    
    # 记录端点统计
    endpoint_key = f"{method} {endpoint}"
    metrics['requests']['endpoints'][endpoint_key]['total'] += 1
    metrics['requests']['endpoints'][endpoint_key]['latency']['total'] += latency
    metrics['requests']['endpoints'][endpoint_key]['latency']['count'] += 1
    if status_code >= 200 and status_code < 400:
        metrics['requests']['endpoints'][endpoint_key]['success'] += 1
    else:
        metrics['requests']['endpoints'][endpoint_key]['failed'] += 1

def record_task_status(status: str):
    """记录任务状态"""
    metrics['tasks']['total'] += 1
    if status == 'completed':
        metrics['tasks']['completed'] += 1
    elif status == 'failed':
        metrics['tasks']['failed'] += 1
    elif status == 'pending':
        metrics['tasks']['pending'] += 1
    elif status == 'processing':
        metrics['tasks']['processing'] += 1

def record_error(error_type: str):
    """记录错误"""
    metrics['errors']['total'] += 1
    metrics['errors']['types'][error_type] += 1

def get_health_status() -> Dict[str, Any]:
    """获取健康状态"""
    uptime = int(time.time() - START_TIME)
    
    # 获取CPU和内存使用情况
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    
    # 计算平均延迟
    latency_data = metrics['requests']['latency']
    avg_latency = latency_data['total'] / latency_data['count'] if latency_data['count'] > 0 else 0.0
    
    # 计算成功率
    success_rate = (metrics['requests']['success'] / metrics['requests']['total'] * 100 
                   if metrics['requests']['total'] > 0 else 100.0)
    
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime': {
            'seconds': uptime,
            'formatted': format_uptime(uptime)
        },
        'system': {
            'cpu_percent': cpu_percent,
            'memory': {
                'total': memory.total // (1024 ** 2),
                'used': memory.used // (1024 ** 2),
                'available': memory.available // (1024 ** 2),
                'percent': memory.percent
            }
        },
        'requests': {
            'total': metrics['requests']['total'],
            'success': metrics['requests']['success'],
            'failed': metrics['requests']['failed'],
            'success_rate': round(success_rate, 2),
            'latency': {
                'avg_ms': round(avg_latency * 1000, 2),
                'min_ms': round(metrics['requests']['latency']['min'] * 1000, 2) if latency_data['count'] else 0,
                'max_ms': round(metrics['requests']['latency']['max'] * 1000, 2)
            },
            'status_codes': dict(metrics['requests']['status_codes'])
        },
        'tasks': {
            'total': metrics['tasks']['total'],
            'completed': metrics['tasks']['completed'],
            'failed': metrics['tasks']['failed'],
            'pending': metrics['tasks']['pending'],
            'processing': metrics['tasks']['processing']
        },
        'errors': {
            'total': metrics['errors']['total'],
            'types': dict(metrics['errors']['types'])
        }
    }

def get_metrics_summary() -> Dict[str, Any]:
    """获取指标摘要"""
    latency_data = metrics['requests']['latency']
    avg_latency = latency_data['total'] / latency_data['count'] if latency_data['count'] > 0 else 0.0
    success_rate = (metrics['requests']['success'] / metrics['requests']['total'] * 100 
                   if metrics['requests']['total'] > 0 else 100.0)
    
    return {
        'timestamp': datetime.now().isoformat(),
        'requests_total': metrics['requests']['total'],
        'requests_success': metrics['requests']['success'],
        'requests_failed': metrics['requests']['failed'],
        'success_rate': round(success_rate, 2),
        'avg_latency_ms': round(avg_latency * 1000, 2),
        'tasks_completed': metrics['tasks']['completed'],
        'tasks_failed': metrics['tasks']['failed'],
        'errors_total': metrics['errors']['total']
    }

def get_endpoint_metrics() -> Dict[str, Any]:
    """获取端点级别的指标"""
    result = {}
    for endpoint_key, data in metrics['requests']['endpoints'].items():
        avg_latency = data['latency']['total'] / data['latency']['count'] if data['latency']['count'] > 0 else 0.0
        success_rate = (data['success'] / data['total'] * 100 if data['total'] > 0 else 100.0)
        result[endpoint_key] = {
            'total': data['total'],
            'success': data['success'],
            'failed': data['failed'],
            'success_rate': round(success_rate, 2),
            'avg_latency_ms': round(avg_latency * 1000, 2)
        }
    return result

def format_uptime(seconds: int) -> str:
    """格式化运行时间"""
    days = seconds // (24 * 3600)
    hours = (seconds % (24 * 3600)) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if days > 0:
        return f"{days}天 {hours}小时 {minutes}分钟"
    elif hours > 0:
        return f"{hours}小时 {minutes}分钟"
    elif minutes > 0:
        return f"{minutes}分钟 {secs}秒"
    else:
        return f"{secs}秒"

def reset_metrics():
    """重置所有指标"""
    global metrics
    metrics = {
        'requests': {
            'total': 0,
            'success': 0,
            'failed': 0,
            'status_codes': defaultdict(int),
            'latency': {
                'total': 0.0,
                'count': 0,
                'min': float('inf'),
                'max': 0.0
            },
            'endpoints': defaultdict(lambda: {
                'total': 0,
                'success': 0,
                'failed': 0,
                'latency': {
                    'total': 0.0,
                    'count': 0
                }
            })
        },
        'tasks': {
            'total': 0,
            'completed': 0,
            'failed': 0,
            'pending': 0,
            'processing': 0
        },
        'errors': {
            'total': 0,
            'types': defaultdict(int)
        }
    }
