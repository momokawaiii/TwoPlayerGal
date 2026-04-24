init:
    image heart_particle = "R.png"

    # 增加了一个参数：rot (旋转角度)
    transform particle_fly_spread(sx, ex, h, t, d, sc, rot):
        subpixel True
        # 初始状态
        alpha 0.0 xoffset sx yoffset 0 zoom 0.0 rotate 0
        
        pause d
        
        block:
            # 重置
            alpha 0.0 xoffset sx yoffset 0 zoom 0.0 rotate 0
            
            parallel:
                # 显现
                easein 0.3 alpha 1.0
                easein 0.3 zoom sc
                pause (t - 0.8)
                easeout 0.5 alpha 0.0
                
            parallel:
                # 向上飘 (减速上升，模拟浮力)
                easeout t yoffset h
                
            parallel:
                # 横向扩散 (加速扩散，模拟风吹)
                easein t xoffset ex
                
            parallel:
                # 顺着方向慢慢旋转
                ease t rotate rot
            
            # 随机微小停顿
            choice:
                pause 0.1
            choice:
                pause 0.2
                
            repeat

    screen heart_explosion(x, y, duration=3.0, particle_count=30):
        zorder 100
        default particles = generate_particles(particle_count)

        fixed:
            pos (x, y)
            anchor (0.5, 0.5)
            xysize (0, 0)
            
            for p in particles:
                # p[6] 是新增的旋转角度
                add "heart_particle" at particle_fly_spread(p[0], p[1], p[2], p[3], p[4], p[5], p[6])

        timer duration action Hide("heart_explosion")
init python:
    import random

    def generate_particles(count):
        data = []
        for i in range(count):
            # 1. 随机决定左右 (-1 左, 1 右)
            side = random.choice([-1, 1])
            
            # 2. 起始位置 (X轴)
            # 稍微靠近身体一点，方便往外飘
            start_x = side * random.randint(40, 150)
            
            # 3. 【关键修改】结束位置 (X轴)
            # 终点 = 起点 + 向外的偏移量
            # 这样左边的会往左飘，右边的会往右飘
            spread_distance = random.randint(80, 250) # 向外飘 80 到 250 像素
            end_x = start_x + (side * spread_distance)
            
            # 4. 上升高度 (Y轴)
            height = -random.randint(300, 500)
            
            # 5. 飞行时间
            time = random.uniform(1.8, 3.5)
            
            # 6. 初始延迟
            delay = random.uniform(0.0, 2.5)
            
            # 7. 大小
            scale = random.uniform(0.5, 1.0)
            
            # 8. 【新增】旋转角度
            # 往左飘就向左歪，往右飘就向右歪
            rot = side * random.randint(10, 30)
            
            data.append((start_x, end_x, height, time, delay, scale, rot))
            
        return data

# 封装函数
    def stream_hearts(pos_name="center", duration=2.5, count=40):
        positions = {
            "left": (0.2, 0.4),   
            "center": (0.5, 0.4), 
            "right": (0.8, 0.4)   
        }
        x, y = positions.get(pos_name, (0.5, 0.4)) # 这里默认值也改一下
        renpy.show_screen("heart_explosion", x=x, y=y, duration=duration, particle_count=count)