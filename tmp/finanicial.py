#! /usr/local/bin/python3
import csv
import re
import sys
import pdfplumber


def extract_tables(pdf: pdfplumber.pdf.PDF, output: str):
    names = ["1、合并资产负债表", "2、母公司资产负债表", "3、合并利润表",
             "4、母公司利润表", "5、合并现金流量表", "6、母公司现金流量表"]

    begin = end = 0
    for i in range(len(pdf.pages)):
        page = pdf.pages[i]
        text = page.extract_text()
        if re.search(names[0], text):
            begin = i
        if re.search(names[-1], text):
            end = i
    print(begin, end)

    with open(output, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        j = -1
        for i in range(begin, end + 1):
            page = pdf.pages[i]
            tables = page.extract_tables({"keep_blank_chars": True})
            for table in tables:
                if table[0][0] == "项目":
                    j += 1
                    if j % 2 == 0:
                        # print("\n" + names[j])
                        writer.writerow([])
                        writer.writerow([names[j]])
                if j % 2:
                    continue
                # print("new table", j)
                n = len(table)
                for k in range(n):
                    if table[k][0] is not None and\
                            (table[k][1] != "" or table[k][2] != "" or k == n - 1 or
                             table[k + 1][0] is not None):
                        if table[k][1] is None and table[k][2] is None:
                            table[k][0] = table[k - 2][0] + table[k][0]
                            table[k][1] = table[k - 1][1]
                            table[k][2] = table[k - 1][2]
                        # print(table[k])
                        writer.writerow(table[k])


def extract_tables2(pdf: pdfplumber.pdf.PDF, begin: int, end: int, output: str):
    with open(output, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        for i in range(begin, end + 1):
            page = pdf.pages[i]
            tables = page.extract_tables()
            for table in tables:
                n = len(table)
                for k in range(n):
                    if table[k][0] is not None and \
                            (table[k][1] != "" or table[k][2] != "" or k == n - 1 or
                             table[k + 1][0] is not None):
                        if table[k][1] is None and table[k][2] is None:
                            table[k][0] = table[k - 2][0] + table[k][0]
                            table[k][1] = table[k - 1][1]
                            table[k][2] = table[k - 1][2]
                        # print(table[k])
                        writer.writerow(table[k])


def main():
    n = len(sys.argv)
    if n < 2:
        print('Usage: ' + sys.argv[0] + ' pdf')
        sys.exit(1)

    with pdfplumber.open(sys.argv[1]) as pdf:
        if n == 2:
            extract_tables(pdf, re.sub("\.pdf", ".csv", sys.argv[1]))
        elif n == 4:
            begin = int(sys.argv[2])
            end = int(sys.argv[3])
            output = re.sub("\.pdf", "_{}_{}.csv".format(sys.argv[2], sys.argv[3]), sys.argv[1])
            extract_tables2(pdf, begin, end, output)


if __name__ == "__main__":
    main()
