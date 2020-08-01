from datetime import datetime,timedelta


def flapping_alarms(list_full):

    # creating DICTIONARY where KEYS are service id and VALUES are tuples {idX : (start, duration),(start, duration),..}
    dict_unique_alarms = {}
    for alarm_instance in list_full:

        next_key = alarm_instance['service_id']
        if next_key in dict_unique_alarms:
            dict_unique_alarms[next_key].append((alarm_instance['startTime'], alarm_instance['duration']))

        else:
            dict_unique_alarms[next_key] = []
            dict_unique_alarms[next_key].append((alarm_instance['startTime'], alarm_instance['duration']))

    # sorting lists for each alarm_id
    list_flappings = []
    for alarm_id, alarm_list_of_tuples in dict_unique_alarms.items():
        alarm_list_of_tuples.sort(key=lambda x: x[0])
        print( alarm_list_of_tuples)
        print('#############')

        # check flapping for each tupple (start, duration)
        for ind, alarm_instance in enumerate(alarm_list_of_tuples):
            print(alarm_instance[0])
            print('------------')
            time_prev_start = 0
            accum_time = 0
            duration = 0
            flapping_ocurrences = 1

            ind_back = ind - 1
            date_time_current_start = datetime.strptime(alarm_instance[0], '%Y-%m-%d %H:%M:%S')
            date_time_current_end = date_time_current_start + timedelta(minutes=alarm_instance[1])
            if ind_back:
                date_time_prev_start = datetime.strptime(alarm_list_of_tuples[ind_back][0], '%Y-%m-%d %H:%M:%S')
                date_time_prev_end = date_time_prev_start + timedelta(minutes=alarm_list_of_tuples[ind_back][1])

            else:
                date_time_prev_start = date_time_current_start
                date_time_prev_end = date_time_current_end




            # case1- 2 hours before start of current / maximum occurrences

            while (ind_back >= 0) and (date_time_prev_end > date_time_current_start-timedelta(minutes=120)):
                date_time_prev_start = datetime.strptime(alarm_list_of_tuples[ind_back][0], '%Y-%m-%d %H:%M:%S')
                date_time_prev_end = date_time_prev_start + timedelta(minutes=alarm_list_of_tuples[ind_back][1])
                if date_time_current_start > date_time_prev_start + timedelta(minutes=120):

                    time_prev_start = alarm_list_of_tuples[ind_back][0]
                    duration += alarm_list_of_tuples[ind_back][1]
                    if date_time_prev_end > date_time_current_start - timedelta(minutes=120):
                        accum_time += (date_time_prev_end - (date_time_current_start-timedelta(minutes=120))).seconds/60

                        flapping_ocurrences +=1
                        #print('t')
                        delta = (date_time_prev_end - (date_time_current_start-timedelta(minutes=120)))
                        #print(delta.seconds/60)
                    break

                else:
                    accum_time += alarm_list_of_tuples[ind_back][1]
                    duration += alarm_list_of_tuples[ind_back][1]
                    date_time_prev_start = datetime.strptime(alarm_list_of_tuples[ind_back][0], '%Y-%m-%d %H:%M:%S')
                    time_prev_start = alarm_list_of_tuples[ind_back][0]
                    flapping_ocurrences += 1
                ind_back -= 1
                #print('is')

            #print(accum_time,flapping_ocurrences )

            if accum_time>15:
                list_flappings.append({'service_id':alarm_id,'start':time_prev_start,'duration':duration,'end': str(date_time_current_end),'amount_outages':flapping_ocurrences,'sum_outages':accum_time})
                break
            else:
                # case2- 2 hours before end of current /maximum time
                ind_back = ind
                date_time_prev_start = date_time_current_start
                date_time_prev_end = date_time_current_end
                while ind_back >= 0 and (date_time_prev_end > date_time_current_end-timedelta(minutes=120)):
                    date_time_prev_start = datetime.strptime(alarm_list_of_tuples[ind_back][0], '%Y-%m-%d %H:%M:%S')
                    date_time_prev_end = date_time_prev_start + timedelta(minutes=alarm_list_of_tuples[ind_back][1])
                    if date_time_current_start > date_time_prev_start + timedelta(minutes=120):

                        time_prev_start = alarm_list_of_tuples[ind_back][0]
                        duration += alarm_list_of_tuples[ind_back][1]
                        if date_time_prev_end > date_time_current_start - timedelta(minutes=120):
                            accum_time += ((date_time_prev_end - (
                                        date_time_current_start - timedelta(minutes=120)))).seconds / 60

                            flapping_ocurrences += 1
                            print('t2')
                            delta = (date_time_prev_end - (date_time_current_start - timedelta(minutes=120)))
                            # print(delta.seconds/60)
                        break

                    else:
                        accum_time += alarm_list_of_tuples[ind_back][1]
                        duration += alarm_list_of_tuples[ind_back][1]
                        date_time_prev_start = datetime.strptime(alarm_list_of_tuples[ind_back][0], '%Y-%m-%d %H:%M:%S')
                        time_prev_start = alarm_list_of_tuples[ind_back][0]
                        flapping_ocurrences += 1
                    ind_back -= 1
                    print('is2')

                print(accum_time, flapping_ocurrences)
                if accum_time > 15:
                    if 0:
                        # check 3 - less time, but more occurrences exist?
                        pass
                    else:
                        list_flappings.append({'service_id': alarm_id, 'start': time_prev_start, 'duration': duration,
                                               'end': str(date_time_current_end), 'amount_outages': flapping_ocurrences,
                                               'sum_outages': accum_time})
                        break


    return list_flappings
