#!/usr/bin/env python3
# -*- coding: utf8 -*-

def remove_duplicate_matches(matches, distance_threshold=10):
    """
    按位置去重匹配结果
    :param matches: 匹配结果列表
    :param distance_threshold: 距离阈值，两个匹配点距离小于此值视为重复
    :return: 去重后的匹配结果列表
    """
    if not matches:
        return []

    unique_matches = []

    for match in matches:
        is_duplicate = False

        # 计算当前位置
        current_top_left = match['top_left']
        current_bottom_right = match['bottom_right']
        current_center = (
            (current_top_left[0] + current_bottom_right[0]) / 2,
            (current_top_left[1] + current_bottom_right[1]) / 2
        )

        # 检查是否与已有的匹配点重复
        for unique_match in unique_matches:
            unique_top_left = unique_match['top_left']
            unique_bottom_right = unique_match['bottom_right']
            unique_center = (
                (unique_top_left[0] + unique_bottom_right[0]) / 2,
                (unique_top_left[1] + unique_bottom_right[1]) / 2
            )

            # 计算欧几里得距离
            distance = ((current_center[0] - unique_center[0]) ** 2 +
                        (current_center[1] - unique_center[1]) ** 2) ** 0.5

            if distance < distance_threshold:
                is_duplicate = True
                # 保留置信度更高的
                if match['confidence'] > unique_match['confidence']:
                    unique_matches.remove(unique_match)
                    unique_matches.append(match)
                break

        if not is_duplicate:
            unique_matches.append(match)

    return unique_matches

def analyze_match_positions(matches):
    """
    分析匹配结果的位置分布
    :param matches: 匹配结果列表
    :return: 统计信息字典
    """
    if not matches:
        return None

    # 提取y坐标
    y_coords = [match['relative_position'][1] for match in matches]

    # 去重并排序
    unique_y = sorted(list(set(y_coords)))

    # 统计每个y坐标的出现次数
    from collections import Counter
    y_counts = Counter(y_coords)

    return {
        'total_matches': len(matches),
        'unique_y_count': len(unique_y),
        'unique_y_values': unique_y,
        'min_y': min(unique_y),
        'max_y': max(unique_y),
        'y_distribution': dict(sorted(y_counts.items()))
    }