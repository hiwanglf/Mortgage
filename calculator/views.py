from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def mortgage_average_capital(value, rate, year):
    """
    等额本金贷款方式还款表及清单计算
    :param value: 贷款额，单位万元
    :param rate:  贷款年利率
    :param year:  贷款年限
    :return: 包含还款信息的字典列表
    """
    # 等额本金
    l_value = int(value) * 10000            # 贷款总金额，转换为int
    l_rate = float(rate) / 1200             # 月利率，浮点数
    l_time = int(year) * 12                 # 换算时间为月
    data_benjin = []
    e_principal = l_value / l_time          # 每月应还本金是确定值

    for i in range(1, l_time+1):
        e_interest = (l_value - e_principal*(i-1)) * l_rate         # 利息=剩余未还*月利率
        e_pay = e_interest + e_principal
        surplus_principal = l_value - e_principal * i
        item = {
            "period": i,                                            # 还款期数
            "e_principal": round(e_principal, 2),                   # 当月本金
            "e_interest": round(e_interest, 2),                     # 当月利息
            "e_pay": round(e_pay, 2),                               # 当月还款额
            "surplus_principal": round(surplus_principal, 2)        # 剩余本金
        }
        data_benjin.append(item)
    return data_benjin


def mortgage_average_capital_plus_interest(value, rate, year):
    """
    等额本息贷款方式还款表及清单计算
    :param value: 贷款额，单位万元
    :param rate:  贷款年利率
    :param year:  贷款年限
    :return: 包含还款信息的字典列表
    """
    l_value = int(value) * 10000        # 贷款总金额，转换为int
    l_rate = float(rate) / 1200         # 月利率，浮点数
    l_time = int(year) * 12             # 换算时间为月
    data_benxi = []
    # 每月所还金额固定
    e_pay = (l_value * l_rate * ((1 + l_rate) ** l_time)) / ((1 + l_rate) ** l_time - 1)    # 当月还款定额
    for i in range(1, l_time + 1):
        e_interest = l_value * l_rate                                                       # 当月利息
        e_principal = e_pay - e_interest                                                    # 当月本金
        if l_value > 0:
            l_value = l_value - e_principal                                                 # 下期的本金减少
        surplus_principal = l_value                                                         # 剩余本金
        item = {
            "period": i,                                        # 还款期数
            "e_principal": round(e_principal, 2),               # 当月本金
            "e_interest": round(e_interest, 2),                 # 当月利息
            "e_pay": round(e_pay, 2),                           # 当月还款额
            "surplus_principal": round(surplus_principal, 2)    # 剩余本金
        }
        data_benxi.append(item)
    return data_benxi


def index(request):
    # return HttpResponse("Hello Python")
    if request.method == "GET":
        return render(request, "index.html")
    elif request.method == "POST":
        amount = request.POST.get("loan_amount", None)      # 贷款金额
        rate = request.POST.get("loan_rate", None)          # 贷款利率
        year = request.POST.get("loan_time", None)          # 贷款时长

        average_capital = mortgage_average_capital(amount, rate, year)
        average_capital_plus_interest = mortgage_average_capital_plus_interest(amount, rate, year)

        data_compare = []

        for i in range(1, int(year)*12+1):
            item = {
                "period": i,
                "e_principal1": average_capital[i-1]['e_principal'],                        # 当月本金
                "e_interest1": average_capital[i-1]['e_interest'],                          # 当月利息
                "e_pay1": average_capital[i-1]['e_pay'],                                    # 当月还款额
                "surplus_principal1": average_capital[i-1]['surplus_principal'],            # 剩余本金
                "e_principal2": average_capital_plus_interest[i-1]['e_principal'],          # 当月本金
                "e_interest2": average_capital_plus_interest[i-1]['e_interest'],            # 当月利息
                "e_pay2": average_capital_plus_interest[i-1]['e_pay'],                      # 当月还款额
                "surplus_principal2": average_capital_plus_interest[i-1]['surplus_principal']  # 剩余本金
            }
            data_compare.append(item)

        # 统计等额本金总利息和总还款额
        interest_benjin = 0
        pay_benjin = 0
        for i in range(0, int(year)*12):
            interest_benjin += average_capital[i]['e_interest']
            pay_benjin += average_capital[i]['e_pay']

        # 统计等额本息总利息和总还款额
        pay_benxi = average_capital_plus_interest[0]['e_pay'] * int(year) * 12
        interest_benxi = pay_benxi - int(amount) * 10000

        data_collect = [
            {
                "interest_all1": round(interest_benjin, 2),
                "pay_all1": round(pay_benjin, 2),
                "interest_all2": round(interest_benxi, 2),
                "pay_all2": round(pay_benxi, 2)
             }
        ]

    return render(request, "index.html", {"data1": data_compare, "data2": data_collect})

