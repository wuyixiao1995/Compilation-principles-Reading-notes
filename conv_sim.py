from bokeh.plotting import figure, show
from bokeh.transform import linear_cmap
from bokeh.palettes import RdBu
from bokeh.models import ColumnDataSource, HoverTool, WheelZoomTool, PanTool
import numpy as np
from bokeh.models import ColorBar, LinearColorMapper
from bokeh.layouts import column

from bokeh.plotting import figure, show
from bokeh.transform import linear_cmap
from bokeh.palettes import RdBu
from bokeh.models import ColumnDataSource, HoverTool, WheelZoomTool, PanTool
import numpy as np
from bokeh.models import ColorBar, LinearColorMapper
from bokeh.layouts import column

def create_heatmap_with_legend(data, title="Heatmap with Legend", additional_info=None):
    # 确定输入张量的维度
    rows, cols = data.shape

    # 根据数据中的最小值和最大值创建颜色映射
    low, high = np.min(data), np.max(data)
    mapper = linear_cmap(field_name='values', palette=RdBu[9], low=low, high=high)

    # 创建热图的数据源
    x, y = np.arange(cols), np.arange(rows)
    xx, yy = np.meshgrid(x, y)
    source_data = {"x": xx.ravel(), "y": yy.ravel(), "values": data.ravel()}

    if additional_info is not None:
        for i, info in enumerate(additional_info):
            source_data[f"additional_info_{i+1}"] = info.ravel()

    source = ColumnDataSource(data=source_data)

    # 创建主要的热图绘图
    p = figure(width=600, height=600, tools=[WheelZoomTool(), PanTool()], title=title)
    p.x_range.range_padding = p.y_range.range_padding = 0
    rect = p.rect(x="x", y="y", width=1, height=1, source=source, fill_color=mapper, line_color=None)

    # 添加用于工具提示的HoverTool
    tooltips = [("数值", "@values"), ("X位置", "@x"), ("Y位置", "@y")]

    if additional_info is not None:
        for i in range(len(additional_info)):
            tooltips.append((f"额外信息 {i+1}", f"@additional_info_{i+1}"))

    hover = HoverTool(tooltips=tooltips, renderers=[rect])
    p.add_tools(hover)

    # 创建简化的图例
    color_mapper = LinearColorMapper(palette=RdBu[9], low=low, high=high)
    color_bar = ColorBar(color_mapper=color_mapper, location=(0, 0))
    p.add_layout(color_bar, 'below')

    # 显示布局
    show(p)

# 示例用法：
# 创建一个随机的 5x5 二维张量用于演示
data = np.random.uniform(-12, 12, size=(15, 25))

# 假设有两个矩阵 additional_info1 和 additional_info2 与 data 具有相同的尺寸
additional_info1 = np.random.rand(15, 25)
additional_info2 = np.random.rand(15, 25)

create_heatmap_with_legend(data, title="Custom Heatmap", additional_info=[additional_info1, additional_info2])
