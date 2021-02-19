import json

class ProductionRecord:
    count = 0
    fairy_count = 0
    special_fairy_count = 0
    fairies = []
    equipment_count = 0
    equipment = []

    def __init__(self, count, fairy_count, special_fairy_count=-1, fairies=[], equipment_count=-1, equipment=[]):
        self.count = count
        self.fairy_count = fairy_count
        self.special_fairy_count = special_fairy_count
        self.fairies = fairies
        self.equipment_count = equipment_count
        self.equipment = equipment


class ProductionResult:
    result = {}

    def new_recipe(self, recipe):
        # 1 - 500 * 4，2 - 2021，3 - 0221，4 - 2221
        if recipe not in self.result.keys():
            self.result[recipe] = []

    def write(self):
        with open('./fairy_result.json', 'w') as f:
            json.dump(self.result, f)

    def record(self):
        first = input('使用已有数据吗？（y - 是，n - 否）\n')
        if first == 'y':
            self.result = json.load(open('./fairy_result.json'))
            json.dump(self.result, open('./temp/fairy_result_%d.json' % len(self.result), 'w'))
        while True:
            self.write()
            recipe = int(input('请输入公式（1 - 500 * 4，2 - 2021，3 - 0221，4 - 2221，0 - 结束录入）\n'))
            if recipe == 0:
                break
            gear = int(input('请输入档位\n'))
            recipe = 10 * recipe + gear
            self.new_recipe(recipe)
            count = int(input('建造次数\n'))
            fairy_count = int(input('妖精数量\n'))
            special_fairy_count = int(input('高耗妖精数量（无数据则输入-1）\n'))
            if special_fairy_count == -1:
                self.result[recipe].append([count, fairy_count, -1, [], -1, []])
                continue
            fairies = []
            f = ''
            print('请输入妖精明细，举例：空降10（无数据则输入q，结束则输入0）')
            while True:
                f = input('')
                if f == 'q' or f == '0':
                    break
                fairies.append(f)
            if f == 'q':
                self.result[recipe].append([count, fairy_count, special_fairy_count, [], -1, []])
                continue
            equipment_count = int(input('金装数量（无数据则输入-1）\n'))
            if equipment_count == -1:
                self.result[recipe].append([count, fairy_count, special_fairy_count, fairies, -1, []])
                continue
            equipment = []
            e = ''
            print('请输入金装明细，举例：光瞄10（无数据则输入q，结束则输入0）')
            while True:
                e = input('')
                if e == 'q' or e == '0':
                    break
                equipment.append(e)
            if e == 'q':
                self.result[recipe].append([count, fairy_count, special_fairy_count, fairies, equipment_count, []])
                continue
            else:
                self.result[recipe].append([count, fairy_count, special_fairy_count, fairies, equipment_count, equipment])
                continue
        self.write()

    def analyse(self):
        self.result = json.load(open('./fairy_result.json'))
        recipe = int(input('请输入公式（0 - 所有，1 - 500 * 4，2 - 2021，3 - 0221，4 - 2221）\n'))
        gear = int(input('请输入档位\n'))
        special = input('是否只算高耗？（y - 是，n - 否）\n')
        recipe = str(10 * recipe + gear)
        local_result = self.result[recipe]
        total_production = 0
        total_fairy_count = 0
        for record in local_result:
            if special == 'n' or record[2] >= 0:
                total_production += record[0]
            if special == 'n':
                total_fairy_count += record[1]
            elif record[2] >= 0:
                total_fairy_count += record[2]
        print('共%d次建造记录' % total_production)
        print('共%d只妖精' % total_fairy_count)
        print('妖精率为%.2f%%' % (100 * total_fairy_count / total_production))

    def basic_info(self):
        self.result = json.load(open('./fairy_result.json'))
        total_production = 0
        total_fairy_count = 0
        for k in self.result.keys():
            print(k)
            local_production = 0
            for record in self.result[k]:
                local_production += record[0]
                total_production += record[0]
                total_fairy_count += record[1]
            print('当前档位%d次建造记录' % local_production)
        print('共%d次建造记录' % total_production)


if __name__ == '__main__':
    r = ProductionResult()
    r.analyse()