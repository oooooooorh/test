from pathlib import Path
import plotly.express as px
import pandas as pd
import json

# 路径设置
path = Path('eq_data_30_day_m1.geojson')

# 读取文件内容
try:
    with path.open('r', encoding='utf-8') as file:
        geojson_data = json.load(file)
except OSError as e:
    print(f"无法读取文件: {e}")
    exit(1)

# 检查 GeoJSON 数据结构
if 'features' not in geojson_data:
    print("GeoJSON 数据结构不正确，未找到 'features' 键。")
    exit(1)

# 提取地震数据
lats, lons, titles, mags = [], [], [], []
for feature in geojson_data['features']:
    if 'geometry' in feature and 'coordinates' in feature['geometry'] and \
            'properties' in feature and 'mag' in feature['properties'] and \
            'title' in feature['properties']:
        lon= feature['geometry']['coordinates'][0]
        lat= feature['geometry']['coordinates'][1]
        mag = feature['properties']['mag']
        title = feature['properties']['title']

        lats.append(lat)
        lons.append(lon)
        titles.append(title)
        mags.append(mag)

    # 创建 DataFrame
df = pd.DataFrame(
    data=list(zip(lons, lats, titles, mags)),
    columns=['经度', '纬度', '位置', '震级']
)

# 创建带有世界地图背景的散点图
fig = px.scatter_geo(
    df,
    lat='纬度',
    lon='经度',
    size='震级',
    color='震级',
    hover_name='位置',
    hover_data=['震级'],
    projection="natural earth",  # 使用自然地球投影
    animation_frame=None,
    title="最近30天地震分布"
)

# 更新布局以优化显示
fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    geo_scope='world',  # 设置地图范围为世界
    geo_showland=True,  # 显示陆地
    geo_landcolor="rgb(220, 220, 220)",  # 设置陆地颜色
    geo_showocean=True,  # 显示海洋
    geo_oceancolor="rgb(0, 0, 128)",  # 设置海洋颜色
    geo_showcountries=True,  # 显示国家边界
    geo_countrycolor="rgb(50, 50, 50)"  # 设置国家边界颜色
)

# 显示图形
fig.show()

# 保存图形为 HTML 文件
fig.write_html('global_earthquake_map.html')