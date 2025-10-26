# Rockfall-Simulation
**基于数字高程模型（DEM），开发了一个简单的岩石坠落运动模拟工具，能够预测岩石在地形上的运动轨迹，并进行可视化。可以通过图形化界面设置参数、加载数据并运行模拟**
## 使用方法
（1）加载 DEM 数据  

（2）设置各项参数  

（3）开始模拟，可视化落石运动轨迹
## 注意事项
（1）目前数据只支持 ASCII DEM （.asc）

（2）支持自定义：
- 初始位置 Start Row, Start Col
- 时间步长 Time Step
- 最大步数 Max Steps
- 摩擦系数 Friction
- 像元大小（空间分辨率） Cellsize
- 重力（或许可以模拟月球场景） Gravity

（3）示例数据为 random_dem_500x500.asc 由AI生成，并非真实地形

--SteCheng 2025/10/26
