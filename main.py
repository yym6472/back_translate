import tqdm
import json
import argparse

from back_translate import back_translate


def main(args):
    schemas = json.load(open(args.schema_file, "r"))
    if "keywords_file" in args:
        keywords = [line.strip() for line in open(args.keywords_file, "r")]
    else:
        keywords = None

    with open(args.input_file, "r") as f_in:
        lines = [line.strip() for line in f_in.readlines() if line.strip()]

    with open(args.output_file, "w") as f_out:
        for line in tqdm.tqdm(lines):
            ques, ans = line.split("\t")
            result_dict = back_translate(ques, schemas, keywords)
            for arg_ques in result_dict.values():
                f_out.write(f"{arg_ques}\t{ans}\n")
            f_out.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True)
    parser.add_argument("--output_file", type=str, required=True)
    parser.add_argument("--schema_file", type=str, required=True)
    parser.add_argument("--keywords_file", type=str, help="Required if keyword mask is applied")
    args = parser.parse_args()

    main(args)