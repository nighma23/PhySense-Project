from math import isclose

def check_peaks_data(data1: list, data2: list, data3: list) -> bool:
    # print(f"{data1=},{data2=},{data3=}")
    delta = 0.4
    max1_1 = max(data1)
    data1.remove(max1_1)
    max1_2 = max(data1)

    max2_1 = max(data2)
    data2.remove(max2_1)
    max2_2 = max(data2)

    max3_1 = max(data3)
    data3.remove(max3_1)
    max3_2 = max(data3)

    d1 = max1_2 / max1_1
    d2 = max2_2 / max2_1
    d3 = max3_2 / max3_1

    print(f"{d1:.2f}, {d2:.2f}, {d3:.2f}")

    if isclose(d1, d2, rel_tol=delta) and isclose(d2, d3, rel_tol=delta):

        return True
    return False
