from for_parser import ForGetter
import glob


def get_jsons(source: str, index_base: int) -> tuple[str, int]:
    jsons = ""
    getter = ForGetter(source)
    forlist = getter.scan_source()
    for ind, fo in enumerate(forlist):
        jsons += getter.to_json(fo, ind + index_base) + "\n"
    return (jsons, index_base + len(forlist))


def add_json(path: str, data: str) -> None:
    with open(path, mode='a') as f:
        f.write(data)


files = glob.glob("./datas/sample/*")
index = 0
for file in files:
    with open(file, 'r', encoding="utf-8") as f:
        text = f.read()
        json, index = get_jsons(text, index)
        add_json("data.jsonl", json)
