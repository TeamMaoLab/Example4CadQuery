"""
直齿轮建模模块

简洁的直齿轮实现，基于CadQuery和标准渐开线齿廓。
参考标准：ISO 53:1998

作者: Example4CadQuery 项目团队
创建日期: 2025-08-07
"""

import math
import cadquery as cq
from cadquery.vis import show_object


class SpurGear:
    """直齿轮类"""
    
    def __init__(self, module, teeth_number, width, pressure_angle=20.0):
        """
        初始化直齿轮
        
        参数:
            module: 模数 (mm)
            teeth_number: 齿数
            width: 齿宽 (mm)
            pressure_angle: 压力角 (度)，默认20°
        """
        self.m = module
        self.z = teeth_number
        self.width = width
        self.alpha = math.radians(pressure_angle)
        
        # 计算基本尺寸
        self.d = module * teeth_number  # 分度圆直径
        self.da = self.d + 2 * module   # 齿顶圆直径
        self.df = self.d - 2.5 * module  # 齿根圆直径
        self.db = self.d * math.cos(self.alpha)  # 基圆直径
        
        # 半径
        self.r = self.d / 2
        self.ra = self.da / 2
        self.rf = self.df / 2
        self.rb = self.db / 2
        
        # 齿距角
        self.tooth_angle = 360 / teeth_number
    
    def _involute(self, t):
        """渐开线函数"""
        return math.tan(t) - t
    
    def _create_tooth_profile(self):
        """创建单个齿的2D轮廓 - 使用简化的渐开线近似"""
        
        # 渐开线函数
        def involute(alpha):
            return math.tan(alpha) - alpha
        
        # 计算齿厚
        tooth_thickness = math.pi * self.m / 2
        
        # 生成渐开线近似点
        points = []
        num_points = 12
        
        # 左侧渐开线（从齿根到齿顶）
        for i in range(num_points):
            t = i / (num_points - 1)
            
            # 半径从齿根到齿顶
            r = self.rf + t * (self.ra - self.rf)
            
            # 计算渐开线偏移
            if r >= self.rb:
                alpha = math.acos(self.rb / r)
                inv_alpha = involute(alpha)
                theta = inv_alpha - tooth_thickness / (2 * self.r)
            else:
                # 在基圆内部，使用径向线
                theta = -tooth_thickness / (2 * self.r)
            
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            points.append((x, y))
        
        # 右侧渐开线（从齿顶到齿根）
        for i in range(num_points - 1, -1, -1):
            t = i / (num_points - 1)
            
            # 半径从齿根到齿顶
            r = self.rf + t * (self.ra - self.rf)
            
            # 计算渐开线偏移（右侧为负）
            if r >= self.rb:
                alpha = math.acos(self.rb / r)
                inv_alpha = involute(alpha)
                theta = -inv_alpha + tooth_thickness / (2 * self.r)
            else:
                # 在基圆内部，使用径向线
                theta = tooth_thickness / (2 * self.r)
            
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            points.append((x, y))
        
        return points
    
    def create_gear(self, bore_diameter=None):
        """
        创建齿轮实体
        
        参数:
            bore_diameter: 中心孔直径 (可选)
        
        返回:
            CadQuery实体
        """
        # 创建齿轮本体（使用齿根圆作为基础，而不是齿顶圆）
        gear = cq.Workplane("XY").circle(self.rf).extrude(self.width)
        
        # 获取齿形点
        tooth_points = self._create_tooth_profile()
        
        # 为每个齿添加齿形
        for i in range(self.z):
            angle = self.tooth_angle * i
            
            # 创建齿的实体
            wp = cq.Workplane("XY")
            
            # 移动到起始点
            start_x, start_y = tooth_points[0]
            wp = wp.moveTo(start_x, start_y)
            
            # 绘制齿形轮廓
            for x, y in tooth_points[1:]:
                wp = wp.lineTo(x, y)
            
            # 闭合并拉伸
            tooth_solid = wp.close().extrude(self.width)
            
            # 旋转到正确位置
            tooth_solid = tooth_solid.rotate((0, 0, 0), (0, 0, 1), angle)
            
            # 添加到齿轮上（齿形会突出于齿轮本体）
            gear = gear.union(tooth_solid)
        
        # 添加中心孔
        if bore_diameter and bore_diameter > 0:
            gear = gear.faces(">Z").workplane().circle(bore_diameter/2).cutThruAll()
        
        return gear


def create_spur_gear(module=2.0, teeth_number=20, width=10.0, 
                     pressure_angle=20.0, bore_diameter=8.0):
    """
    便捷函数：创建直齿轮
    
    参数:
        module: 模数 (mm)
        teeth_number: 齿数  
        width: 齿宽 (mm)
        pressure_angle: 压力角 (度)
        bore_diameter: 中心孔直径 (mm)
    
    返回:
        CadQuery实体
    """
    gear = SpurGear(module, teeth_number, width, pressure_angle)
    return gear.create_gear(bore_diameter)


# 示例和测试函数
def example_gear():
    """创建示例齿轮"""
    print("创建示例直齿轮...")
    
    gear = create_spur_gear(
        module=3.0,
        teeth_number=16,
        width=8.0,
        bore_diameter=8.0
    )
    
    # 显示信息
    bbox = gear.val().BoundingBox()
    print(f"齿轮尺寸: {bbox.xlen:.1f} × {bbox.ylen:.1f} × {bbox.zlen:.1f} mm")
    print(f"体积: {gear.val().Volume():.0f} mm³")
    
    return gear


if __name__ == "__main__":
    # 运行示例
    gear = example_gear()
    
    # 尝试显示
    try:
        show_object(gear)
        print("齿轮已显示")
    except:
        print("无法显示3D模型")
    
    # 导出文件
    try:
        import os
        os.makedirs("output", exist_ok=True)
        cq.exporters.export(gear, "output/example_spur_gear.stl")
        print("齿轮已导出为STL文件")
    except:
        print("文件导出失败")