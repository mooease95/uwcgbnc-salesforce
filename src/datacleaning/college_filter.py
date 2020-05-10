import os
import argparse as ap
import re
import pandas as pd
import numpy as np


def create_arg_parser():
    parser = ap.ArgumentParser(description='UWCGB Salesforce files to clean data')
    parser.add_argument('-input', help='The csv file to be cleaned')
    parser.add_argument('--ref', help='Reference to help clean the data')
    return parser


def create_output_directory(directory_name):
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)
        print("Directory ", directory_name, " created.")
    else:
        print("Directory ", directory_name, " already exists.")


def create_input_paths(args, directory_name):
    if not os.path.exists(directory_name):
        return -1

    input_filename = args.input
    ref_filename = args.ref


def get_input(input_file):
    input_df = pd.read_excel(input_file)
    return input_df


def parse_ref(line):
    college_names = line.split('=')
    if len(college_names) == 2:
        valid_college_name = college_names[0]
        college_name_variations = college_names[1]
        college_name_variations = college_name_variations.split(',')
    else:
        return -1
    return valid_college_name, college_name_variations


def get_ref(ref_file):
    ref_dict = {}
    with open(ref_file, 'r') as file:
        for line in file:
            valid_college_name, colleges = parse_ref(line.strip())
            ref_dict[valid_college_name] = colleges
    return ref_dict


def clean_data(input_df, ref_dict):
    key_list = list(ref_dict.keys())
    value_list = list(ref_dict.values())
    for college in value_list:
        input_df.replace(to_replace=college, value=key_list[value_list.index(college)], inplace=True)
    return input_df



if __name__ == "__main__":
    args = create_arg_parser().parse_args()
    input_df = get_input(args.input)
    ref_dict = get_ref(args.ref)
    output_df = clean_data(input_df, ref_dict)
    output_df.reset_index(drop=True, inplace=True)
    output_df.to_excel('output.xlsx', index=False)
    pass
