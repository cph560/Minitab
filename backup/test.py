from decimal import Decimal, ROUND_HALF_UP

num = Decimal('799.98')

if num<0:
    rounded_num = num.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)

    # 将Decimal对象转换为字符串，并去除末尾的无效0
    formatted_num = format(rounded_num, 'f')

    # 去除末尾的无效0
    formatted_num = formatted_num.rstrip('0').rstrip('.')
elif num<10:
    rounded_num = num.quantize(Decimal('.001'), rounding=ROUND_HALF_UP)

    # 将Decimal对象转换为字符串，并去除末尾的无效0
    formatted_num = format(rounded_num, 'f')

    # 去除末尾的无效0
    formatted_num = formatted_num.rstrip('0').rstrip('.')
elif num<100:
    rounded_num = num.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

    # 将Decimal对象转换为字符串，并去除末尾的无效0
    formatted_num = format(rounded_num, 'f')

    # 去除末尾的无效0
    formatted_num = formatted_num.rstrip('0').rstrip('.')
elif num<1000:
    rounded_num = num.quantize(Decimal('.1'), rounding=ROUND_HALF_UP)

    # 将Decimal对象转换为字符串，并去除末尾的无效0
    formatted_num = format(rounded_num, 'f')

    # # 去除末尾的无效0
    formatted_num = formatted_num.rstrip('0').rstrip('.')
else:
    formatted_num=round(num, 0)

print(formatted_num)  # 输出: 123.4568