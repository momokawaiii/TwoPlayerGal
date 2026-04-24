init:
    image fav_up_img = "faup.png"
    image fav_down_img = "fadown.png"

    transform fav_float_anim:
        zoom 0.3
        align (1.0, 0.5) xoffset 100 alpha 0.0
        
        parallel:
            easein 0.3 xoffset -80
        parallel:
            easein 0.3 alpha 1.0
            
        pause 0.8
        
        parallel:
            easeout 0.5 yoffset -100
        parallel:
            easeout 0.5 alpha 0.0

    screen fav_notify_screen(img_target):
        zorder 100      
        add img_target at fav_float_anim
        timer 1.6 action Hide("fav_notify_screen")

init python:
    def show_up():
        renpy.hide_screen("fav_notify_screen")
        renpy.show_screen("fav_notify_screen", img_target="fav_up_img")
        renpy.restart_interaction()

    def show_down():
        renpy.hide_screen("fav_notify_screen")
        renpy.show_screen("fav_notify_screen", img_target="fav_down_img")
        renpy.restart_interaction()

    import socket
    import threading
    import json
    import time
    
    server_socket = None
    client_connection = None
    network_running_flag = False 
    network_status = "未连接"
    
    ROLE_NONE = 0
    ROLE_KING = 1
    ROLE_HERO = 2
    
    ACTION_CLAIM_KING = 101
    ACTION_CLAIM_HERO = 102

    stat_translation_map = { "H": "圣人点数", "E": "撒旦点数", "S": "守序", "C": "混沌", "L": "孤独感", "F": "满足感" }


    def send_sync_action(action_code):
        global client_connection
        if client_connection:
            try:
                data = json.dumps({"type": "sync", "action": action_code}) + "\n"
                client_connection.sendall(data.encode('utf-8'))
            except: pass

    def send_async_action(action_code):
        global client_connection
        if client_connection:
            try:
                action_data = { "type": "async", "action": action_code, "plane": renpy.store.my_plane }
                json_string = json.dumps(action_data) + "\n"
                client_connection.sendall(json_string.encode('utf-8'))
            except: pass

    def connection_loop(conn):
        global network_running_flag, network_status
        buffer = ""
        conn.settimeout(0.5)
        
        while network_running_flag:
            try:
                data = conn.recv(4096)
                if not data: break 
                buffer += data.decode('utf-8')
                while '\n' in buffer:
                    message, buffer = buffer.split('\n', 1)
                    handle_received_data(message)
            except socket.timeout:
                continue 
            except:
                break

    def handle_received_data(data_string):
        try:
            received_data = json.loads(data_string)
            msg_type = received_data.get("type")
            renpy.store.event_queue.append(received_data)
            
            if msg_type == "async":
                renpy.store.opponent_plane = received_data.get("plane")
            elif msg_type == "sync":
                renpy.store.opponent_action = received_data.get("action")
                renpy.store.opponent_has_chosen = True
            
            renpy.restart_interaction()
        except: pass

    def wait_for_opponent_choice_1():
        if not renpy.store.opponent_has_chosen:
            renpy.show_screen("waiting_screen", message="等待对方做出选择...")

    def server_thread_func():
        global server_socket, client_connection, network_running_flag, network_status
        host = "0.0.0.0"; port = 11451
        
        while network_running_flag:
            try:
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_socket.bind((host, port))
                server_socket.listen(1)
                server_socket.settimeout(1.0)
            except OSError:
                renpy.store.network_status = "端口被占用，1秒后重试..."
                renpy.restart_interaction()
                time.sleep(0.1)
                continue

            renpy.store.network_status = "主机等待连接..."
            renpy.restart_interaction()
            
            try:
                while network_running_flag:
                    try:
                        conn, addr = server_socket.accept()
                        client_connection = conn
                        renpy.store.network_status = f"已连接: {addr}"
                        renpy.restart_interaction()
                        
                        connection_loop(client_connection)
                        
                        client_connection = None
                        renpy.store.network_status = "连接断开，重新监听..."
                        renpy.restart_interaction()
                        
                    except socket.timeout:
                        continue
                    except Exception as e:
                        break 
            finally:
                try: server_socket.close()
                except: pass

    def client_thread_func(target_ip, port):
        global client_connection, network_running_flag, network_status

        while network_running_flag:
            try:
                renpy.store.network_status = f"正在连接 {target_ip}..."
                renpy.restart_interaction()
                
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.settimeout(5.0)
                conn.connect((target_ip, port))
                
                client_connection = conn
                renpy.store.network_status = "已连接主机"
                renpy.restart_interaction()
                
                connection_loop(client_connection)
                
                client_connection = None
                renpy.store.network_status = "连接断开，准备重连..."
                
            except Exception as e:
                renpy.store.network_status = "连接失败，1秒后重试..."
                renpy.restart_interaction()
                time.sleep(1.0)
            finally:
                try: conn.close()
                except: pass

    def reset_and_start_network(is_host_mode, ip="127.0.0.1"):
        global network_running_flag, server_socket, client_connection
        
        network_running_flag = False
        try:
            if client_connection: 
                client_connection.shutdown(socket.SHUT_RDWR)
                client_connection.close()
            if server_socket: 
                server_socket.close()
        except: pass
        
        time.sleep(0.1)
        
        network_running_flag = True
        renpy.store.event_queue = [] 
        
        if is_host_mode:
            t = threading.Thread(target=server_thread_func, daemon=True)
            t.start()
        else:
            t = threading.Thread(target=client_thread_func, args=(ip, 11451), daemon=True)
            t.start()

    def notify_stat_change(message, changes):
        change_parts = []
        for var_name, value in changes.items():
            label = stat_translation_map.get(var_name, var_name)
            sign = "+" if value >= 0 else ""
            part = "你的'{}' {}{}".format(label, sign, value)
            change_parts.append(part)
        renpy.notify(message + "，" + "，".join(change_parts))
        
    def make_sync_choice(action_code):
        renpy.store.my_action = action_code
        send_sync_action(action_code)
        renpy.store.i_have_chosen = True

    def wait_for_opponent_choice():
        if not renpy.store.opponent_has_chosen:
            renpy.show_screen("waiting_screen", message="等待对方做出选择...")
            renpy.pause(0.1)
            while not renpy.store.opponent_has_chosen:
                process_all_async_events()
                renpy.pause(0.2)
            renpy.hide_screen("waiting_screen")
        renpy.store.i_have_chosen = False
        renpy.store.opponent_has_chosen = False

    def player_select_role(role):
        renpy.store.my_role = role
        if role == ROLE_KING:
            send_async_action(ACTION_CLAIM_KING)
        elif role == ROLE_HERO:
            send_async_action(ACTION_CLAIM_HERO)

    def role_selection_periodic_check():
        events_to_process = list(renpy.store.event_queue)
        for event in events_to_process:
            action = event.get("action")
            if action == ACTION_CLAIM_KING:
                if renpy.store.my_role == ROLE_KING:
                    if not renpy.store.session_store.get("is_host"):
                        renpy.store.my_role = ROLE_HERO
                        renpy.store.event_queue.remove(event)
                        return "force_hero"
                elif renpy.store.my_role == ROLE_NONE:
                    renpy.store.my_role = ROLE_HERO
                    renpy.store.event_queue.remove(event)
                    return "force_hero"
            elif action == ACTION_CLAIM_HERO:
                if renpy.store.my_role == ROLE_HERO:
                    if not renpy.store.session_store.get("is_host"):
                        renpy.store.my_role = ROLE_KING
                        renpy.store.event_queue.remove(event)
                        return "force_king"
                elif renpy.store.my_role == ROLE_NONE:
                    renpy.store.my_role = ROLE_KING
                    renpy.store.event_queue.remove(event)
                    return "force_king"
        return None

    def process_all_async_events():
            for event in renpy.store.event_queue:
                if event.get("action") == 999:
                    renpy.hide_screen("waiting_screen")
                    renpy.store.event_queue = [] 
                    renpy.jump("stone_water")
                    return
                if event.get("action") == 888:
                    renpy.hide_screen("waiting_screen")
                    renpy.store.event_queue = []
                    renpy.jump("be2_mars_heart")
                    return

            queue_copy = list(renpy.store.event_queue)
            for event in queue_copy:
                act = event.get("action")
                handled = False
                
                if act == 901:
                    renpy.store.opponent_plane = event.get("plane")
                    handled = True

                elif act in [201, 221, 304, 302]:
                    renpy.store.H += 2
                    notify_stat_change("受到对方选择的干扰", {"H": 2})
                    handled = True
                
                elif act in [202, 222, 303]:
                    renpy.store.E += 2
                    notify_stat_change("受到对方选择的干扰", {"E": 2})
                    handled = True
                
                elif act in [233, 3411]:
                    renpy.store.E -= 1
                    notify_stat_change("受到对方选择的干扰", {"E": -1})
                    handled = True
                
                elif act in [234, 3421]:
                    renpy.store.E += 1
                    notify_stat_change("受到对方选择的干扰", {"E": 1})
                    handled = True
                
                elif act == 3412:
                    renpy.store.C += 1
                    renpy.store.E += 1
                    notify_stat_change("受到对方选择的干扰", {"C": 1,"E": 1})
                    handled = True

                elif act == 2141:
                    renpy.store.H += 1
                    renpy.store.S += 1
                    notify_stat_change("受到对方选择的干扰", {"H": 1,"S":1})
                    handled = True

                elif act == 332:
                    renpy.store.F += 1
                    notify_stat_change("受到对方选择的干扰", {"F": 1})
                    handled = True

                elif act in [232, 331]:
                    renpy.store.S += 1
                    notify_stat_change("受到对方选择的干扰", {"S": 1})
                    handled = True

                elif act in [213, 231]:
                    renpy.store.H += 1
                    renpy.store.E += 1
                    notify_stat_change("受到对方选择的干扰", {"H": 1,"E":1})
                    handled = True

                elif act == 211:
                    renpy.store.H += 1
                    renpy.store.S += 1
                    notify_stat_change("受到对方选择的干扰", {"H": 1,"S":1})
                    handled = True

                elif act in [212, 2142]:
                    renpy.store.H += 1
                    renpy.store.F += 1
                    notify_stat_change("受到对方选择的干扰", {"H": 1,"F":1})
                    handled = True

                elif act == 333:
                    renpy.store.C += 1
                    renpy.store.E += 1
                    notify_stat_change("受到对方选择的干扰", {"C": 1,"E":1})
                    handled = True

                if handled and event in renpy.store.event_queue:
                    renpy.store.event_queue.remove(event)

    def global_event_handler():
        process_all_async_events()
    renpy.persistent.before_interaction = global_event_handler

    class DynamicRadarChart(renpy.Displayable):
        def __init__(self, stats_map, levels=1, max_value=10, size=300, colors=None, **kwargs):
            super(DynamicRadarChart, self).__init__(**kwargs)
            
            self.stats_map = stats_map
            self.points = len(stats_map)
            self.texts = list(stats_map.keys())
            
            self.levels = levels
            self.max_value = max_value
            self.size = size
            self.colors = colors or ["#f51a1a00", "#6085ffd0", "#ffffff"]
            
        def render(self, width, height, st, at):
            self.nums = [getattr(store, var_name) for var_name in self.stats_map.values()]

            render = renpy.Render(self.size, self.size)
            canvas = render.canvas()
            
            center = (self.size // 2, self.size // 2)
            
            radius = self.size // 2 - 40
            points = []
            for i in range(self.points):
                angle = 2 * math.pi * i / self.points - math.pi / 2
                x = center[0] + radius * math.cos(angle)
                y = center[1] + radius * math.sin(angle)
                points.append((x, y))
            canvas.polygon(self.colors[0], points)

            for point in points:
                canvas.line(self.colors[1], center, point, width=2)
            
            for n in range(1, self.levels + 1):
                scale = n / self.levels
                grid_points = []
                for i in range(self.points):
                    angle = 2 * math.pi * i / self.points - math.pi / 2
                    x = center[0] + (radius * scale) * math.cos(angle)
                    y = center[1] + (radius * scale) * math.sin(angle)
                    grid_points.append((x, y))
                canvas.polygon(self.colors[1], grid_points, width=2)
            
            data_points = []
            for i, value in enumerate(self.nums):
                clamped_value = max(0, min(value, self.max_value))
                scaled_radius = radius * (clamped_value / self.max_value)
                angle = 2 * math.pi * i / len(self.nums) - math.pi / 2
                x = center[0] + scaled_radius * math.cos(angle)
                y = center[1] + scaled_radius * math.sin(angle)
                data_points.append((x, y))
            canvas.polygon(self.colors[1], data_points)
            canvas.polygon(self.colors[1], data_points, width=2)

            group_radius = radius + self.size * 0.05
            for i, (label, value) in enumerate(zip(self.texts, self.nums)):
                angle = 2 * math.pi * i / len(self.texts) - math.pi / 2
                x = center[0] + group_radius * math.cos(angle)
                y = center[1] + group_radius * math.sin(angle)
                
                label_text = Text(label, color=self.colors[2], size=int(self.size*0.05))
                value_text = Text(str(value), color=self.colors[2], size=int(self.size*0.05))
                
                label_render = renpy.render(label_text, width, height, st, at)
                value_render = renpy.render(value_text, width, height, st, at)
                label_width, label_height = label_render.get_size()
                value_width, value_height = value_render.get_size()
                
                group_width = max(label_width, value_width)
                group_height = label_height + value_height
                
                text_group = VBox(label_text, value_text, xalign=0.5)
                
                render.blit(
                    renpy.render(text_group, width, height, st, at),
                    (x - group_width / 2, y - group_height / 2)
                )
            
            return render
define player_stats_map = {"善": "H","恶": "E","谐": "S", "虚": "C", "全": "F","孤": "L"}
screen radar_screen():
    zorder 100
    vbox:
        xalign 1.0
        yalign 0.0
        xoffset -20
        yoffset 20
        spacing 10
        add DynamicRadarChart(
            stats_map=player_stats_map,
            levels=5,
            max_value=20,
            size=300
        )
        hbox:
            align(0.5, 0.5)
            spacing 10
            text "好感度":
                size 22
                color "#dddddd"
                yalign 0.5
            bar:
                value favorability
                range 100
                xsize 200
                ysize 25
                left_bar Solid("#f942db")
                right_bar Solid("#342626")

init python:
 
    STARNEST_FUNCTIONS = """
        vec2 MatMultiplayVec(vec4 m, vec2 v) { return vec2(m.x * v.x + m.z * v.y, m.y * v.x + m.w * v.y); }
        float SCurve (float value) {
            if(value < 0.5) { return value * value * value * value * value * 16.0; }
            value -= 1.0;
            return value * value * value * value * value * 16.0 + 1.0;
        }
    """
     
    STARNEST_MAIN = """
        #define iterations 17
        #define formuparam 0.53
        #define volsteps 20
        #define stepsize 0.1
        #define zoom   0.800
        #define tile   0.850
        #define speed  0.002
        #define brightness 0.002
        #define darkmatter 0.300
        #define distfading 0.750
        #define saturation 0.750
 
        vec2 uv=v_tex_coord-.5;
        uv.y*=u_model_size.y/u_model_size.x;
        vec3 dir=vec3(uv*zoom,1.);
        float time=u_time*speed+.25;
        vec3 from=vec3(1.,.5,0.5);
        from+=vec3(time*2.,time,-2.);
 
        float s=0.1,fade=1.;
        vec3 v=vec3(0.);
        for (int r=0; r<volsteps; r++) {
            vec3 p=from+s*dir*.5;
            p = abs(vec3(tile)-mod(p,vec3(tile*2.)));
            float pa,a=pa=0.;
            for (int i=0; i<iterations; i++) {
                p=abs(p)/dot(p,p)-formuparam;
                a+=abs(length(p)-pa);
                pa=length(p);
            }
            float dm=max(0.,darkmatter-a*a*.001);
            a = pow(a, 2.5);
            if (r>6) fade*=1.-dm;
            v+=fade;
            v+=vec3(s,s*s,s*s*s*s)*a*brightness*fade;
            fade*=distfading;
            s+=stepsize;
        }
        v=mix(vec3(length(v)),v,saturation);
        vec4 C = vec4(v*.01,1.);
        C.r = pow(C.r, 0.35); C.g = pow(C.g, 0.36); C.b = pow(C.b, 0.4);
        vec4 L = C;
        C.r = mix(L.r, SCurve(C.r), 1.0); C.g = mix(L.g, SCurve(C.g), 0.9); C.b = mix(L.b, SCurve(C.b), 0.6);
        gl_FragColor = C;
    """

    renpy.register_shader("shadertoy.StarNest", variables="""
        uniform float u_time;
        uniform vec2 u_model_size;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """,
    fragment_functions=STARNEST_FUNCTIONS,
    vertex_300="""
        v_tex_coord = vec2(a_tex_coord.s, 1.0 - a_tex_coord.t);
    """,
    fragment_300=STARNEST_MAIN)

init python:

    FRACTAL_FUNCTIONS = """
        vec3 hsv(float h, float s, float v) {
            vec4 K = vec4(1.0, 2.0/3.0, 1.0/3.0, 3.0);
            vec3 p = abs(fract(vec3(h) + K.xyz) * 6.0 - K.www);
            return v * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), s);
        }
    """
     
    FRACTAL_MAIN = """
        float i;
        float e = 1.0;
        float R = 0.0;
        float s = 1.0;
        vec3 q = vec3(0.0);
        vec3 p;
        vec3 d;
        vec3 o = vec3(0.0);
        
        vec2 uv = (gl_FragCoord.xy - 0.5 * u_model_size.xy) / u_model_size.y;
        d = vec3(uv.x, uv.y, 1.0);
        q.y -= 1.0;
        q.z -= 1.0;
        
        float start_time = 4.8;
        float t = start_time + u_time;
        
        for (i = 0.0; i < 129.0; i++) {
            o.rgb += hsv(0.7 + (-R / (i + 2.0)) * 0.1, 0.15, min(R * e * s - 0.07, e) / 8.0);
            
            s = 1.0;
            p = q += d * e * R * 0.24;
            
            p = vec3(
                log2(R = length(p)) - t * 0.5,
                exp(-p.z / R),
                atan(p.y, p.x)
            );
            
            e = --p.y;
            for (s = 1.0; s < 500.0; s += s) {
                e += dot(
                    sin(p.yzx * s - t),
                    0.2 - cos(p.yxy * s)
                ) / s * 0.2;
            }
        }
        
        float transition_duration = 1.5;
        
        float progress = clamp(u_time / transition_duration, 0.0, 1.0);
        
        //    progress = 0.0时, curtain_y = 0.5  (在屏幕顶部)
        //    progress = 1.0时, curtain_y = -0.5 (在屏幕底部)
        float curtain_y = 0.5 - progress * 1.0;
        
        if (uv.y < curtain_y) {
            o = vec3(0.0, 0.0, 0.0);
        }
        gl_FragColor = vec4(o, 1.0);
    """
    

    renpy.register_shader("mygame.fractal", variables="""
        uniform float u_time;
        uniform vec2 u_model_size;
    """,
    fragment_functions=FRACTAL_FUNCTIONS,
    fragment_300=FRACTAL_MAIN)

init -1 python:
 
    class ShaderToy(renpy.Displayable):
        def __init__(self, child, shader_name, **kwargs):
            super(ShaderToy, self).__init__(**kwargs)
            self.child = renpy.displayable(child)
            self.shader_name = shader_name
            self.width = config.screen_width
            self.height = config.screen_height
 
        def render(self, width, height, st, at):
            render = renpy.Render(self.width, self.height)
            render.place(self.child)
            render.add_shader(self.shader_name)
            render.add_uniform("u_time", st)
            render.add_uniform("u_model_size", (self.width, self.height))
            renpy.redraw(self, 0)
            return render

image plgrd = "images/plgrd.png"

image starnest_effect = ShaderToy("plgrd", "shadertoy.StarNest")

init -1 python:
 
    class FractalDisplayable(renpy.Displayable):
        def __init__(self,child, shader_name, **kwargs):
            super(FractalDisplayable, self).__init__(**kwargs)
            self.child = renpy.displayable(child)
            self.shader_name = shader_name
            self.width = config.screen_width
            self.height = config.screen_height
 
        def render(self, width, height, st, at):
            render = renpy.Render(self.width, self.height)
            render.place(self.child)
            render.add_shader(self.shader_name)
            render.add_uniform("u_time", st)
            render.add_uniform("u_model_size", (self.width, self.height))
            renpy.redraw(self, 0)
            return render

image fractal_background = FractalDisplayable("plgrd", "mygame.fractal")

init python:

    CELLS_FUNCTIONS = """
        float rand21(vec2 p) {
            return fract(sin(dot(p, vec2(12.456, 56.789))) * 798484.123);
        }

        vec2 rand22(vec2 p) {
            float r1 = rand21(p);
            return vec2(r1, rand21(r1 * p));
        }

        vec2 getPoint(vec2 id, float time) {
            vec2 r = rand22(id);
            float t = time * 2.; 

            vec2 speed = rand22(id + rand22(id));

            float x = cos(t * speed.x * (r.x + 1.)) * .4 + .5;
            float y = sin(t * speed.y * (r.y + 1.)) * .4 + .5;

            return vec2(x, y);
        }
    """

    CELLS_MAIN = """
        const float ZOOM = 10.0;
        vec3 col = vec3(0.0);

        vec2 uv = v_tex_coord;
        
        uv.x *= u_model_size.x / u_model_size.y;
        
        uv *= ZOOM;
        uv.y += u_time;

        vec2 id = floor(uv);
        vec2 gv = fract(uv);

        float presence = 0.0;
        
        for (int x = -1; x < 2; x++) {
            for (int y = -1; y < 2; y++) {
                vec2 offset = vec2(float(x), float(y));

                vec2 nid = id + offset;
                vec2 np = getPoint(nid, u_time);

                float size = rand21(nid) * 0.2;

                float x2 = distance(offset + np, gv);
                
                float y2 = max(size / x2 - size, 0.0);
                presence += y2;
            }
        }

        vec3 base_color = sin(vec3(2., 3., 5.) * u_time * .5) * .2 + .4;
        col = base_color * presence;
        
        gl_FragColor = vec4(col, 1.0);
    """

    renpy.register_shader("shadertoy.Cells", variables="""
        uniform float u_time;
        uniform vec2 u_model_size;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """,
    fragment_functions=CELLS_FUNCTIONS,
    vertex_300="""
        v_tex_coord = vec2(a_tex_coord.s, 1.0 - a_tex_coord.t);
    """,
    fragment_300=CELLS_MAIN)

init -1 python:
 
    class ShaderToy(renpy.Displayable):
        def __init__(self, child, shader_name, **kwargs):
            super(ShaderToy, self).__init__(**kwargs)
            self.child = renpy.displayable(child)
            self.shader_name = shader_name
            self.width = config.screen_width
            self.height = config.screen_height
 
        def render(self, width, height, st, at):
            render = renpy.Render(self.width, self.height)
            render.place(self.child)
            render.add_shader(self.shader_name)
            render.add_uniform("u_time", st)
            render.add_uniform("u_model_size", (self.width, self.height))
            renpy.redraw(self, 0)
            return render
image plgrd = "images/plgrd.png"
image cells_bg = ShaderToy("plgrd", "shadertoy.Cells")
init python:

    # 定义 Shader 逻辑
    NEON_WAVE_CODE = """
        vec2 fragCoord = v_tex_coord * u_model_size;
        vec2 uv = (2.0 * fragCoord - u_model_size) / min(u_model_size.x, u_model_size.y);

        for(float i = 1.0; i < 10.0; i++){
            uv.x += 0.6 / i * cos(i * 2.5 * uv.y + u_time);
            uv.y += 0.6 / i * cos(i * 1.5 * uv.x + u_time);
        }
        
        vec3 col = vec3(0.1) / abs(sin(u_time - uv.y - uv.x));
        
        gl_FragColor = vec4(col, 1.0);
    """

    renpy.register_shader("shadertoy.NeonWave", variables="""
        uniform float u_time;
        uniform vec2 u_model_size;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """,
    vertex_300="""
        v_tex_coord = a_tex_coord;
    """,
    fragment_300=NEON_WAVE_CODE)

image neon_wave_effect = ShaderToy("plgrd", "shadertoy.NeonWave")

init python:

    UNIVERSE_FUNCTIONS = """
        #define S(a, b, t) smoothstep(a, b, t)
        #define NUM_LAYERS 4.0
        
        float N21(vec2 p) {
            vec3 a = fract(vec3(p.xyx) * vec3(213.897, 653.453, 253.098));
            a += dot(a, a.yzx + 79.76);
            return fract((a.x + a.y) * a.z);
        }

        vec2 GetPos(vec2 id, vec2 offs, float t) {
            float n = N21(id + offs);
            float n1 = fract(n * 10.0);
            float n2 = fract(n * 100.0);
            float a = t + n;
            return offs + vec2(sin(a * n1), cos(a * n2)) * 0.4;
        }

        float df_line(in vec2 a, in vec2 b, in vec2 p) {
            vec2 pa = p - a, ba = b - a;
            float h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0);
            return length(pa - ba * h);
        }

        float line(vec2 a, vec2 b, vec2 uv) {
            float r1 = 0.04;
            float r2 = 0.01;
            
            float d = df_line(a, b, uv);
            float d2 = length(a - b);
            float fade = S(1.5 * 4.0, 0.0, d2);
            
            fade += S(0.05, 0.02, abs(d2 - 0.75));
            return S(r1, r2, d) * fade;
        }

        float NetLayer(vec2 st, float n, float t) {
            vec2 id = floor(st) + n;
            st = fract(st) - 0.5;
        
            vec2 p[9];
            int i = 0;
            for(float y = -1.0; y <= 1.0; y++) {
                for(float x = -1.0; x <= 1.0; x++) {
                    p[i] = GetPos(id, vec2(x, y), t);
                    i++;
                }
            }
            
            float m = 0.0;
            float sparkle = 0.0;
            
            for(int i = 0; i < 9; i++) {
                m += line(p[4], p[i], st);

                float d = length(st - p[i]);
                float s = (0.005 / (d * d));
                s *= S(1.0, 0.7, d);
                float pulse = sin((fract(p[i].x) + fract(p[i].y) + t) * 5.0) * 0.4 + 0.6;
                pulse = pow(pulse, 20.0);

                s *= pulse;
                sparkle += s;
            }
            
            m += line(p[1], p[3], st);
            m += line(p[1], p[5], st);
            m += line(p[7], p[5], st);
            m += line(p[7], p[3], st);
            
            float sPhase = (sin(t + n) + sin(t * 0.1)) * 0.25 + 0.5;
            sPhase += pow(sin(t * 0.1) * 0.5 + 0.5, 50.0) * 5.0;
            m += sparkle * sPhase;
            
            return m;
        }
    """

    UNIVERSE_MAIN_FAST = """
        vec2 uv = v_tex_coord - 0.5;
        uv.y *= u_model_size.y / u_model_size.x;
        
        vec2 M = vec2(0.0); 
        
        float t = u_time * 0.25;
        
        float rotate_t = 8.0 * sin(t * 0.4);
        float s = sin(rotate_t);
        float c = cos(rotate_t);
        mat2 rot = mat2(c, -s, s, c);
        
        vec2 st = uv * rot;  
        M *= rot * 2.0;
        
        float m = 0.0;
        for(float i = 0.0; i < 1.0; i += 1.0 / NUM_LAYERS) {
            float z = fract(t + i);
            float size = mix(15.0, 1.0, z);
            float fade = S(0.0, 0.6, z) * S(1.0, 0.8, z);
            m += fade * NetLayer(st * size - M * z, i, u_time*0.5);
        }
        
        float fake_fft = sin(u_time * 2.5) * 0.1 + 0.5;
        float glow = -uv.y * fake_fft * 2.0;
    
        vec3 baseCol = vec3(s, cos(rotate_t * 0.2), sin(rotate_t * 0.5));
        baseCol = abs(baseCol); 
        baseCol = mix(baseCol, vec3(0.2, 0.5, 1.0), 0.4);

        vec3 col = baseCol * m;
        col += baseCol * glow;
        col *= 1.0 - dot(uv, uv);
        
        gl_FragColor = vec4(col, 1.0);
    """

    renpy.register_shader("shadertoy.UniverseWithinFast", variables="""
        uniform float u_time;
        uniform vec2 u_model_size;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """,
    vertex_300="""
        v_tex_coord = a_tex_coord;
    """,
    fragment_functions=UNIVERSE_FUNCTIONS,
    fragment_300=UNIVERSE_MAIN_FAST)

image UniverseWithin = ShaderToy("plgrd", "shadertoy.UniverseWithinFast")

init python:

    RIPPLE_FUNCTIONS = """
        #define MAX_RADIUS 2
        #define DOUBLE_HASH 0
        #define HASHSCALE1 0.1031
        #define HASHSCALE3 vec3(0.1031, 0.1030, 0.0973)

        float hash12(vec2 p)
        {
            vec3 p3  = fract(vec3(p.xyx) * HASHSCALE1);
            p3 += dot(p3, p3.yzx + 19.19);
            return fract((p3.x + p3.y) * p3.z);
        }

        vec2 hash22(vec2 p)
        {
            vec3 p3 = fract(vec3(p.xyx) * HASHSCALE3);
            p3 += dot(p3, p3.yzx+19.19);
            return fract((p3.xx+p3.yz)*p3.zy);
        }
    """

    RIPPLE_MAIN = """
        float resolution = 5.0; 
        uv_screen.x *= u_model_size.x / u_model_size.y;
        
        vec2 uv = uv_screen * resolution;
        vec2 p0 = floor(uv);

        vec2 circles = vec2(0.0);
        
        for (int j = -MAX_RADIUS; j <= MAX_RADIUS; ++j)
        {
            for (int i = -MAX_RADIUS; i <= MAX_RADIUS; ++i)
            {
                vec2 pi = p0 + vec2(float(i), float(j));
                
                #if DOUBLE_HASH
                vec2 hsh = hash22(pi);
                #else
                vec2 hsh = pi;
                #endif
                
                vec2 p = pi + hash22(hsh);

                float t = fract(0.3 * u_time + hash12(hsh));
                vec2 v = p - uv;
                float d = length(v) - (float(MAX_RADIUS) + 1.0) * t;

                float h = 1e-3;
                float d1 = d - h;
                float d2 = d + h;
                
                float p1 = sin(31.0 * d1) * smoothstep(-0.6, -0.3, d1) * smoothstep(0.0, -0.3, d1);
                float p2 = sin(31.0 * d2) * smoothstep(-0.6, -0.3, d2) * smoothstep(0.0, -0.3, d2);
                
                circles += 0.5 * normalize(v) * ((p2 - p1) / (2.0 * h) * (1.0 - t) * (1.0 - t));
            }
        }
        
        circles /= float((MAX_RADIUS * 2 + 1) * (MAX_RADIUS * 2 + 1));

        float intensity = mix(0.01, 0.15, smoothstep(0.1, 0.6, abs(fract(0.05 * u_time + 0.5) * 2.0 - 1.0)));
        vec3 n = vec3(circles, sqrt(max(0.0, 1.0 - dot(circles, circles))));
        
        vec2 distorted_uv = v_tex_coord - intensity * n.xy;
        
        vec3 color = texture2D(tex0, distorted_uv).rgb;
        
        color += 5.0 * pow(clamp(dot(n, normalize(vec3(1.0, 0.7, 0.5))), 0.0, 1.0), 6.0);
        
        gl_FragColor = vec4(color, 1.0);
    """

    renpy.register_shader("shadertoy.RainRipples", variables="""
        uniform float u_time;
        uniform vec2 u_model_size;
        uniform sampler2D tex0;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """,
    vertex_300="""
        v_tex_coord = a_tex_coord;
    """,
    fragment_functions=RIPPLE_FUNCTIONS,
    fragment_300=RIPPLE_MAIN)

image bg_rain_effect = ShaderToy("empstreet", "shadertoy.RainRipples")
image mirror_rain_effect = ShaderToy("linkroad", "shadertoy.RippleSpread")

init python:
    CYBER_TUNNEL_FIXED_FUNCTIONS = """
        vec3 tanh_approx(vec3 x) {
            vec3 e2x = exp(2.0 * x);
            return (e2x - 1.0) / (e2x + 1.0);
        }
    """

    CYBER_TUNNEL_FIXED_MAIN = """
        
        vec2 fragCoord = v_tex_coord * u_model_size;
        vec2 iResolution = u_model_size;
        
        vec2 uv = (fragCoord - iResolution.xy * 0.5) / iResolution.y;
        
        uv.y = -uv.y;

        float d = 0.0;      // 累积距离
        float s = 0.0;      // 单步 SDF 距离
        vec3 c = vec3(0.0); // 颜色
        vec3 p = vec3(0.0); // 3D 坐标点
        
        float t = u_time;   // 时间

        for(int i = 0; i < 64; i++) {
            
            // 原理：p = uv * d (射线投射)
            // p.z = d + t*4. (向前移动)
            p = vec3(uv * d, d + t * 4.0);
            
            float s_noise = 0.1;
            
            for(int k = 0; k < 5; k++) {
                if(s_noise >= 3.0) break;
                
                p.y += abs(dot(sin(0.2 * p / s_noise), vec3(1.0))) * s_noise;
                
                // 对应: s+=s
                s_noise += s_noise; 
            }
            
            
            float d_floor = 1.0 + p.y;
            float d_ceil = 1.5 - p.y * 0.1;
            
            float bat_shape = step(
                0.005 - abs(uv.x) * 0.4,
                abs(0.1 * sin(t * 0.3) + uv.y - 0.1 + 0.7 * abs(uv.x) * sin(t * 24.0))
            );
            
            s = min(d_floor, min(d_ceil, bat_shape));
            
            d += s;
            
            
            c += s * d + 0.1 * vec3(2.0, 3.0, 4.0) / length(uv - 0.25);
        }
        
        vec3 final_color = (c / 1000.0) * exp(-d / 50.0);
        
        gl_FragColor = vec4(tanh_approx(final_color), 1.0);
    """
    renpy.register_shader("shadertoy.CyberTunnelFixed", variables="""
        uniform float u_time;
        uniform vec2 u_model_size;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """,
    vertex_300="""
        v_tex_coord = a_tex_coord;
    """,
    fragment_functions=CYBER_TUNNEL_FIXED_FUNCTIONS,
    fragment_300=CYBER_TUNNEL_FIXED_MAIN)
init python:
    SCI_FI_TUNNEL_FUNCTIONS = """
        vec3 tanh_approx(vec3 x) {
            vec3 e2x = exp(2.0 * x);
            return (e2x - 1.0) / (e2x + 1.0);
        }
    """

    SCI_FI_TUNNEL_MAIN = """
        // --- 坐标系准备 ---
        vec2 fragCoord = v_tex_coord * u_model_size;
        vec2 iResolution = u_model_size;
        
        vec2 uv = (fragCoord * 2.0 - iResolution.xy) / iResolution.y;
        
        uv.y = -uv.y;
        
        float time_scaled = 0.2 * u_time;
        uv += cos(time_scaled * vec2(0.4, 0.8)) * vec2(0.3, 0.1);
        
        float d = 0.4 + 0.1 * dot(fract(sin(fragCoord)), sin(fragCoord));
        vec3 o = vec3(0.0); 

        vec2 v_glow_pos = (0.2 + 0.2 * sin(time_scaled * 6.0)) + uv + (vec2(uv.y, uv.x) * 0.8 + 0.2 - vec2(-1.0, 0.1));

        for(int i = 0; i < 50; i++) {
            if(d >= 100.0) break;
            
            vec3 p = vec3(uv * d, d + time_scaled * 10.0);
            
            vec4 angle_vec = 0.02 * p.zzzz + 0.4 * time_scaled + vec4(0.0, 33.0, 11.0, 0.0);
            vec4 cos_vals = cos(angle_vec);
            mat2 rot_mat = mat2(cos_vals.x, cos_vals.y, cos_vals.z, cos_vals.w);
            p.xy *= rot_mat;
            
            float a = 0.01;
            for(int k = 0; k < 5; k++) {
                if(a >= 0.5) break;
                
                vec3 fold_input = time_scaled + 0.3 * p / a;
                p -= dot(ceil(cos(fold_input)), vec3(4.0)) * a;
                
                p += ceil(sin(p.yzx * 0.3) * 3.0);
                
                a += a;
            }
            
            float s = sin(p.z) * 5.0 + 16.0 - abs(p.y);
            
            o += 0.2 * vec3(6.0, 3.0, 12.0) / length(v_glow_pos);
            
            vec3 wall_color = 1.0 + cos(0.5 * p.z + vec3(4.0, 2.0, 1.0));
            o += wall_color / (10.0 * abs(s));
            
            d += 0.01 + 0.1 * abs(s);
        }

        o = tanh_approx(o * o / 10000.0);
        
        gl_FragColor = vec4(o, 1.0);
    """

    renpy.register_shader("shadertoy.SciFiTunnel", variables="""
        uniform float u_time;
        uniform vec2 u_model_size;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """,
    vertex_300="""
        v_tex_coord = a_tex_coord;
    """,
    fragment_functions=SCI_FI_TUNNEL_FUNCTIONS,
    fragment_300=SCI_FI_TUNNEL_MAIN)

init python:

    TOTEM_FUNCTIONS = """
        float g_time;

        struct Hit {
            float d;
            int id;
            vec3 uv;
        };

        float n31(vec3 p) {
            const vec3 s = vec3(7.0, 157.0, 113.0);
            vec3 ip = floor(p);
            p = fract(p);
            p = p * p * (3.0 - 2.0 * p);
            vec4 h = vec4(0.0, s.yz, s.y + s.z) + dot(ip, s);
            h = mix(fract(sin(h) * 43.5453), fract(sin(h + s.x) * 43.5453), p.x);
            h.xy = mix(h.xz, h.yw, p.y);
            return mix(h.x, h.y, p.z);
        }

        float n21(vec2 p) {
            const vec3 s = vec3(7.0, 157.0, 0.0);
            vec2 ip = floor(p);
            p = fract(p);
            p = p * p * (3.0 - 2.0 * p);
            vec2 h = s.zy + dot(ip, s.xy);
            h = mix(fract(sin(h) * 43.5453), fract(sin(h + s.x) * 43.5453), p.x);
            return mix(h.x, h.y, p.y);
        }

        float n11(float p) {
            float ip = floor(p);
            p = fract(p);
            vec2 h = fract(sin(vec2(ip, ip + 1.0) * 12.3456) * 43.5453);
            return mix(h.x, h.y, p * p * (3.0 - 2.0 * p));
        }

        float smin(float a, float b, float k) {
            float h = clamp(0.5 + 0.5 * (b - a) / k, 0.0, 1.0);
            return mix(b, a, h) - k * h * (1.0 - h);
        }

        Hit minH(Hit a, Hit b) {
            if (a.d < b.d) return a;
            return b;
        }

        mat2 rot(float a) {
            float c = cos(a);
            float s = sin(a);
            return mat2(c, s, -s, c);
        }

        float sdCyl(vec3 p, vec2 hr) {
            vec2 d = abs(vec2(length(p.xz), p.y)) - hr;
            return min(max(d.x, d.y), 0.0) + length(max(d, 0.0));
        }

        float sdCapsule(vec3 p, float h, float r) {
            p.y -= clamp(p.y, 0.0, h);
            return length(p) - r;
        }

        vec3 getRayDir(vec3 ro, vec2 uv) {
            vec3 f = normalize(-ro);
            vec3 r = normalize(cross(vec3(0.0, 1.0, 0.0), f));
            return normalize(f + r * uv.x + cross(f, r) * uv.y);
        }

        float wood(vec2 p) {
            p.x *= 71.0;
            p.y *= 1.9;
            return n11(n21(p) * 30.0);
        }

        Hit map(vec3 p) {
            float f = p.y;
            vec3 q = p;
            q.x += 0.2 + cos(g_time * 10.0) * 0.05;
            q.z += 3.5 + sin(g_time * 10.0) * 0.05;
            q.xz *= rot(g_time * 150.0);
            q.xy *= rot(mix(0.02, 0.04, sin(g_time * 0.001) * 0.5 - 0.5));
            q.y -= 0.4;
            float t = 1.0 - abs(q.y / 0.4 + 0.07);
            float d_totem = smin(
                sdCyl(q, vec2(smoothstep(0.0, 1.0, t * t * t) * 0.35, 0.4)), 
                sdCapsule(q + vec3(0.0, 0.35, 0.0), 0.8, 0.01), 
                mix(0.03, 0.3, t * 0.7)
            );
            return minH(Hit(f, 1, q), Hit(d_totem, 2, q));
        }

        vec3 calcN(vec3 p, float t) {
            float h = 0.004 * t;
            vec2 k = vec2(1.0, -1.0);
            return normalize(
                k.xyy * map(p + k.xyy * h).d + 
                k.yyx * map(p + k.yyx * h).d + 
                k.yxy * map(p + k.yxy * h).d + 
                k.xxx * map(p + k.xxx * h).d
            );
        }

        float calcShadow(vec3 p, vec3 ld) {
            float s = 1.0;
            float t = 0.1;
            for (float i = 0.0; i < 20.0; i++) {
                float h = map(p + ld * t).d;
                s = min(s, 15.0 * h / t);
                t += h;
                if (s < 0.001 || t > 6.0) break;
            }
            return clamp(s, 0.0, 1.0);
        }

        float ao(vec3 p, vec3 n, float h) { return map(p + h * n).d / h; }

        vec3 vignette(vec3 c, vec2 uv) {
            c *= 0.5 + 0.5 * pow(16.0 * uv.x * uv.y * (1.0 - uv.x) * (1.0 - uv.y), 0.4);
            return c;
        }

        vec3 lights(vec3 p, vec3 rd, float d, Hit h) {
            vec3 mat;
            vec3 ld = normalize(vec3(6.0, 3.0, -10.0) - p);
            vec3 ld2 = ld * vec3(-1.0, 1.0, 1.0);
            vec3 n = calcN(p, d);
            if (h.id == 1) {
                mat = mix(mix(vec3(0.17, 0.1, 0.05), vec3(0.08, 0.05, 0.03), wood(p.xz)), vec3(0.2, 0.16, 0.08), 0.3 * wood(p.xz * 0.2));
                n.x -= smoothstep(0.98, 1.0, pow(abs(sin(p.x * 2.4)), 90.0)) * 0.3;
                n = normalize(n);
            }
            else {
                mat = 0.03 * mix(vec3(0.4, 0.3, 0.2), mix(vec3(0.6, 0.3, 0.2), 2.0 * vec3(0.7, 0.6, 0.5), n31(h.uv * 1e2)), n31(h.uv * 36.5));
            }
            float occ = dot(vec3(ao(p, n, 0.2), ao(p, n, 0.5), ao(p, n, 2.0)), vec3(0.3, 0.4, 0.3));
            float l1 = max(0.0, 0.1 + 0.9 * dot(ld, n));
            float spe = smoothstep(0.0, 1.0, pow(max(0.0, dot(rd, reflect(ld, n))), 20.0)) * 10.0 + 
                        smoothstep(0.0, 1.0, pow(max(0.0, dot(rd, reflect(ld2, n))), 20.0)) * 2.0;
            float fre = smoothstep(0.7, 1.0, 1.0 + dot(rd, n));
            l1 *= mix(0.4, 1.0, mix(calcShadow(p, ld), calcShadow(p, ld2), 0.3));
            return mix(mat * (l1 * occ + spe) * vec3(2.0, 1.6, 1.4), vec3(0.005), fre);
        }

        vec3 march(vec3 ro, vec3 rd) {
            vec3 p;
            vec3 c = vec3(0.0);
            float d = 0.01;
            Hit h;
            for (float i = 0.0; i < 90.0; i++) {
                p = ro + rd * d;
                h = map(p);
                if (abs(h.d) < 0.0015) break;
                if (d > 48.0) return vec3(0.0); 
                d += h.d;
            }
            c = lights(p, rd, d, h) * exp(-d * 0.14);
            float f = smoothstep(-2.2, -3.0, p.z) * (h.id == 1 ? 0.4 : 1.0);
            if (f > 0.0) {
                ro = p;
                rd = reflect(rd, calcN(p, d));
                d = 0.1;
                for (float i = 0.0; i < 50.0; i++) {
                    p = ro + rd * d;
                    h = map(p);
                    if (abs(h.d) < 0.002 || d > 1.0) break;
                    d += h.d;
                }
                vec3 reflect_col = (d > 1.0) ? vec3(0.0) : lights(p, rd, d, h);
                c = mix(c, reflect_col, 0.2 * f);
            }
            return c;
        }
    """

    TOTEM_MAIN_FIXED = """

        g_time = mod(u_time * 0.2, 30.0);
        
        vec2 fragCoord = v_tex_coord * u_model_size;
        
        vec2 uv = (fragCoord - 0.5 * u_model_size) / u_model_size.y;
        
        uv.y = -uv.y;
        
        vec3 ro = vec3(0.0, 0.0, -5.0);
        ro.yz *= rot(-0.13 - sin(g_time * 0.3) * 0.02);
        ro.xz *= rot(0.07 + cos(g_time) * 0.02);
        
        // 射线方向 (uv 已经修正)
        vec3 rd = getRayDir(ro, uv);
        
        // Raymarching
        vec3 col = march(ro, rd);
        
        // 色调映射
        col = pow(col * 3.0, vec3(0.45));
        
        col = vignette(col, v_tex_coord);

        gl_FragColor = vec4(col, 1.0);
    """

    renpy.register_shader("shadertoy.InceptionTotemFixed", variables="""
        uniform float u_time;
        uniform vec2 u_model_size;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """,
    vertex_300="""
        v_tex_coord = a_tex_coord;
    """,
    fragment_functions=TOTEM_FUNCTIONS,
    fragment_300=TOTEM_MAIN_FIXED)

init python:

    PHOSPHOR_FUNCTIONS = """
        vec4 tanh_approx(vec4 x) {
            vec4 e2x = exp(2.0 * x);
            return (e2x - 1.0) / (e2x + 1.0);
        }
    """

    PHOSPHOR_MAIN = """
        vec2 fragCoord = v_tex_coord * u_model_size;
        vec2 iResolution = u_model_size;
        
        vec3 dir = normalize(vec3(2.0 * fragCoord - iResolution.xy, -iResolution.y));
        dir.y = -dir.y; // 修正 Y 轴
        
        float t = u_time;
        float z = 0.0;      // 深度 (Raymarch depth)
        float d = 0.0;      // 单步距离 (Step distance)
        float s = 0.0;      // 符号距离 (Signed distance)
        vec4 O = vec4(0.0); // 输出颜色
        
        for(int i = 0; i < 80; i++) {
            
            
            vec3 p = z * dir;
            
            p.z += 5.0;
            
            vec3 a = normalize(cos(vec3(1.0, 2.0, 0.0) + t - d * 8.0));
            
            a = a * dot(a, p) - cross(a, p);
            
            for(float k = 1.0; k < 9.0; k++) {
                a += sin(a * k + t).yzx / k;
            }
            
            s = a.y;
            
            d = 0.1 * abs(length(p) - 3.0) + 0.04 * abs(s);
            
            z += d;
            
            vec4 color_factor = cos(s + vec4(0.0, 1.0, 2.0, 0.0)) + 1.0;
            O += color_factor / max(d, 0.0001) * z;
        }
        
        O = tanh_approx(O / 30000.0);
        
        gl_FragColor = vec4(O.rgb, 1.0);
    """

    renpy.register_shader("shadertoy.Phosphor2", variables="""
        uniform float u_time;
        uniform vec2 u_model_size;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """,
    vertex_300="""
        v_tex_coord = a_tex_coord;
    """,
    fragment_functions=PHOSPHOR_FUNCTIONS,
    fragment_300=PHOSPHOR_MAIN)

init python:
    RIPPLE_SPREAD_FUNCTIONS = """
        float hash12(vec2 p) {
            vec3 p3  = fract(vec3(p.xyx) * .1031);
            p3 += dot(p3, p3.yzx + 33.33);
            return fract((p3.x + p3.y) * p3.z);
        }

        float ripple(vec2 uv, float t) {
            float d = length(uv);
            
            float radius = t * 0.6; 
            
            float dist_from_wave = d - radius;
            
            float wave = sin(dist_from_wave * 40.0) * exp(-abs(dist_from_wave) * 10.0);
            
            wave *= smoothstep(1.0, 0.0, t);
            
            return wave;
        }

        float get_water_height(vec2 uv, float time) {
            // 增加网格密度，让雨滴更小更多
            vec2 grid_uv = uv * 5.0; 
            vec2 id = floor(grid_uv);
            vec2 fract_uv = fract(grid_uv);
            
            float h = 0.0;
            
            for(int y = -1; y <= 1; y++) {
                for(int x = -1; x <= 1; x++) {
                    vec2 offs = vec2(float(x), float(y));
                    vec2 cell_id = id + offs;
                    
                    // 每个格子的随机属性
                    float rnd = hash12(cell_id);
                    
                    // 随机位置偏移
                    vec2 center = offs + vec2(rnd, hash12(cell_id * 2.5)) - 0.5;
                    
                    // 随机时间偏移
                    float t_offs = hash12(cell_id + vec2(3.0, 4.0));
                    
                    // 循环播放雨滴：时间 * 速度 + 偏移
                    // fract 让时间在 0~1 之间循环
                    float t = fract(time * 0.8 + t_offs);
                    
                    // 计算当前像素相对于该雨滴中心的坐标
                    vec2 p = fract_uv - center - 0.5;
                    
                    // 累加波纹高度
                    h += ripple(p, t);
                }
            }
            return h;
        }
    """

    RIPPLE_SPREAD_MAIN = """
        vec2 uv = v_tex_coord;
        
        vec2 uv_aspect = uv;
        uv_aspect.x *= u_model_size.x / u_model_size.y;
        
        // 采样高度 (上下左右) 用来计算法线
        vec2 e = vec2(2.0 / u_model_size.x, 2.0 / u_model_size.y);
        
        float h_center = get_water_height(uv_aspect, u_time);
        float h_right  = get_water_height(uv_aspect + vec2(e.x, 0.0), u_time);
        float h_up     = get_water_height(uv_aspect - vec2(0.0, e.y), u_time);
        
        vec3 norm = normalize(vec3(h_center - h_right, h_center - h_up, 0.2));
        
        vec2 distorted_uv = uv + norm.xy * 0.09;
        vec4 bg_col = texture2D(tex0, distorted_uv);
        
        // 光照 (Lighting)
        vec3 light_dir = normalize(vec3(0.5, -0.5, 1.0));
        light_dir.y = -light_dir.y; // Ren'Py Y轴修正
        
        // 高光 (Specular)
        float spec = pow(max(0.0, reflect(light_dir, norm).z), 32.0);
        
        // 漫反射 (Diffuse)
        float diff = max(0.0, dot(norm, light_dir));
        
        // 颜色混合
        vec4 final_col = mix(bg_col, vec4(0.6, 0.8, 1.0, 1.0), 0.2);
        final_col += vec4(spec);
        
        // 稍微加一点漫反射阴影
        final_col *= (0.8 + 0.2 * diff);
        
        gl_FragColor = final_col;
        gl_FragColor.a = 1.0;
    """

    renpy.register_shader("shadertoy.RippleSpread", variables="""
        uniform float u_time;
        uniform vec2 u_model_size;
        uniform sampler2D tex0;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """,
    vertex_300="""
        v_tex_coord = a_tex_coord;
    """,
    fragment_functions=RIPPLE_SPREAD_FUNCTIONS,
    fragment_300=RIPPLE_SPREAD_MAIN)


init python:

    FIRE_SMOKE_FUNCTIONS = """
        vec4 tanh_approx(vec4 x) {
            vec4 e2x = exp(2.0 * x);
            return (e2x - 1.0) / (e2x + 1.0);
        }

        vec4 smoke(vec2 u, float time) {
            float d = 0.0;      // 射线距离
            float s = 0.0;      // 单步距离
            vec4 o = vec4(0.0); // 累积颜色/密度
            vec3 p = vec3(0.0); // 射线位置
            
            for(int i = 0; i < 64; i++) {
                
                p = vec3(u * d, d - time * 10.0);
                
                float scale = 0.01;
                for(int k = 0; k < 9; k++) {
                    if(scale >= 4.0) break;
                    
                    // 空间扭曲
                    p.yz -= cos(p.zx * 0.05);
                    p.yz -= abs(dot(sin(0.02 * p.z * scale + 0.03 * p.x + time + 0.5 * p / scale), vec3(0.1 + scale)));
                    
                    scale += scale; // 步长倍增
                }
                
                p *= vec3(0.3, 0.6, 1.0);
                
                // SDF 距离场：主要由 p.y 决定
                s = 0.3 + 0.2 * abs(p.y - 2.0);
                
                d += s; // 射线前进
                
                // 密度累积 (距离越近，密度越大)
                o += 10.0 / s;
            }
            
            return o / 2000.0;
        }

        vec4 fire(vec2 u, float time) {
            float d = 0.0;
            float s = 0.0;
            vec4 o = vec4(0.0);
            vec3 p = vec3(0.0);
            
            vec4 angle_vec = 0.3 * time + vec4(0.0, 33.0, 11.0, 0.0);
            vec4 cos_vals = cos(angle_vec);
            mat2 r = mat2(cos_vals.x, cos_vals.y, cos_vals.z, cos_vals.w);
            
            for(int i = 0; i < 64; i++) {
                p = vec3(u * d, d);
                
                p += cos(p.z + time + p.yzx * 0.5) * 0.6;
                
                s = p.y - 2.0;
                
                p.yz *= r;
                
                for(float n = 1.6; n < 32.0; n += n) {
                    s += abs(dot(sin(p.z + time + p * n), vec3(2.5))) / n;
                }
                
                float step_dist = 0.01 + abs(s) * 0.1;
                d += step_dist;
                
                o += 1.0 / step_dist;
            }
            
            return vec4(6.0, 2.0, 1.0, 1.0) * o * o / d / 200000.0;
        }
    """

    FIRE_SMOKE_MAIN = """
        vec2 fragCoord = v_tex_coord * u_model_size;
        vec2 iResolution = u_model_size;
        
        vec2 uv = (fragCoord - iResolution.xy * 0.5) / iResolution.y;
        
        uv.y = -uv.y;
        
        vec4 fire_col = fire(uv, u_time);
        vec4 smoke_col = smoke(uv, u_time);
        
        vec4 final_col = mix(fire_col, smoke_col, 0.92);
        
        final_col = tanh_approx(final_col);
        
        gl_FragColor = vec4(final_col.rgb, 1.0);
    """

    renpy.register_shader("shadertoy.FireAndSmoke", variables="""
        uniform float u_time;
        uniform vec2 u_model_size;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """,
    vertex_300="""
        v_tex_coord = a_tex_coord;
    """,
    fragment_functions=FIRE_SMOKE_FUNCTIONS,
    fragment_300=FIRE_SMOKE_MAIN)

image inegg_rain = ShaderToy("inegg", "shadertoy.RippleSpread")
image firefire = ShaderToy("eatingstreet", "shadertoy.FireAndSmoke")
image water_somewhat = ShaderToy("eatingstreet", "shadertoy.RippleSpread")
image phos = ShaderToy("plgrd", "shadertoy.Phosphor2")
image gyro = ShaderToy("plgrd", "shadertoy.InceptionTotemFixed")
image bat_mount = ShaderToy("plgrd", "shadertoy.CyberTunnelFixed")
image sft = ShaderToy("plgrd", "shadertoy.SciFiTunnel")