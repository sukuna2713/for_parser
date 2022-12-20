from for_parser import ForGetter
import glob


def get_jsons(source: str) -> str:
    jsons = ""
    getter = ForGetter(source)
    forlist = getter.scan_source()
    print(getter.to_input_string(forlist))
    for ind, fo in enumerate(forlist):
        jsons += getter.to_json(fo, ind) + "\n"
    return jsons


files = glob.glob("./datas/sample/*")
for file in files:
    print(file)
    with open(file, 'r', encoding="utf-8") as f:
        text = f.read()
        print(get_jsons(text))
