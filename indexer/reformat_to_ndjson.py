#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime

# 第一引数に処理するjsonファイルのパスを指定すること
filepath = sys.argv[1]
# ndjsonに変換したデータを入れる用の配列
ndjson = []

start_datetime = datetime.datetime.now()
print(f"{start_datetime.strftime('%Y/%m/%d %H:%M:%S')}: start converting {filepath}.")

# ファイルの各行を読み込んでBulk API用のactionを追加する
with open(filepath, encoding="utf-8") as f:
    for line in f:
        # 空行はスキップ
        if(line == '\n'):
            ndjson.append('\n')
            continue

        ndjson.append('{"index":{}}\n')
        ndjson.append(line)

# 作成したndjsonを新規ファイルに書き込む
new_filepath = filepath + "_new.ndjson"
with open(new_filepath, mode='w', encoding="utf-8") as f:
    f.writelines(ndjson)

finish_datetime = datetime.datetime.now()
processing_time = finish_datetime - start_datetime
print(f"{finish_datetime.strftime('%Y/%m/%d %H:%M:%S')}: {filepath} is converted to {new_filepath}({processing_time.seconds} sec).")
