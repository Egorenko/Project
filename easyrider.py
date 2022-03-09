import json
import re


def errors_check(info):
    errors = {
        'Type and required field validation': 0,
        'bus_id': 0,
        'stop_id': 0,
        'stop_name': 0,
        'next_stop': 0,
        'stop_type': 0,
        'a_time': 0
    }
    for bus in info:
        if type(bus['bus_id']) != int:
            errors['bus_id'] += 1
        if type(bus['stop_id']) != int:
            errors['stop_id'] += 1
        if not re.match('([A-Z][a-z]+) ?([A-Z][a-z]+)? (Road|Avenue|Boulevard|Street)$', bus['stop_name']):
            errors['stop_name'] += 1
        if type(bus['next_stop']) != int:
            errors['next_stop'] += 1
        if bus['stop_type'] != '' and not re.match('[SOF]?$', bus['stop_type']):
            errors['stop_type'] += 1
        if not re.match('([01][0-9]|[2][0123]):([0-5][0-9])$', bus['a_time']):
            errors['a_time'] += 1
    errors['Type and required field validation'] = sum(list(errors.values()))
    return errors


def line_check(info):
    lines = {}
    for bus in info:
        lines[bus['bus_id']] = lines.get(bus['bus_id'], 0) + 1
    return lines


def stop_chek(info):
    stops = {}
    starts = []
    ends = []
    stop = []
    transfer = []
    for bus in info:
        stops[bus['bus_id']] = stops.get(bus['bus_id'], []) + [bus['stop_type']]
        if bus['stop_type'] == 'S':
            starts.append(bus['stop_name'])
        elif bus['stop_type'] == 'F':
            ends.append(bus['stop_name'])
        if bus['stop_name'] in stop:
            transfer.append(bus['stop_name'])
        else:
            stop.append(bus['stop_name'])
    starts = set(starts)
    ends = set(ends)
    transfer = set(transfer)
    for bus in stops:
        if 'F' not in stops[bus] or 'S' not in stops[bus]:
            return f'There is no start or end stop for the line: {bus}'
    return {'start': starts, 'transfer': transfer, 'end': ends}


def time_check(info):
    times = {}
    for bus in info:
        if bus['bus_id'] not in times:
            times[bus['bus_id']] = []
        times[bus['bus_id']].append((bus['stop_name'], bus['a_time']))
    error = {}
    for bus in times:
        now_time = times[bus][0][1]
        for stop in times[bus]:
            if (int(stop[1][0:2]) < int(now_time[0:2])
                    or int(stop[1][0:2]) == int(now_time[0:2]) and int(stop[1][3:]) < int(now_time[3:])):
                error[bus] = stop[0]
                break
            else:
                now_time = stop[1]
    if not error:
        return 'OK'
    errors = []
    for bus in error:
        errors.append(f'bus_id line {bus}: wrong time on station {error[bus]}')
    return '\n'.join(errors)


def on_demand_check(info):
    stops = stop_chek(info)
    stop = stops['start']|stops['transfer']|stops['end']
    on_demand = []
    for bus in info:
        if bus['stop_type'] == 'O':
            on_demand.append(bus['stop_name'])
    on_demand = set(on_demand)
    if not stop & on_demand:
        return 'OK'
    return list(stop & on_demand)


information = json.loads(input())
num_errors = errors_check(information)
num_lines = line_check(information)
num_stops = stop_chek(information)
num_times = time_check(information)
num_on_demand = on_demand_check(information)
print('On demand stops test:')
print(f'Wrong stop type: {sorted(num_on_demand)}' if type(num_on_demand) == list else num_on_demand)
# print('Line names and number of stops:')
# for line in num_lines:
# print(f'bus_id: {line}, stops: {num_lines[line]}')
# for error in num_errors:
# if num_errors[error] != 0:
# print(f'{error}: {num_errors[error]}', 'errors' if error == 'Type and required field validation' else '')
