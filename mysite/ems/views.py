from django.shortcuts import render
from django.template.loader import render_to_string
from .forms import DateRangeForm
from ems.models import *
import influxdb_client
from pytz import timezone
import json
import requests
from datetime import datetime, timedelta, timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Sum
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from decouple import config
import csv
import tempfile
# Create your views here.

# init influx
org = config('INFLUX_ORG')
token = config('INFLUX_TOKEN')
url = config('INFLUX_URL')

# init alarm

alarm_url = config('ALARM_URL')
alarm_token = config('ALARM_TOKEN')

client = influxdb_client.InfluxDBClient(
        url = url,
        token = token,
        org = org
    )

query_api = client.query_api()

# timezone
timezone_kst = timezone(timedelta(hours=9))


# main

def show_main(request):
    return render(request, 'ems/main.html')


# redis

def show_redis(request):
    return render(request, 'ems/redis.html')

def request_alarm(request):
    username = request.GET.get('username', '')
    phone = request.GET.get('phone', '')
    header = {
        "Authorization": alarm_token,
        "Content-Type": "application/json"
    }
    data = {
        "header": "[Django EMS] - ■■■누적전력량■■■",
        "site_id": 6,
        "site_name": "Django EMS",
        "device_name": str(username),
        "status": f"누적 전력량: 1556.21kWh",
        "occurred_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "call_number": str(phone),
    }

    json_data = json.dumps(data)
    requests.post(alarm_url, data=json_data, headers=header)
    return HttpResponse()


# mariaDB

def show_maria(request):
    form = DateRangeForm(request.POST or None)
    
    return render(request, 'ems/maria.html', {'form': form})

# ajax request mariadb
def ajax_update_table(request):
    page = request.GET.get('page', '1')
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')

    ems_list = Ems.objects.order_by('save_date')
    battery_list = Battery.objects.order_by('save_date')
    pv_list = Photovoltaics.objects.order_by('save_date')

    if start:
        ems_list = ems_list.filter(
            Q(save_date__gte=start)
        ).distinct()
        battery_list = battery_list.filter(
            Q(save_date__gte=start)
        ).distinct()
        pv_list = pv_list.filter(
            Q(save_date__gte=start)
        ).distinct()
        
    if end:
        end = datetime.strptime(end, '%Y-%m-%d')
        end = end.replace(hour=23, minute=59, second=59)
        ems_list = ems_list.filter(
            Q(save_date__lte=end)
        ).distinct()
        battery_list = battery_list.filter(
            Q(save_date__lte=end)
        ).distinct()
        pv_list = pv_list.filter(
            Q(save_date__lte=end)
        ).distinct()

    paginator_ems = Paginator(ems_list, 5)
    paginator_battery = Paginator(battery_list, 5)
    paginator_pv = Paginator(pv_list, 5)
    page_obj_ems = paginator_ems.get_page(page)
    page_obj_battery = paginator_battery.get_page(page)
    page_obj_pv = paginator_pv.get_page(page)
    
    context = {
        'ems_list': page_obj_ems,
        'battery_list': page_obj_battery, 
        'pv_list': page_obj_pv,
        'page': page,
        'start': start,
        'end': end,
    }

    html_data = render_to_string('ems/ems-table.html', context)

    return JsonResponse({'html_data': html_data})

def export_data_to_csv_min(request):
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')

    data = Ems.objects.order_by('save_date')
    if start:
        data = data.filter(
            Q(save_date__gte=start)
        ).distinct()
    if end:
        end = datetime.strptime(end, '%Y-%m-%d')
        end = end.replace(hour=23, minute=59, second=59)
        data = data.filter(
            Q(save_date__lte=end)
        ).distinct()
    temp_file = tempfile.NamedTemporaryFile(delete=False)

    with open(temp_file.name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        writer.writerow(['voltage_R', 'voltage_S','voltage_T', 'current_R', 'current_S', 'current_T', 'active_power', 'frequency', 'accumulate_energy', 'save_date'])
        
        for item in data:
            writer.writerow([item.voltage_R, item.voltage_S, item.voltage_T, item.current_R, item.current_S, item.current_T, item.active_power, item.frequency, item.accumulate_energy, item.save_date])
        
    response = HttpResponse(temp_file, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="data.csv"'
    
    return response


# influxDB

def show_influx(request):
    form = DateRangeForm(request.POST or None)
    return render(request, 'ems/influx.html', {'form': form})

# ajax request influx
def ajax_update_table_influx(request):
    page = int(request.GET.get('page', '1'))
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')

    if start == "":
        start = datetime(2000, 1, 1, 0, 0, 0).strftime('%Y-%m-%d')
    if end == "":
        end = datetime.now().strftime('%Y-%m-%d')
    
    query = f"""from(bucket: "mybucket")
    |> range(start: { start }T00:00:00Z, stop: { end }T23:59:59Z)
    |> filter(fn: (r) => r._measurement == "ems_data")
    |> limit(n: 15, offset: { ((page - 1) * 15) + 1 })
    """

    tables = query_api.query(query, org=org)

    query_c = f"""from(bucket: "mybucket")
    |> range(start: { start }T00:00:00Z, stop: { end }T23:59:59Z)
    |> filter(fn: (r) => r._measurement == "ems_data")
    |> filter(fn: (r) => r._field == "active_power")
    |> count()
    """
    
    try:
        count = query_api.query(query_c, org=org)
        total_obj = count.to_values(columns=['_value'])[0][0]
    except:
        total_obj = 0

    total_page = int(total_obj/15) + 1

    output = tables.to_json(columns=['_field', '_time', '_value'])
    output_json = json.loads(output)
    
    restructured_data = {}

    for item in output_json:
        time = item['_time']
        field = item['_field']
        value = item['_value']
        
        if time not in restructured_data:
            restructured_data[time] = {}
        restructured_data[time][field] = value
        
    result_list = []

    for time, values in restructured_data.items():
        influx_time = time
        formatted_time = datetime.strptime(influx_time, '%Y-%m-%dT%H:%M:%S.%f%z')
        datetime_kst = formatted_time.astimezone(timezone_kst)
        result_time = datetime_kst.strftime('%Y-%m-%d %H:%M:%S')
        new_item = {"time": result_time}
        new_item.update(values)
        result_list.append(new_item)

    start_index = (page - 1) * 15 + 1
    if total_obj == 0:
        start_index = 0
    end_index = start_index + 14
    if end_index > total_obj:
        end_index = total_obj
    

    context = {
        'start_index': start_index,
        'end_index': end_index,
        'page_range': range(1, total_page+1),
        'data': result_list,
        'total_obj': total_obj,
        'page': page,
        'total_page': total_page,
        'start': start,
        'end': end
        }

    html_data = render_to_string('ems/second-table.html', context)

    return JsonResponse({'html_data': html_data})

def export_data_to_csv_sec(request):
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')

    if start == "":
        start = datetime(2000, 1, 1, 0, 0, 0).strftime('%Y-%m-%d')
    if end == "":
        end = datetime.now().strftime('%Y-%m-%d')
    
    query = f"""from(bucket: "mybucket")
    |> range(start: { start }T00:00:00Z, stop: { end }T23:59:59Z)
    |> filter(fn: (r) => r._measurement == "ems_data")
    """

    tables = query_api.query(query, org=org)

    output = tables.to_json(columns=['_field', '_time', '_value'])
    output_json = json.loads(output)
    
    restructured_data = {}

    for item in output_json:
        time = item['_time']
        field = item['_field']
        value = item['_value']
        
        if time not in restructured_data:
            restructured_data[time] = {}
        restructured_data[time][field] = value
        
    result_list = []

    for time, values in restructured_data.items():
        influx_time = time
        formatted_time = datetime.strptime(influx_time, '%Y-%m-%dT%H:%M:%S.%f%z')
        datetime_kst = formatted_time.astimezone(timezone_kst)
        result_time = datetime_kst.strftime('%Y-%m-%d %H:%M:%S')
        new_item = {"time": result_time}
        new_item.update(values)
        result_list.append(new_item)
    
        
    temp_file = tempfile.NamedTemporaryFile(delete=False)

    with open(temp_file.name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        writer.writerow(['voltage_R', 'voltage_S','voltage_T', 'current_R', 'current_S', 'current_T', 'active_power', 'frequency', 'accumulate_energy', 'save_date'])
        
        for item in result_list:
            try:
                writer.writerow([item['voltage_R'], item['voltage_S'], item['voltage_T'],  item['current_R'], item['current_S'], \
                                 item['current_T'], item['active_power'], item['frequency'], item['accumulate_energy'], item['time']])
            except KeyError as e:
                print("error key")
        
    response = HttpResponse(temp_file, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="data.csv"'
    
    return response



# chart.js

def show_statistics(request):
    
    return render(request, 'ems/statistics.html')

def ajax_update_table_chart(request):
    page = request.GET.get('page', '1')
    date = request.GET.get('date', '')

    data = Ems.objects.order_by('save_date')

    if date:
        data = data.filter(
            Q(save_date__icontains=date)
        ).distinct()

    table_data = []

    if data:
        current_time = min(data, key=lambda x: x.save_date).save_date.replace(second=0, microsecond=0)
        end_time = max(data, key=lambda x: x.save_date).save_date.replace(second=0, microsecond=0)
        while current_time <= end_time:
            data_for_interval = data.filter(save_date__gte=current_time, save_date__lt=current_time + timedelta(minutes=15))
            total_value = data_for_interval.aggregate(Sum('active_power'))['active_power__sum'] or 0
            table_data.append({
                'time': current_time.strftime('%Y-%m-%d %H:%M'),
                'total_value': round(total_value/60, 2)
            })
            current_time += timedelta(minutes=15)

    paginator_data = Paginator(table_data, 5)
    page_obj_data = paginator_data.get_page(page)

    context = {
        'data': page_obj_data,
        'page': page,
        'date': date
        }

    html_data = render_to_string('ems/chart-table.html', context)

    return JsonResponse({'html_data': html_data})

def chart_data(request):
    date = request.GET.get('date', '')
    data = Ems.objects.all()

    if date:
        data = data.filter(
            Q(save_date__icontains=date)
        ).distinct()

    chart_data = {
        'labels': [],
        'data': []
    }

    current_time = min(data, key=lambda x: x.save_date).save_date.replace(second=0, microsecond=0)
    end_time = max(data, key=lambda x: x.save_date).save_date.replace(second=0, microsecond=0)

    while current_time <= end_time:
        data_for_interval = data.filter(save_date__gte=current_time, save_date__lt=current_time + timedelta(minutes=15))
        total_value = data_for_interval.aggregate(Sum('active_power'))['active_power__sum'] or 0
        chart_data['labels'].append(current_time.strftime('%Y-%m-%d %H:%M'))
        chart_data['data'].append(round(total_value/60, 2))
        current_time += timedelta(minutes=15)

    return JsonResponse(chart_data)