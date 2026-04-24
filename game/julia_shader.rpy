init python:

    # --- 1. 辅助函数库 ---
    OCEAN_FUNCTIONS = """
        #define DRAG_MULT 0.048
        #define ITERATIONS_RAYMARCH 12  // 原版13，微调
        #define ITERATIONS_NORMAL 40    // 原版48，微调

        // 全局变量
        float iTime;
        vec2 iResolution;

        // --- 基础数学工具 ---
        mat3 rotmat(vec3 axis, float angle) {
            float s = sin(angle);
            float c = cos(angle);
            float oc = 1.0 - c;
            return mat3(oc * axis.x * axis.x + c, oc * axis.x * axis.y - axis.z * s,  oc * axis.z * axis.x + axis.y * s, 
            oc * axis.x * axis.y + axis.z * s,  oc * axis.y * axis.y + c,           oc * axis.y * axis.z - axis.x * s, 
            oc * axis.z * axis.x - axis.y * s,  oc * axis.y * axis.z + axis.x * s,  oc * axis.z * axis.z + c);
        }

        // --- 波浪生成逻辑 ---
        vec2 wavedx(vec2 position, vec2 direction, float speed, float frequency, float timeshift) {
            float x = dot(direction, position) * frequency + timeshift * speed;
            float wave = exp(sin(x) - 1.0);
            float dx = wave * cos(x);
            return vec2(wave, -dx);
        }

        float getwaves(vec2 position, int iterations){
            float iter = 0.0;
            float phase = 6.0;
            float speed = 2.0;
            float weight = 1.0;
            float w = 0.0;
            float ws = 0.0;
            for(int i=0; i<iterations; i++){
                vec2 p = vec2(sin(iter), cos(iter));
                vec2 res = wavedx(position, p, speed, phase, iTime);
                position += p * res.y * weight * DRAG_MULT;
                w += res.x * weight;
                iter += 12.0;
                ws += weight;
                weight = mix(weight, 0.0, 0.2);
                phase *= 1.18;
                speed *= 1.07;
            }
            return w / ws;
        }

        // --- Raymarching 核心 ---
        float raymarchwater(vec3 camera, vec3 start, vec3 end, float depth){
            vec3 pos = start;
            float h = 0.0;
            vec3 dir = normalize(end - start);
            float eps = 0.01;
            
            // 循环次数：这是性能杀手。
            // 如果卡顿，请将 200 改为 100 或更低。
            for(int i=0; i<200; i++){
                h = getwaves(pos.xz * 0.1, ITERATIONS_RAYMARCH) * depth - depth;
                float dist_pos = distance(pos, camera);
                if(h + eps*dist_pos > pos.y) {
                    return dist_pos;
                }
                pos += dir * (pos.y - h);
            }
            return -1.0;
        }

        // --- 法线计算 ---
        vec3 normal(vec2 pos, float e, float depth){
            vec2 ex = vec2(e, 0);
            float H = getwaves(pos.xy * 0.1, ITERATIONS_NORMAL) * depth;
            vec3 a = vec3(pos.x, H, pos.y);
            return normalize(cross(normalize(a-vec3(pos.x - e, getwaves((pos.xy - ex.xy)*0.1, ITERATIONS_NORMAL) * depth, pos.y)), 
                                normalize(a-vec3(pos.x, getwaves((pos.xy + ex.yx )* 0.1, ITERATIONS_NORMAL) * depth, pos.y + e))));
        }

        // --- 摄像机射线 ---
        vec3 getRay(vec2 uv){
            // 修正：Ren'Py Y轴翻转，这里需要再次翻转uv.y
            uv = (uv * 2.0 - 1.0) * vec2(iResolution.x / iResolution.y, 1.0);
            uv.y = -uv.y; 
            
            vec3 proj = normalize(vec3(uv.x, uv.y, 1.0) + vec3(uv.x, uv.y, -1.0) * pow(length(uv), 2.0) * 0.05);
            
            // 模拟鼠标视角：固定一个好看的角度
            // Mouse.x -> 0.0, Mouse.y -> 0.1 (稍微俯视)
            float mx = 0.0; 
            float my = 0.15; 
            
            vec3 ray = rotmat(vec3(0.0, -1.0, 0.0), 3.0 * (mx * 2.0 - 1.0)) * rotmat(vec3(1.0, 0.0, 0.0), 1.5 * (my * 2.0 - 1.0)) * proj;
            return ray;
        }

        float intersectPlane(vec3 origin, vec3 direction, vec3 point, vec3 n) { 
            return clamp(dot(point - origin, n) / dot(direction, n), -1.0, 9991999.0); 
        }

        // --- 大气与光照 ---
        vec3 extra_cheap_atmosphere(vec3 raydir, vec3 sundir){
            sundir.y = max(sundir.y, -0.07);
            float special_trick = 1.0 / (raydir.y * 1.0 + 0.1);
            float special_trick2 = 1.0 / (sundir.y * 11.0 + 1.0);
            float raysundt = pow(abs(dot(sundir, raydir)), 2.0);
            float sundt = pow(max(0.0, dot(sundir, raydir)), 8.0);
            float mymie = sundt * special_trick * 0.2;
            vec3 suncolor = mix(vec3(1.0), max(vec3(0.0), vec3(1.0) - vec3(5.5, 13.0, 22.4) / 22.4), special_trick2);
            vec3 bluesky= vec3(5.5, 13.0, 22.4) / 22.4 * suncolor;
            vec3 bluesky2 = max(vec3(0.0), bluesky - vec3(5.5, 13.0, 22.4) * 0.002 * (special_trick + -6.0 * sundir.y * sundir.y));
            bluesky2 *= special_trick * (0.24 + raysundt * 0.24);
            return bluesky2 * (1.0 + 1.0 * pow(1.0 - raydir.y, 3.0)) + mymie * suncolor;
        } 

        vec3 getatm(vec3 ray){
            return extra_cheap_atmosphere(ray, normalize(vec3(1.0))) * 0.5;
        }

        float sun(vec3 ray){
            vec3 sd = normalize(vec3(1.0));   
            return pow(max(0.0, dot(ray, sd)), 528.0) * 110.0;
        }

        // --- ACES 色调映射 ---
        vec3 aces_tonemap(vec3 color){	
            mat3 m1 = mat3(
                0.59719, 0.07600, 0.02840,
                0.35458, 0.90834, 0.13383,
                0.04823, 0.01566, 0.83777
            );
            mat3 m2 = mat3(
                1.60475, -0.10208, -0.00327,
                -0.53108,  1.10813, -0.07276,
                -0.07367, -0.00605,  1.07602
            );
            vec3 v = m1 * color;    
            vec3 a = v * (v + 0.0245786) - 0.000090537;
            vec3 b = v * (0.983729 * v + 0.4329510) + 0.238081;
            return pow(clamp(m2 * (a / b), 0.0, 1.0), vec3(1.0 / 2.2));	
        }
    """

# --- 2. 主逻辑 (黑潮版) ---
    OCEAN_MAIN = """
        iTime = u_time;
        iResolution = u_model_size;
        vec2 uv = v_tex_coord; 
        
        float waterdepth = 2.1;
        vec3 wfloor = vec3(0.0, -waterdepth, 0.0);
        vec3 wceil = vec3(0.0, 0.0, 0.0);
        vec3 orig = vec3(0.0, 2.0, 0.0);
        
        vec3 ray = getRay(uv);
        float hihit = intersectPlane(orig, ray, wceil, vec3(0.0, 1.0, 0.0));
        
        // 天空渲染 (保持明亮，形成反差)
        if(ray.y >= -0.01){
            vec3 C = getatm(ray) * 2.0 + sun(ray);
            C = aces_tonemap(C);
            gl_FragColor = vec4(C, 1.0);   
            return;
        }
        
        // 海面渲染
        float lohit = intersectPlane(orig, ray, wfloor, vec3(0.0, 1.0, 0.0));
        vec3 hipos = orig + ray * hihit;
        vec3 lopos = orig + ray * lohit;
        
        float dist = raymarchwater(orig, hipos, lopos, waterdepth);
        vec3 pos = orig + ray * dist;

        vec3 N = normal(pos.xz, 0.001, waterdepth);
        vec2 velocity = N.xz * (1.0 - N.y);
        N = mix(vec3(0.0, 1.0, 0.0), N, 1.0 / (dist * dist * 0.01 + 1.0));
        vec3 R = reflect(ray, N);
        
        // 菲涅尔效应
        float fresnel = (0.04 + (1.0-0.04)*(pow(1.0 - max(0.0, dot(-N, ray)), 5.0)));
        
        // --- 黑潮调色核心修改 ---
        
        // 1. 获取天空反射颜色
        vec3 sky_reflection = getatm(R) * 2.0;
        
        // 2. 定义黑潮的固有色 (极深的墨蓝)
        vec3 kuroshio_base = vec3(0.002, 0.01, 0.05); 
        
        // 3. 混合：
        // 水体本身是深色的 (kuroshio_base)
        // 只有在菲涅尔反射强的地方（远处/切角）才显现出天空的颜色
        // 这里的 0.6 是为了压暗天空反射，让水看起来更深
        vec3 C = mix(kuroshio_base, sky_reflection, fresnel * 0.6);
        
        // 4. 叠加太阳高光
        // 太阳光依然强烈，形成黑水白光的强烈对比
        C += fresnel * sun(R);
        
        // 色调映射
        C = aces_tonemap(C);
        
        // 稍微加强一点对比度，让暗部更暗
        C = pow(C, vec3(1.1)); 
        
        gl_FragColor = vec4(C, 1.0);
    """
    # --- 3. 注册 ---
    renpy.register_shader("shadertoy.RealisticOcean", variables="""
        uniform float u_time;
        uniform vec2 u_model_size;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """,
    vertex_300="""
        v_tex_coord = a_tex_coord;
    """,
    fragment_functions=OCEAN_FUNCTIONS,
    fragment_300=OCEAN_MAIN)

image fractal_jewel = ShaderToy("eatingstreet", "shadertoy.RealisticOcean")