import re

pattern = re.compile(r"(.+)\s*[(（](.+)[)）]\s*,(.+)")


def parse(file_contents: str) -> list[list[str]]:
    res = []
    for line_num, line in enumerate(file_contents.split("\n")):
        matches = pattern.search(line)

        if matches:
            res.append([matches[1], matches[2], matches[3]])
        else:
            print(f"could not parse line {line_num+1}: '{line}'")

    return res


if __name__ == "__main__":
    with open("../sets/set.txt", "r", encoding="utf8") as f:
        contents = f.read()

    print(parse(contents))
