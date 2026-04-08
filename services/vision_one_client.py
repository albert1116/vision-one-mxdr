import requests
from datetime import datetime, timedelta, timezone

REGION_URL_MAP = {
    'SG': 'https://api.sg.xdr.trendmicro.com',
    'US': 'https://api.xdr.trendmicro.com',
    'TW-G': 'https://api.tw-g.xdr.trendmicro.com',
    'XDR': 'https://api.xdr.trendmicro.com',
    'JP': 'https://api.xdr.trendmicro.co.jp',
    'AU': 'https://api.au.xdr.trendmicro.com',
    'EU': 'https://api.eu.xdr.trendmicro.com',
    'IN': 'https://api.in.xdr.trendmicro.com',
    'UK': 'https://api.uk.xdr.trendmicro.com',
    'MEA': 'https://api.mea.xdr.trendmicro.com',
}


class VisionOneClientError(Exception):
    pass


class VisionOneClient:
    def __init__(self, token: str, region: str, timeout: int = 60):
        if not token:
            raise VisionOneClientError('尚未輸入 Vision One API Token。')
        if not region:
            raise VisionOneClientError('尚未輸入 Vision One Region。')

        base_url = REGION_URL_MAP.get(region)
        if not base_url:
            raise VisionOneClientError(f'不支援的 Region：{region}')

        self.base_url = base_url
        self.region = region
        self.timeout = timeout
        self.headers = {'Authorization': f'Bearer {token}'}

    def _get(self, path: str, params=None, extra_headers=None):
        headers = dict(self.headers)
        if extra_headers:
            headers.update(extra_headers)

        response = requests.get(
            self.base_url + path,
            params=params or {},
            headers=headers,
            timeout=self.timeout,
        )

        if response.status_code >= 400:
            snippet = response.text[:500]
            raise VisionOneClientError(f'API 呼叫失敗（HTTP {response.status_code}）：{snippet}')

        try:
            return response.json()
        except Exception as e:
            raise VisionOneClientError(f'API 回傳不是合法 JSON：{e}')

    def _time_filter(self, time_range: str, field_name: str = 'createdDateTime'):
        now = datetime.now(timezone.utc)
        if time_range.endswith('h'):
            start_time = now - timedelta(hours=int(time_range[:-1]))
        elif time_range.endswith('d'):
            start_time = now - timedelta(days=int(time_range[:-1]))
        else:
            start_time = now - timedelta(hours=24)
        return f"{field_name} gt {start_time.strftime('%Y-%m-%dT%H:%M:%SZ')} and {field_name} le {now.strftime('%Y-%m-%dT%H:%M:%SZ')}"

    def query_endpoints(self, filter_string: str = ''):
        params = {'orderBy': 'agentGuid', 'top': 100}
        extra_headers = {'TMV1-Filter': filter_string} if filter_string else {}
        data = self._get('/v3.0/endpointSecurity/endpoints', params=params, extra_headers=extra_headers)
        items = data.get('items', [])
        records = []
        for item in items:
            raw_ips = item.get('ipAddresses', []) or []
            filtered_ips = [ip for ip in raw_ips if not ip.startswith('169.254') and ':' not in ip]
            records.append({
                'endpointName': item.get('endpointName', ''),
                'agentGuid': item.get('agentGuid', ''),
                'ipAddresses': ', '.join(filtered_ips),
                'osName': item.get('osName', ''),
                'osVersion': item.get('osVersion', ''),
                'lastLoggedOnUser': item.get('lastLoggedOnUser', ''),
                'lastUsedIp': item.get('lastUsedIp', ''),
                'isolationStatus': item.get('isolationStatus', ''),
            })
        return {'queryType': '端點查詢', 'totalCount': len(records), 'items': records, 'raw': data}

    def query_insights(self, time_range: str = '24h', filter_string: str = ''):
        params = {'orderBy': 'createdDateTime desc', 'top': 50}
        time_filter = self._time_filter(time_range, 'createdDateTime')
        final_filter = f'({filter_string}) and ({time_filter})' if filter_string else time_filter
        data = self._get('/v3.0/workbench/insights', params=params, extra_headers={'TMV1-Filter': final_filter})
        items = data.get('items', [])
        records = []
        for item in items:
            records.append({
                'id': item.get('id', ''),
                'score': item.get('score', ''),
                'name': item.get('name', ''),
                'createdDateTime': item.get('createdDateTime', ''),
                'updatedDateTime': item.get('updatedDateTime', ''),
                'indicatorCount': item.get('indicatorCount', 0),
                'matchedHighlightCount': item.get('matchedHighlightCount', 0),
            })
        return {'queryType': 'Insight 查詢', 'totalCount': len(records), 'items': records, 'raw': data, 'appliedFilter': final_filter}

    def query_workbench_alerts(self, time_range: str = '24h', filter_string: str = ''):
        params = {'top': 100}
        time_filter = self._time_filter(time_range, 'createdDateTime')
        final_filter = f'({filter_string}) and ({time_filter})' if filter_string else time_filter
        data = self._get('/v3.0/workbench/alerts', params=params, extra_headers={'TMV1-Filter': final_filter})
        items = data.get('items', [])
        records = []
        for item in items:
            records.append({
                'id': item.get('id', ''),
                'alertProvider': item.get('alertProvider', ''),
                'model': item.get('model', ''),
                'severity': item.get('severity', ''),
                'createdDateTime': item.get('createdDateTime', ''),
                'updatedDateTime': item.get('updatedDateTime', ''),
                'matchedIndicatorCount': item.get('matchedIndicatorCount', ''),
            })
        return {'queryType': 'Workbench 查詢', 'totalCount': len(records), 'items': records, 'raw': data, 'appliedFilter': final_filter}

    def query_events(self, time_range: str = '24h', filter_string: str = '', endpoint_name: str = ''):
        params = {
            'startDateTime': '',
            'endDateTime': '',
            'top': 100,
            'select': 'endpointHostName,parentFilePath,parentCmd,processFilePath,processCmd,objectFilePath,eventSubName,eventSubId,ruleName,src,dst,dpt,spt'
        }

        now = datetime.now(timezone.utc)
        if time_range.endswith('h'):
            start_time = now - timedelta(hours=int(time_range[:-1]))
        elif time_range.endswith('d'):
            start_time = now - timedelta(days=int(time_range[:-1]))
        else:
            start_time = now - timedelta(hours=24)

        params['startDateTime'] = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        params['endDateTime'] = now.strftime('%Y-%m-%dT%H:%M:%SZ')

        criteria_parts = []
        if endpoint_name:
            criteria_parts.append(f'endpointHostName:{endpoint_name}')
        if filter_string:
            criteria_parts.append(filter_string)
        criteria = ' AND '.join(criteria_parts) if criteria_parts else '*'

        data = self._get('/v3.0/search/endpointActivities', params=params, extra_headers={'TMV1-Query': criteria})
        items = data.get('items', [])
        records = []
        for item in items:
            records.append({
                'endpointHostName': item.get('endpointHostName', ''),
                'processFilePath': item.get('processFilePath', ''),
                'processCmd': item.get('processCmd', ''),
                'objectFilePath': item.get('objectFilePath', ''),
                'eventSubName': item.get('eventSubName', ''),
                'ruleName': item.get('ruleName', ''),
                'src': item.get('src', ''),
                'dst': item.get('dst', ''),
            })
        return {'queryType': '事件查詢', 'totalCount': len(records), 'items': records, 'raw': data, 'appliedFilter': criteria}

    def get_insight_detail(self, insight_id: str):
        if not insight_id:
            raise VisionOneClientError('缺少 Insight ID。')
        data = self._get(f'/v3.0/workbench/insights/{insight_id}')
        return {'detailType': 'Insight 詳細資料', 'raw': data}

    def get_alert_detail(self, alert_id: str):
        if not alert_id:
            raise VisionOneClientError('缺少 Alert ID。')
        data = self._get(f'/v3.0/workbench/alerts/{alert_id}')
        return {'detailType': 'Workbench 詳細資料', 'raw': data}
