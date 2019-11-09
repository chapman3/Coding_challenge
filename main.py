import csv
import json
import operator
from statistics import median, mean
from datetime import datetime, timezone


def parse_csv(filename):
    # assumes headers are id, timestamp, value
    ret_dict = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if(row['id'] in ret_dict.keys()):
                ret_dict[row['id']].update({row['timestamp']: int(row['value'])})
            else:
                ret_dict[row['id']] = {row['timestamp']: int(row['value'])}
    return ret_dict


def get_max(parsed_dict):
    max_vals = []
    for key in parsed_dict:
        max_val = max(parsed_dict[key], key=parsed_dict[key].get)
        max_vals.append((key, max_val, parsed_dict[key][max_val]))
    maximum = (max(max_vals, key=lambda item:item[2]))
    return maximum[0], maximum[1]


def get_average(parsed_dict):
    averages = []
    for key in parsed_dict:
        temp_averages = []
        for val in parsed_dict[key].values():
            temp_averages.append(val)
        averages.append((key,mean(temp_averages)))
    return averages


def get_median(parsed_dict):
    medians = []
    for key in parsed_dict:
        temp_medians = []
        for val in parsed_dict[key].values():
            temp_medians.append(val)
        medians.append((key,median(temp_medians)))
    return medians


def print_readable(parsed_dict):
    for key in parsed_dict:
        for k,v in parsed_dict[key].items():
            print(key + " | " + str(datetime.fromtimestamp(int(k), timezone.utc)) + " | " + str(v))


def transform_json(parsed_dict):
    new_dict = {}
    i = 0
    for key in parsed_dict:
        temp_dict = [{'timestamp': k, 'value':v} for k,v in parsed_dict[key].items()]
        new_dict[i] = {'id':key, 'children': temp_dict}
        i = i+1
    with open('result.json', 'w') as jfile:
        json.dump(new_dict, jfile, indent=4)


def main():
    # parse csv
    parsed_dict = parse_csv('input.csv')
    # get maximum
    print("Maximum:")
    print(get_max(parsed_dict))
    # get average
    print("Averages:")
    print(get_average(parsed_dict))
    # get median
    print("Medians:")
    print(get_median(parsed_dict))
    # print readable using UTC timezone
    print("Data with readable datetimes:")
    print_readable(parsed_dict)
    # create json
    print("Generating json file")
    transform_json(parsed_dict)

if __name__ == "__main__":
    """
    Question 2.b. write up:
    The json model I would use would be as follows:
        {
            "id": 1000,
            "children": [
                {"timestamp": timestamp1, "value": value1},
                ...
            ]
        }
    However, at the end of this I see that the way I constructed my dictionary makes it difficult
    for me to simply generate the above sketched out plan with a simple json.dump call, so I first needed
    to make some adjustments to the dictionary that I was generating the json from. If I was doing this again,
    I think I would have made those adjustments from the parsing stage and used that model throughout the rest
    of the exercise. See results.json for the resulting json file.

    In finishing this up I noticed that the dict.update function I was using was making it so that
    only the seecond id and children were showing up. with more time I could figure this out, but for now
    I hacked a dummy id together to show the full output. 
    """
    """
    Question 3 Write up:
    """
    """
    a:
    class Data(models.Model):
        id = models.IntegerField() # I am assuming id is explicitly set, not sequentially generated
        timestamp = models.DateTimeField() # would need to handle conversion from epoch time
        value = models.IntegerField()
        
        class Meta:
            unique_together = (id, timestamp)
    """
    """
    b: get all Data objects with id 1001, order descencing by timestamp:
    Data.objects.filter(id=1001).order_by('-timestamp')
    """
    main()