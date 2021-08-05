import argparse
import json
import itertools
import threading
import time
import sys


done = False

# Animation loading
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone, please help to check the JSON file in the output folder! \n')

def transfer(
    input_file: str,
    output_file: str,
    is_allow_null: bool,
):
    """
    This method helps to read data from input file and write new JSON file.

    Args:
        input_file (str): Input file
        output_file (str): Output file
        is_allow_null (bool): Allow to set null or not?
                              If not, the value will be set ''
    """

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    is_allow_null = sys.argv[3]
    expected_result = []
    null_value = '' if is_allow_null else None

    t = threading.Thread(target=animate)
    t.start()
    sys.stdout.write('\rStarted the progress ...\n')

    # Read the input file
    with open(input_file, 'r') as input_data:
        data = json.loads(input_data.read())
        key_set = max(data.items(), key=lambda x : len(x[1][0]))[1][0]

        # Access data in json file and write the output file
        for i, v in data.items():
            real_data = data[i][0]
            expected_item = {}

            # Loop key_set to set the null value
            for key in key_set:
                value = real_data.get(key) if real_data.get(key) else null_value

                expected_item.update({key: value})

            expected_result.append(expected_item)

        # Close the input file
        input_data.close()

    with open(output_file, 'w') as output:
        output.write(str(json.dumps(expected_result)))
        output.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_in', help='The path of input file')
    parser.add_argument('file_out', help='The path of output file')
    parser.add_argument(
        'is_allow_null',
        help='Is allow null or not? if not, the value will be set \'\'',
        default=False
    )
    args = parser.parse_args()

    transfer(args.file_in, args.file_out, args.is_allow_null)

if __name__ == '__main__':
    main()
    done = True
