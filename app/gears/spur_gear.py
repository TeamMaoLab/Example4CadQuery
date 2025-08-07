"""
高精度直齿轮建模模块

基于标准渐开线理论的高精度直齿轮实现。
参考标准：ISO 53:1998
参考实现：CQ_Gears项目中的spur_gear.py

作者: Example4CadQuery 项目团队
创建日期: 2025-08-07
"""

import numpy as np
import cadquery as cq
from cadquery.vis import show_object


class SpurGear:
    """高精度直齿轮类"""
    
    def __init__(self, module, teeth_number, width, 
                 pressure_angle=20.0, clearance_coeff=0.25, backlash=0.0,
                 addendum_coeff=1.0, dedendum_coeff=1.25):
        """
        初始化高精度直齿轮
        
        参数:
            module: 模数 (mm)
            teeth_number: 齿数
            width: 齿宽 (mm)
            pressure_angle: 压力角 (度)，默认20°
            clearance_coeff: 顶隙系数，默认0.25
            backlash: 齿侧间隙 (mm)
            addendum_coeff: 齿顶高系数，默认1.0
            dedendum_coeff: 齿根高系数，默认1.25
        """
        # 基本参数
        self.m = module
        self.z = teeth_number
        self.width = width
        self.a0 = np.radians(pressure_angle)
        self.clearance_coeff = clearance_coeff
        self.backlash = backlash
        self.addendum_coeff = addendum_coeff
        self.dedendum_coeff = dedendum_coeff
        
        # 计算齿轮几何尺寸（符合Wiki标准）
        self.d = self.m * self.z  # 分度圆直径 d
        self.ha = self.addendum_coeff * self.m  # 齿顶高 ha = 1.00m
        self.hf = self.dedendum_coeff * self.m  # 齿根高 hf = 1.25m
        self.h = self.ha + self.hf  # 全齿高 h = 2.25m
        self.c = self.clearance_coeff * self.m  # 顶隙 c = 0.25m
        
        # 计算各圆直径
        self.da = self.d + 2.0 * self.ha  # 齿顶圆直径 da = d + 2ha
        self.df = self.d - 2.0 * self.hf  # 齿根圆直径 df = d - 2hf
        self.p = np.pi * self.m  # 齿距 p = πm
        self.s = self.m * (np.pi / 2.0 - self.backlash * np.tan(self.a0))  # 分度圆齿厚
        
        # 计算各圆半径
        self.r = self.d / 2.0  # 分度圆半径
        self.ra = self.da / 2.0  # 齿顶圆半径
        self.rf = self.df / 2.0  # 齿根圆半径
        self.rb = np.cos(self.a0) * self.d / 2.0  # 基圆半径
        self.rr = max(self.rb, self.rf)  # 齿根半径(取基圆和齿根圆较大者)
        
        # 齿距角
        self.tau = np.pi * 2.0 / self.z
        
        # 检查齿根圆直径是否有效
        if self.df <= 0:
            raise ValueError(
                f"无效的齿根圆直径: {self.df:.3f}mm。请检查模数、齿数和齿根高系数。"
            )
        
        # 渐开线计算点数
        self.curve_points = 20
    
    def _involute_function(self, alpha):
        """渐开线函数: inv(alpha) = tan(alpha) - alpha"""
        return np.tan(alpha) - alpha
    
    def _calculate_involute_points(self):
        """计算渐开线点"""
        # 在齿根半径到齿顶半径之间生成点
        r = np.linspace(self.rr, self.ra, self.curve_points)
        
        # 计算对应的角度
        cos_a = self.r / r * np.cos(self.a0)
        a = np.arccos(np.clip(cos_a, -1.0, 1.0))
        inv_a = self._involute_function(a)
        inv_a0 = self._involute_function(self.a0)
        s = r * (self.s / self.d + inv_a0 - inv_a)
        phi = s / r
        
        # 左侧渐开线点
        self.t_lflank_pts = np.dstack((np.cos(phi) * r,
                                       np.sin(phi) * r,
                                       np.zeros(self.curve_points))).squeeze()
        
        # 齿顶圆弧点
        b = np.linspace(phi[-1], -phi[-1], self.curve_points)
        self.t_tip_pts = np.dstack((np.cos(b) * self.ra,
                                    np.sin(b) * self.ra,
                                    np.zeros(self.curve_points))).squeeze()
        
        # 右侧渐开线点（镜像左侧）
        self.t_rflank_pts = np.dstack(((np.cos(-phi) * r)[::-1],
                                       (np.sin(-phi) * r)[::-1],
                                       np.zeros(self.curve_points))).squeeze()
        
        # 齿根圆弧点 - 正确计算齿根圆弧
        rho = self.tau - phi[0] * 2.0
        # 齿根圆弧的起点是右侧渐开线的终点
        start_angle = -phi[0]
        # 齿根圆弧的终点是下一个齿的左侧渐开线的起点
        end_angle = -phi[0] - rho
        
        # 在齿根圆上生成点
        root_angles = np.linspace(start_angle, end_angle, self.curve_points)
        self.t_root_pts = np.dstack((np.cos(root_angles) * self.rr,
                                     np.sin(root_angles) * self.rr,
                                     np.zeros(self.curve_points))).squeeze()
    
    def _create_tooth_profile(self):
        """创建单个齿的2D轮廓"""
        # 计算渐开线点
        self._calculate_involute_points()
        
        # 组合所有点
        pts = np.concatenate((self.t_lflank_pts, self.t_tip_pts,
                              self.t_rflank_pts, self.t_root_pts))
        
        # 转换为CadQuery点，确保没有重复点
        cq_pts = []
        for pt in pts:
            # 检查是否与最后一个点相同
            if not cq_pts or not (abs(cq_pts[-1].x - pt[0]) < 1e-6 and abs(cq_pts[-1].y - pt[1]) < 1e-6):
                cq_pts.append(cq.Vector(pt[0], pt[1], 0))
        
        return cq_pts

    def create_gear(self, bore_diameter=None):
        """
        创建齿轮实体
        
        参数:
            bore_diameter: 中心孔直径 (可选)
        
        返回:
            CadQuery实体
        """
        # 创建齿轮基体（使用齿根圆作为基础）
        gear = cq.Workplane("XY").circle(self.rr).extrude(self.width)
        
        # 创建单个齿的轮廓
        tooth_points = self._create_tooth_profile()
        
        # 检查点的数量
        if len(tooth_points) < 3:
            raise ValueError("齿形点数不足，无法创建轮廓")
        
        # 创建第一个齿的实体
        wp = cq.Workplane("XY")
        wp = wp.polyline(tooth_points).close()
        tooth = wp.extrude(self.width)
        
        # 复制并旋转创建所有齿，并添加到基体上
        for i in range(self.z):
            angle = np.degrees(self.tau * i)
            rotated_tooth = tooth.rotate((0, 0, 0), (0, 0, 1), angle)
            gear = gear.union(rotated_tooth)
        
        # 添加中心孔
        if bore_diameter and bore_diameter > 0:
            gear = gear.faces(">Z").workplane().circle(bore_diameter/2).cutThruAll()
        
        return gear


def create_spur_gear(module=2.0,
                     teeth_number=20,
                     width=10.0,
                     pressure_angle=20.0,
                     clearance_coeff=0.25,
                     backlash=0.0,
                     addendum_coeff=1.0,
                     dedendum_coeff=1.25,
                     bore_diameter=8.0):
    """
    便捷函数：创建高精度直齿轮
    
    参数:
        module: 模数 (mm)
        teeth_number: 齿数  
        width: 齿宽 (mm)
        pressure_angle: 压力角 (度)
        clearance_coeff: 顶隙系数，默认0.25
        backlash: 齿侧间隙 (mm)
        addendum_coeff: 齿顶高系数
        dedendum_coeff: 齿根高系数
        bore_diameter: 中心孔直径 (mm)
    
    返回:
        CadQuery实体
    """
    gear = SpurGear(module, teeth_number, width, pressure_angle, 
                   clearance_coeff, backlash, addendum_coeff, dedendum_coeff)
    return gear.create_gear(bore_diameter)


def print_gear_parameters(gear_obj):
    """打印齿轮参数信息"""
    print("\n" + "="*60)
    print("齿轮参数信息 (符合Wiki标准)")
    print("="*60)
    print(f"模数 m = {gear_obj.m:.2f} mm")
    print(f"齿数 z = {gear_obj.z}")
    print(f"压力角 α = {np.degrees(gear_obj.a0):.1f}°")
    print(f"齿距 p = πm = {gear_obj.p:.3f} mm")
    print("-"*60)
    print("几何尺寸:")
    print(f"分度圆直径 d = mz = {gear_obj.d:.2f} mm")
    print(f"齿顶高 ha = {gear_obj.addendum_coeff}m = {gear_obj.ha:.2f} mm")
    print(f"齿根高 hf = {gear_obj.dedendum_coeff}m = {gear_obj.hf:.2f} mm")
    print(f"全齿高 h = ha + hf = {gear_obj.h:.2f} mm")
    print(f"顶隙 c = {gear_obj.clearance_coeff}m = {gear_obj.c:.2f} mm")
    print(f"工作齿高 hw = 2.00m = {2.0 * gear_obj.m:.2f} mm")
    print("-"*60)
    print("圆直径:")
    print(f"齿顶圆直径 da = d + 2ha = {gear_obj.da:.2f} mm")
    print(f"齿根圆直径 df = d - 2hf = {gear_obj.df:.2f} mm")
    print(f"基圆直径 db = d·cos(α) = {gear_obj.rb * 2:.2f} mm")
    print("-"*60)
    print("圆半径:")
    print(f"分度圆半径 r = {gear_obj.r:.2f} mm")
    print(f"齿顶圆半径 ra = {gear_obj.ra:.2f} mm")
    print(f"齿根圆半径 rf = {gear_obj.rf:.2f} mm")
    print(f"基圆半径 rb = {gear_obj.rb:.2f} mm")
    print("-"*60)
    print("重要计算说明:")
    print(f"实际齿根半径 rr = max(rb, rf) = {gear_obj.rr:.2f} mm")
    
    # 分析基圆和齿根圆的关系
    if gear_obj.rb > gear_obj.rf:
        print("⚠️  基圆半径 > 齿根圆半径")
        print("   说明：渐开线从基圆开始生成，实际齿轮基体使用基圆半径")
        print("   影响：调整齿根高系数对齿轮外形影响有限")
        print(f"   差值：rb - rf = {gear_obj.rb - gear_obj.rf:.2f} mm")
        print("   建议：如需齿根高系数更明显影响，可")
        print("         1. 增大齿数（减小基圆）")
        print("         2. 增大压力角（减小基圆）")
        print("         3. 减小齿根高系数")
    else:
        print("✅ 齿根圆半径 ≥ 基圆半径")
        print("   说明：实际齿轮基体使用齿根圆半径")
        print("   影响：调整齿根高系数会直接影响齿轮外形")
        print(f"   差值：rf - rb = {gear_obj.rf - gear_obj.rb:.2f} mm")
    
    # 计算临界点
    critical_teeth = int(2 * gear_obj.addendum_coeff / (1 - np.cos(gear_obj.a0)))
    print(f"\n临界齿数分析：")
    print(f"当前齿数 z = {gear_obj.z}")
    print(f"临界齿数（rf=rb）z_critical ≈ {critical_teeth}")
    if gear_obj.z < critical_teeth:
        print("⚠️  齿数较少，基圆 > 齿根圆")
    else:
        print("✅ 齿数充足，齿根圆 ≥ 基圆")
    
    print("="*60)


if __name__ == "__main__":
    # 运行示例
    gear_obj = SpurGear(
        # 模数 (mm) - 决定齿轮大小，增大则整体尺寸增大，承载能力增强
        2.0,
        # 齿数 - 影响传动比和平稳性，增多则传动更平稳，单齿承载减小
        40,
        # 齿宽 (mm) - 影响齿轮强度和接触面积，增宽则强度提高，但重量增加, 也可以理解为直齿轮的厚度
        3.0,
        # 压力角 (°) - 影响齿形和传动性能，增大则齿根强度提高，但传动效率略降
        20.0,
        # 顶隙系数 - 保证啮合间隙，增大则啮合更宽松，但传动精度降低
        0.5,
        # 齿侧间隙 (mm) - 防止卡死的热膨胀间隙，增大则传动有回差，但不易卡死
        0.0,
        # 齿顶高系数 - 标准值为1.0，增大则齿顶变尖，强度可能降低
        1.0,
        # 齿根高系数 - 标准值为1.25，增大则齿根加深，强度提高但加工困难
        1.25)

    print_gear_parameters(gear_obj)
    
    # 尝试显示
    try:
        show_object(gear_obj.create_gear())
        print("\n3D模型已显示")
    except:
        print("无法显示3D模型")