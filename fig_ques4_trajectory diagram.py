import matplotlib.pyplot as plt
import numpy as np

# 参数从代码中提取
R1 = 5.566688015613427
x1, y1 = -1.7630984055082974, 11.700150365918836
R2 = 2.7833440078067135
x2, y2 = 1.298654145997392, 3.9367679651678076

# 创建圆1（完整圆）
theta1 = np.linspace(0, 2 * np.pi, 100)
x1_circle = x1 + R1 * np.cos(theta1)
y1_circle = y1 + R1 * np.sin(theta1)

# 创建圆2（完整圆）
theta2 = np.linspace(0, 2 * np.pi, 100)
x2_circle = x2 + R2 * np.cos(theta2)
y2_circle = y2 + R2 * np.sin(theta2)

# 设置图形
fig, ax = plt.subplots()
ax.plot(x1_circle, y1_circle, label='Circle 1', color='orange')
ax.plot(x2_circle, y2_circle, label='Circle 2', color='blue')

# 绘制圆弧中心
ax.plot(x1, y1, 'ro', label='Center 1')
ax.plot(x2, y2, 'bo', label='Center 2')

# 标注龙头的初始位置
initial_position_x = x1 - R1
initial_position_y = y1
ax.plot(initial_position_x, initial_position_y, 'go', label='Dragon Head Initial Position')

# 设置轴范围和标签
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Optimized Path Visualization')
ax.legend()
ax.grid(True)
ax.set_aspect('equal')

# 保存图像到文件
plt.savefig('D:\\optimized_circles_visualization.png')

# 显示图形
plt.show()
